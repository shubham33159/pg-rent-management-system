from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Room(models.Model):    
    number = models.CharField(max_length=10, null=False, blank=False)
    sharing_type = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(3)], default=2)
    rent = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(100000)])
    floor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    room_state = models.CharField(max_length=100)

    def __str__(self):
        return self.number

class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    country = models.CharField(max_length=100, default="India")

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"
    

class Tenant(models.Model):
    firstname = models.CharField(max_length=100, null=False, blank=False)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    uid = models.CharField(unique=True, max_length=12, blank=False)
    gender = models.CharField(max_length=10)
    status = models.CharField(max_length=100, null=True, blank=False)
    emg_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emg_contact = models.CharField(max_length=10, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=False, blank=False)
    room = models.ForeignKey(Room,on_delete=models.PROTECT, null=False, blank=False)
    move_in_date = models.DateField(auto_now=True,null=False, blank=False)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    adv_rent = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(max_length=1000, blank=True)
    slug = models.SlugField(unique=True)


