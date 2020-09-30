from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, data):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(data['first_name'])<1:
            errors['first_name']="Please enter your first name!"
        if len(data['last_name'])<2:
            errors["last_name"]="Please enter at least 2 characters for your last name!"
        if len(data['email'])<1:
            errors["email"]="Please enter an email!"
        #if email does NOT match
        elif not EMAIL_REGEX.match(data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(data['password'])<8:
            errors['password']="Please enter at least 8 characters for your password!"
        if data['pw_confirm']!= data["password"]:
            errors['pw_confirm']="Please match your password to its confirmation!"

        return errors

class TripManager(models.Manager):
    def basic_validator(self, data):
        errors={}
        if len(data['destination'])<3:
            errors['destination']="Destination must be at least 3 characters."
        if data['start_date']=='':
            errors['start_date'] = "Start date field is empty."
        if data['end_date']=='':
            errors['end_date'] = "End date field is empty."
        if len(data['plan'])<3:
            errors['plan']="Plan must be at least 3 characters."
            
        return errors


class User(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Trip(models.Model):
    destination=models.CharField(max_length=100)
    start_date=models.DateField()
    end_date=models.DateField()
    plan=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, related_name="trips", on_delete = models.CASCADE)
    objects=TripManager()