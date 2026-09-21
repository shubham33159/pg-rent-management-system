from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from dashboard.forms import TenantForm, AddressForm, RoomForm, MaintenanceForm
from dashboard.models import Tenant, Address, Room, Payment, Maintenance
from django.views.decorators.http import require_POST

import json
# Create your views here.

from itertools import groupby
from collections.abc import Iterable, Iterator

from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User

import razorpay
from django.conf import settings
from django.http import JsonResponse

from django.utils import timezone
import zoneinfo

def dashboard(request):
    return render(request, "dashboard/dashboard.html")

# without form
# def registration(request):
#     if request.method == "POST":
#         tenant_form = TenantForm(request.POST)
#         address_form = AddressForm(request.POST)
#         room_form = RoomForm(request.POST)
#         if tenant_form.is_valid() and address_form.is_valid() and room_form.is_valid():
#             tenant_data = tenant_form.cleaned_data
#             address_data = address_form.cleaned_data
#             room_data = room_form.cleaned_data

#             address = Address(
#                 street = address_data["street"],
#                 city = address_data["city"],
#                 state = address_data["state"],
#                 pincode = address_data["pincode"],
#                 country = address_data["country"]
#             )
#             address.save()

#             room = Room(
#                 number = room_data["number"],
#                 sharing_type = room_data["sharing_type"],
#                 rent = room_data["rent"],
#                 floor = room_data["floor"],
#                 room_state = room_data["room_state"]
#             )
#             room.save()

#             tenant = Tenant(
#                 firstname = tenant_data["firstname"], 
#                 lastname = tenant_data["lastname"], 
#                 email = tenant_data["email"], 
#                 uid = tenant_data["uid"],
#                 gender = tenant_data["gender"],
#                 status = tenant_data["status"],
#                 emg_contact_name = tenant_data["emg_contact_name"],
#                 emg_contact = tenant_data["emg_contact"],
#                 address = address,
#                 room = room,
#                 move_in_date = tenant_data["move_in_date"],
#                 security_deposit = tenant_data["security_deposit"],
#                 adv_rent = tenant_data["adv_rent"],
#                 notes = tenant_data["notes"]
#             )
#             tenant.save()
#     else:
#         tenant_form = TenantForm()
#         address_form = AddressForm()
#         room_form = RoomForm()

#     return render(request, "dashboard/registration.html", {
#         "tenant_form": tenant_form,
#         "address_form": address_form,
#         "room_form": room_form
#     })


