from django.urls import path

from . import views

urlpatterns = [

    ## admin UI
    path("login/", views.login_views, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("registration/", views.registration, name="registration"),
    path("tenant/", views.tenant, name="tenant"),
    path("room/", views.room, name="room"),
    path("payment/", views.payment, name="payment"),
    path("complaint-registration/", views.complaint_registration, name="complaint-registration"),


    ## Tenant UI
    path("tenant-dashboard/", views.tenant_dashboard, name="tenant-dashboard"),
    path("tenant-payment/", views.tenant_payment, name="tenant-payment"),
    path("create-payment-order/", views.create_payment_order, name="create-payment-order"),
    path("verify-payment/", views.verify_payment, name="verify-payment"),
    path("tenant-maintenance/", views.tenant_maintenance, name="tenant-maintenance"),

]


