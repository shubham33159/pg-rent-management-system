from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


# Create your models here.
class Room(models.Model):    
    number = models.CharField(max_length=10, null=False, blank=False)
    sharing_type = models.CharField(max_length=10)
    rent = models.CharField(max_length=100000)
    floor = models.CharField(max_length=50)

    def __str__(self):
        return f"Room {self.number}•{self.sharing_type}•₹{self.rent}/mo"

class Address(models.Model):
    street = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    pincode = models.CharField(max_length=6, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False, default="India")

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"
    

class Tenant(models.Model):
    firstname = models.CharField(max_length=100, null=False, blank=False)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    uid = models.CharField(unique=True, max_length=12, blank=False)
    gender = models.CharField(max_length=10)
    status = models.CharField(max_length=100, null=False, blank=False, default="Active")
    emg_contact_name = models.CharField(max_length=100, null=False, blank=False)
    emg_contact = models.CharField(max_length=10, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=False, blank=False)
    room = models.ForeignKey(Room,on_delete=models.PROTECT, null=False, blank=False)
    move_in_date = models.DateField(null=False, blank=False)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    adv_rent = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(max_length=1000, blank=True)
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False)


    # def __str__(self):
    #     return f"{self.firstname} {self.lastname}"
    
