from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_views, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("registration/", views.registration, name="registration"),
    path("tenant/", views.tenant, name="tenant"),
    path("room/", views.room, name="room"),
    path("payment/", views.payment, name="payment"),
    path("complaint-registration/", views.complaint_registration, name="complaint-registration"),
    path("agent-dashboard/", views.agent_dashboard, name="agent-dashboard")
]


