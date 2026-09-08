from django.shortcuts import render, redirect
from dashboard.forms import TenantForm, AddressForm, RoomForm
from dashboard.models import Tenant, Address, Room
# Create your views here.

from itertools import groupby
from collections.abc import Iterable, Iterator

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

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
                print("I am in agent dashboard")
                return redirect("agent-dashboard")

        else:
            return render(request, "dashboard/login.html", {
                "error": "Invalid username and password."
            })
    else:
        return render(request, "dashboard/login.html")

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
    tenant_info = Tenant.objects.all()
    return render(request, "dashboard/tenant.html", {
        "tenant_info" : tenant_info
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


def agent_dashboard(request):
    return render(request, "dashboard/agent-dashboard.html")