from django import forms
from .models import Tenant, Address, Room
from django.core.validators import RegexValidator
from datetime import date


# class TenantForm(forms.Form):
#     firstname = forms.CharField(label="First Name" ,max_length=100)
#     lastname = forms.CharField(label="Last Name" ,max_length=100)
#     email = forms.EmailField(label="Email")
#     uid = forms.CharField(label="Adhar Number", max_length=100)
#     gender = forms.ChoiceField(label="Gender", choices=[("male","Male"), ("female","Female"),])
#     status = forms.CharField(label="Status", max_length=100)
#     emg_contact_name = forms.CharField(label="Contact Name", max_length=100)
#     emg_contact = forms.CharField(label="Emergency Phone", max_length=10)
#     move_in_date = forms.DateField(label="Move-In Date")
#     security_deposit = forms.DecimalField(label="Security Deposit", max_digits=10, decimal_places=2)
#     adv_rent = forms.DecimalField(label="Advance Rent", max_digits=10, decimal_places=2)
#     notes = forms.CharField(label="Additional Notes", widget=forms.Textarea, max_length=1000)

# class AddressForm(forms.Form):
#     street = forms.CharField(label="Street", max_length=100)
#     city = forms.CharField(label="City", max_length=100)
#     state = forms.CharField(label="State", max_length=100)
#     pincode = forms.CharField(label="Pincode", max_length=6)
#     country = forms.CharField(label="Country", max_length=100)

# class RoomForm(forms.Form):
#     number = forms.CharField(label="Room Number", max_length=10)
#     sharing_type = forms.IntegerField(label="Sharing Type", min_value=2, max_value=3)
#     rent = forms.IntegerField(label="Rent")
#     floor = forms.IntegerField(label="Floor", min_value=1, max_value=7)
#     room_state = forms.ChoiceField(label="Room State", choices=[("occupied","OCCUPIED"),("vacant","VACANT"),("maintenance","MAINTENANCE")])


class TenantForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(min_length=14, max_length=140, widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=14, max_length=140, widget=forms.PasswordInput)

    # gender = forms.ChoiceField(label="Gender", choices=[("","Select Gender"), ("male","Male"), ("female","Female"), ("others","Others")])
    uid = forms.CharField(label="Adhar Number", max_length=12, validators=[RegexValidator(regex=r"^\d{12}$", message="Aadhaar number must contain exactly 12 digits.")], widget=forms.TextInput(attrs={"placeholder": "XXXX XXXX XXXX"}))
    emg_contact = forms.CharField(label="Contact Phone", max_length=10, validators=[RegexValidator(regex=r"^\d{10}$", message="Phone number must contain exactly 10 digits.")], widget=forms.TextInput(attrs={"placeholder": "e.g. 9999999999"}))
    move_in_date = forms.DateField(label="Move-In Date", initial=date.today, widget=forms.DateInput(attrs={"type": "date"}))

    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        empty_label="Select Room"
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password do not match")

        return cleaned_data

    class Meta:
        model = Tenant
        exclude = ["slug","address", "status", "user"]

        widgets = {
            # "firstname": forms.TextInput(attrs={"placeholder": "Enter first name"}),
            # "lastname": forms.TextInput(attrs={"placeholder": "Enter last name"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "e.g. 9898989898"}),
            # "email": forms.TextInput(attrs={"placeholder": "shubham@email.com"}),
            "emg_contact_name": forms.TextInput(attrs={"placeholder": "Parent / Gaurdian name"}),
            "security_deposit": forms.TextInput(attrs={"placeholder": "e.g. 6000"}),
            "adv_rent": forms.TextInput(attrs={"placeholder": "0"}),
            "notes": forms.Textarea(attrs={"placeholder": "Any special requirements, restrictions, or notes about this tenant…"})
        }

        labels = {
            "firstname": "First Name",
            "lastname": "Last Name",
            "phone_number": "Mobile Number",
            "email": "email",
            "emg_contact_name": "Contact Name",
            "emg_contact": "Contact Number",
            "room": "Room",
            "security_deposit": "Security Deposit (₹)",
            "adv_rent": "Advance Rent (₹)",
            "notes": "Notes"
        }



        error_messages = {
            "firstname": {
                "required": "First name is required.",
                "max_length": "First name must be 100 characters or fewer.",
            },

            "lastname": {
                "max_length": "Last name must be 100 characters or fewer.",
            },

            "phone_number": {
                "required": "The Mobile Number must be 13 charators",
                "invalid": "Please enter a valid Mobile Number.",
            },

            "email": {
                "required": "Email address is required.",
                "invalid": "Please enter a valid email address.",
                "unique": "A tenant with this email address already exists.",
            },

            "uid": {
                "required": "Aadhaar number is required.",
                "max_length": "Aadhaar number must be 12 characters.",
                "unique": "A tenant with this Aadhaar number already exists.",
            },

            "gender": {
                "required": "Please select a gender.",
                "max_length": "Gender must be 10 characters or fewer.",
            },

            "emg_contact_name": {
                "max_length": "Contact name must be 100 characters or fewer.",
            },

            "emg_contact": {
                "max_length": "Emergency phone number must be 10 digits.",
            },

            "room": {
                "required": "Please select a room.",
            },

            "move_in_date": {
                "required": "Move-in date is required.",
                "invalid": "Please enter a valid date.",
            },

            "security_deposit": {
                "required": "Security deposit is required.",
                "invalid": "Please enter a valid amount.",
                "max_digits": "Security deposit is too large.",
                "max_decimal_places": "Security deposit can have at most 2 decimal places.",
            },

            "adv_rent": {
                "required": "Advance rent is required.",
                "invalid": "Please enter a valid amount.",
                "max_digits": "Advance rent is too large.",
                "max_decimal_places": "Advance rent can have at most 2 decimal places.",
            },

            "notes": {
                "max_length": "Notes must be 1000 characters or fewer.",
            },
        }


