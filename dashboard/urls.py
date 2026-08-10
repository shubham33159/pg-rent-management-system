from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("registration", views.registration, name="registration"),
    path("tenant", views.tenant, name="tenant"),
    path("room", views.tenant, name="room"),
    path("payment", views.payment, name="payment"),
    path("complaint-registration", views.complaint_registration, name="complaint-registration")
]


