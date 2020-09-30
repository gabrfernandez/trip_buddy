from django.urls import path
from . import views

urlpatterns=[
    path("", views.show_login_reg_page),
    path("users", views.register_form),
    path("dashboard", views.show_dashboard),
    path("login", views.login_form),
    path("logout", views.logout), 
    path("createtrip", views.create_trip),
    path("create_trip_form", views.create_trip_form),
    path("trips/<int:trip_id>", views.trip_profile),
    path("trips/edit/<int:trip_id>", views.edit_trip_page),
    path("trips/edit/<int:trip_id>/update", views.update),
    path("trips/<int:trip_id>/delete", views.delete)
]