class AddressForm(forms.ModelForm):
    pincode = forms.CharField(label="Pincode", max_length=6, validators=[RegexValidator(regex=r"^\d{6}$", message="Pincode must contain exactly 6 digits.")], widget=forms.TextInput(attrs={"placeholder": "XXXXXX"}))
    class Meta:
        model = Address
        fields = "__all__"

        error_messages = {
            "street": {
                "required": "Street name is required.",
                "max_length": "Street name can be 100 charactor or fever"
            },
            "city": {
                "required": "City name is required.",
                "max_length": "City name can be 100 charactor or fever"
            },
            "state": {
                "required": "State name is required.",
                "max_length": "State name can be 100 charactor or fever"
            },
            "pincode": {
                "required": "Pincode is required.",
                "max_length": "Pincode must be 6 digits."
            },
            "country": {
                "required": "Country name is required.",
                "max_length": "Country name can be 100 charactor or fever"
            }
        }


class RoomForm(forms.ModelForm):
    # sharing_type = forms.ChoiceField(label="Sharing Type", choices=[("single","Single"),("double","Double"),("triple","Triple"), ("quadruple","Quadruple")])
    rent = forms.ChoiceField(label="Rent", choices=[("8000","₹8000"), ("9000","₹9000"), ("12000", "₹12000"), ("12500","₹12500")])
    floor = forms.ChoiceField(label="Floor",choices=[(1, "Floor 1"), (2, "Floor 2"), (3, "Floor 3"), (4, "Floor 4"), (5, "Floor 5"), (6, "Floor 6"), (7, "Floor 7"),(8, "Floor 8"),(9, "Floor 9"),(10, "Floor 10")])
    class Meta:
        model = Room

        fields = "__all__"
        labels = {
            "number": "Room Number",
            "sharing_type": "Sharing Type",
            "rent": "Rent",
            "floor": "Floor"
        }

        error_messages = {
            "number": {
                "required": "Room number is required.",
                "max_length": "Room number can be 10 digits or fever"
            },
            "sharing_type": {
                "required": "Sharing type is required.",
            },
            "rent": {
                "rent": "Rent is required."
            },
            "floor": {
                "floor": "Floor is required."
            }
        }