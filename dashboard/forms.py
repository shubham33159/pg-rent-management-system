from django import forms

class TenantForm(forms.Form):
    firstname = forms.CharField(label="First Name" ,max_length=100)
    lastname = forms.CharField(label="Last Name" ,max_length=100)
    email = forms.EmailField(label="Email")
    uid = forms.CharField(label="Adhar Number", max_length=100)
    gender = forms.ChoiceField(label="Gender", choices=[("male","Male"), ("female","Female"),])
    status = forms.CharField(label="Status", max_length=100)
    emg_contact_name = forms.CharField(label="Contact Name", max_length=100)
    emg_contact = forms.CharField(label="Emergency Phone", max_length=10)
    move_in_date = forms.DateField(label="Move-In Date")
    security_deposit = forms.DecimalField(label="Security Deposit", max_digits=10, decimal_places=2)
    adv_rent = forms.DecimalField(label="Advance Rent", max_digits=10, decimal_places=2)
    notes = forms.CharField(label="Additional Notes", widget=forms.Textarea, max_length=1000)

class AddressForm(forms.Form):
    street = forms.CharField(label="Street", max_length=100)
    city = forms.CharField(label="City", max_length=100)
    state = forms.CharField(label="State", max_length=100)
    pincode = forms.CharField(label="Pincode", max_length=6)
    country = forms.CharField(label="Country", max_length=100)

class RoomForm(forms.Form):
    number = forms.CharField(label="Room Number", max_length=10)
    sharing_type = forms.IntegerField(label="Sharing Type", min_value=2, max_value=3)
    rent = forms.IntegerField(label="Rent")
    floor = forms.IntegerField(label="Floor", min_value=1, max_value=7)
    room_state = forms.ChoiceField(label="Room State", choices=[("occupied","OCCUPIED"),("vacant","VACANT"),("maintenance","MAINTENANCE")])