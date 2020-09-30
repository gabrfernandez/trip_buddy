from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
import bcrypt

def show_login_reg_page(request):
    return render (request, "index.html")

def register_form(request):
    errors=User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, err in errors.items():
            messages.error(request, err)
        return redirect("/")
        
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    created_user=User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
    )
    request.session["user_id"]=created_user.id
    request.session["first_name"]=created_user.first_name 

    return redirect("/dashboard")

def show_dashboard(request):

    if "user_id" not in request.session:
        messages.error(request, "Please login or register first.")
        return redirect("/")

    context={
        "user":User.objects.get(id=request.session["user_id"]),
        "trip":Trip.objects.all()

    }
    return render(request, "dashboard.html", context)

def login_form(request):

    potential_users=User.objects.filter(email=request.POST['email'])
    
    if len(potential_users)==0:
        messages.error(request, "Please check your email and password.")

        return redirect("/")

    user=potential_users[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Please check your email and password.")

        return redirect("/")

    request.session["user_id"]=user.id
    request.session["first_name"]=user.first_name 
    return redirect ("/dashboard")

def logout(request):
    request.session.pop("user_id")
    request.session.pop("first_name")

    return redirect("/")

def create_trip(request):
    if "user_id" not in request.session:
        messages.error(request, "Please login or register first.")
        return redirect("/")
    context={
        "user":User.objects.get(id=request.session["user_id"]),
    }
    return render(request, "create-trip.html", context)

def create_trip_form (request):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, err in errors.items():
            messages.error(request, err)
        return redirect ("/createtrip")
    
    Trip.objects.create(
        destination=request.POST['destination'],
        start_date=request.POST['start_date'],
        end_date=request.POST['end_date'],
        plan=request.POST['plan'],
        user = User.objects.get(id=request.session['user_id'])
    )

    return redirect("/dashboard")

def trip_profile (request, trip_id):
    if "user_id" not in request.session:
        messages.error(request, "Please login or register first.")
        return redirect("/")
    context={
        "trip": Trip.objects.get(id=trip_id), 
        "user":User.objects.get(id=request.session["user_id"]),
    }
    return render(request, "trip-profile.html", context)

def edit_trip_page(request, trip_id):
    if "user_id" not in request.session:
        messages.error(request, "Please login or register first.")
        return redirect("/")
    trip=Trip.objects.get(id=trip_id)
    trip.start_date=trip.start_date.strftime("%Y-%m-%d")
    trip.end_date=trip.end_date.strftime("%Y-%m-%d")
    context={
        "trip": trip,
        "user":User.objects.get(id=request.session["user_id"]),
    }

    return render (request, "edit-trip.html", context)

def update (request, trip_id):
    errors=Trip.objects.basic_validator(request.POST)

    if len(errors)>0:
        for key, err in errors.items():
            messages.error(request, err)
        return redirect(f"/trips/edit/{trip_id}")
        

    newtrip=Trip.objects.get(id=trip_id)
    newtrip.destination=request.POST['destination']
    newtrip.start_date=request.POST['start_date']
    newtrip.end_date=request.POST['end_date']
    newtrip.plan=request.POST['plan']

    newtrip.save()

    return redirect("/dashboard")

def delete(request, trip_id):
    trip=Trip.objects.get(id=trip_id)
    trip.delete()

    return redirect("/dashboard")
