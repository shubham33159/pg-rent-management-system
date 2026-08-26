from django.shortcuts import render
from dashboard.forms import TenantForm, AddressForm, RoomForm
from dashboard.models import Tenant, Address, Room
# Create your views here.

def dashboard(request):
    return render(request, "dashboard/dashboard.html")

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


def registration(request):
    if request.method == "POST":
        tenant_form = TenantForm(request.POST)
        address_form = AddressForm(request.POST)
        if tenant_form.is_valid() and address_form.is_valid():
            address= address_form.save()
            tenant = tenant_form.save(commit=False)
            tenant.address = address
            tenant.save()
    else:
        tenant_form = TenantForm()
        address_form = AddressForm()

    tenant_form = list(tenant_form)
    address_form = list(address_form)

    return render(request, "dashboard/registration.html", {
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
    tenant = Tenant.objects.all()
    room = Room.objects.all()
    return render(request, "dashboard/room.html", {
        "tenant": tenant,
        "room": room
    })


def payment(request):
    return render(request, "dashboard/payments.html")

def complaint_registration(request):
    return render(request, "dashboard/complaint-registration.html")
