from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def registration(request):
    return render(request, "dashboard/registration.html")

def tenant(request):
    return render(request, "dashboard/tenant.html")

def payment(request):
    return render(request, "dashboard/payments.html")

def complaint_registration(request):
    return render(request, "dashboard/complaint-registration.html")