def login_views(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            if user.is_staff:
                return redirect("dashboard")
            else:
                return redirect("tenant-dashboard")

        else:
            return render(request, "dashboard/login.html", {
                "error": "Invalid username and password."
            })
    else:
        return render(request, "dashboard/login.html")


def logout_views(request):
    logout(request)
    return redirect("login")


## with form
def registration(request):
    if request.method == "POST":
        tenant_form = TenantForm(request.POST)
        address_form = AddressForm(request.POST)
        if tenant_form.is_valid() and address_form.is_valid():
            username = tenant_form.cleaned_data["username"]
            password = tenant_form.cleaned_data["password"]

            user = User.objects.create_user(
                username = username,
                password = password
            )

            address= address_form.save()
            tenant = tenant_form.save(commit=False)

            tenant.user = user
            tenant.address = address

            tenant.save()

            return HttpResponseRedirect(reverse("registration"))

    else:
        tenant_form = TenantForm()
        address_form = AddressForm()

    tenant_form = list(tenant_form)
    address_form = list(address_form)

    return render(request, "dashboard/registration.html", {
        "tenant_login_credientials": tenant_form[13:16],
        "personal_details_form" : tenant_form[:6],
        "emergency_contact_form": tenant_form[6:8],
        "address_form" : address_form[:6],
        "room_finance_form" : tenant_form[8:12],
        "additional_notes_form" : tenant_form[12:13],
    })





def tenant(request):
    print(request.GET)
    search_query = request.GET.get("q","").strip()

    tenants = Tenant.objects.all()

    if search_query:
        tenants = tenants.filter(
            Q(firstname__icontains=search_query) | 
            Q(lastname__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query) | 
            Q(room__number__icontains=search_query)
        )

    return render(request, "dashboard/tenant.html", {
        "tenants" : tenants,
        "search_query": search_query,
    })


def room(request):
    rooms = Room.objects.all().order_by("floor", "number")
    grouped_rooms = ((floor, list(room)) for floor, room in groupby(rooms, key = lambda room: room.floor))


    return render(request, "dashboard/room.html", {
        "grouped_rooms": grouped_rooms,
    })


def payment(request):
    return render(request, "dashboard/payments.html")

def complaint_registration(request):
    return render(request, "dashboard/complaint-registration.html")


def tenant_dashboard(request):
    return render(request, "dashboard/tenant-dashboard.html")

def tenant_payment(request):
    tenant = Tenant.objects.get(user=request.user)

    room_rent = tenant.room.rent
    room_number = tenant.room.number
    rent_status = tenant.rent_status

    return render(request, "dashboard/tenant-payment.html", {
        "rent_status": rent_status,
        "room_rent": room_rent,
        "room_number": room_number,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID
    })



def create_payment_order(request):
    tenant = Tenant.objects.get(user=request.user)
    # adv_rent = tenant.adv_rent
    amount = tenant.room.rent
    month=timezone.now().date().replace(day=1)

    payment, created = Payment.objects.get_or_create(
            tenant=tenant, 
            month=month,
            defaults={
                "rent_amount": amount,
                "advance_used": 0,
                "penalty": 0,
                "total_amount": amount,
                "status": "pending",
            }
        )

    if created:
        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        order_data = {
            "amount" : amount * 100,
            "currency": "INR",
            "receipt": f"rent_{tenant.firstname}_{timezone.now().timestamp()}"
        }
    
        order = client.order.create(data=order_data)

        payment.razorpay_order_id = order["id"]
        payment.save()

    
    return JsonResponse({
        "order_id": payment.razorpay_order_id,
        "amount": amount,
        "currency": "INR"
    })

def verify_payment(request):
    tenant = Tenant.objects.get(user=request.user)

    data = json.loads(request.body)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:
        print("inside try block")
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"],
        })

        payment = Payment.objects.get(
            tenant=tenant, 
            razorpay_order_id=data["razorpay_order_id"]
        )


        payment.status = "paid"
        tenant.rent_status = "paid"
        payment.razorpay_payment_id = data["razorpay_payment_id"]
        payment.paid_at = timezone.now()
        payment.save()
        tenant.save()

        return HttpResponseRedirect("tenant-payment")
    
    except razorpay.errors.SignatureVerificationError:
        print("inside except block")
        return JsonResponse({
            "status": "failed"
        }, status=400)

@require_POST
def payment_failed(request):
    tenant = Tenant.objects.get(user=request.user)

    data = json.loads(request.body)
    order_id = data.get("razorpay_order_id")
    payment_id = data.get("razorpay_payment_id")
    payment = Payment.objects.get(
        tenant=tenant,
        razorpay_order_id=order_id
    )

    payment.status='failed'
    payment.razorpay_payment_id = payment_id
    payment.save()

    return JsonResponse({
        "status": "failed"
    })

def tenant_payment_history(request):
    tenant = Tenant.objects.get(user=request.user)
    payments = Payment.objects.filter(tenant=tenant)

    total_paid_payment = 0
    total_paid_payment_count = 0

    total_pending_payment = 0
    total_pending_payment_count = 0

    total_overdue_payment = 0
    total_overdue_payment_count = 0

    for payment in payments:
        if payment.status == "paid":
            total_paid_payment += payment.total_amount
            total_paid_payment_count += 1

        elif payment.status == "pending":
            total_pending_payment += payment.total_amount
            total_pending_payment_count += 1

            if payment.penalty >= 500:
                total_overdue_payment += payment.penalty
                total_overdue_payment_count += 1

    return render(request, "dashboard/tenant-payment-history.html", {
        "total_paid_payment": total_paid_payment,
        "total_pending_payment": total_pending_payment,
        "total_overdue_payment": total_overdue_payment,

        "total_paid_payment_count": total_paid_payment_count,
        "total_pending_payment_count": total_pending_payment_count,
        "total_overdue_payment_count": total_overdue_payment_count,
    
        "payments": payments
    })


def tenant_maintenance(request):

    tenant = Tenant.objects.get(user=request.user)

    if request.method == "POST":
        maintenance_form = MaintenanceForm(request.POST)
        if maintenance_form.is_valid():
            maintenance = maintenance_form.save(commit=False)
            maintenance.tenant = tenant
            maintenance.save()
            return HttpResponseRedirect(reverse("tenant-maintenance"))

    else:
        maintenance_form = MaintenanceForm()
        
    maintenance = Maintenance.objects.filter(tenant=tenant).order_by("-status_update_time")

    return render(request, "dashboard/tenant-maintenance.html", {
        "maintenance_form" : maintenance_form,
        "maintenance" : maintenance
    })
