from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

from random import randint

# Create your models here.

class Customers(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    account_number = models.IntegerField(default=randint(1000000000, 2000000000))
    account_balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class BankTranfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Bank_to_transfer_to = models.CharField(max_length=255, blank=True)
    transfer_amount = models.IntegerField(blank=True)
    transfer_account_number = models.CharField(blank=True, max_length=255)
    account_holder = models.CharField(blank=False, max_length=255)
    account_holder_address = models.CharField(blank=True, max_length=255)
    reason_for_payment = models.CharField(blank=True, max_length=255)
    ref_no = models.IntegerField(verbose_name="Reference no", max_length=8, default=randint(100000, 900000))
    date = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.user.username



class ForeignTransactionInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_holder = models.CharField(blank=True, max_length=255)
    ach_routing = models.IntegerField(blank=True)
    swift_code = models.CharField(blank=True, max_length=255)
    wire_routing = models.IntegerField(blank=True)
    bank_name = models.CharField(blank=True, max_length=255)
    bank_address = models.TextField(blank=True)

    def __str__(self):
        return self.account_holder


class InternationalTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="international_transfer")
    account_holder = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    transfer_amount = models.IntegerField(default=0)
    account_number = models.IntegerField(default=0)
    routing_number = models.CharField(max_length=255)
    bank_address = models.TextField()
    reason_for_payment = models.CharField(blank=True, max_length=255)
    ref_no = models.CharField(verbose_name="Reference no", max_length=8, default=randint(100000, 900000))
    date = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.user.username


class ReceivedFunds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.CharField(blank=True, max_length=255)
    account_number = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    ref_no = models.CharField(verbose_name="Reference no", max_length=8, default=randint(100000, 900000))
    date = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.user.username



class Profile(models.Model):

    

    MARITAL_STATUS = (
        ("NONE", "none"),
        ("SINGLE", "Single"),
        ("MARRIED", "Married")
    )

    ACCOUNT_TYPE = (
        ("PERSONAL", "Personal"),
        ("BUSINESS", "Business"),
        ("CHECKING", "Checking")
    )


    country = CountryField(blank_label="Select country")
    Occupation = models.CharField(max_length=50, default="Business")
    marital_status = models.CharField(max_length=20, verbose_name="Marital status", choices=MARITAL_STATUS, default="NONE")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, default="+")
    account_type = models.CharField(max_length=20, verbose_name="Type of account", choices=ACCOUNT_TYPE, default="PERSONAL")

    def __str__(self):
        return self. user.username
    
class Popup(models.Model):
    code = models.CharField(max_length=10, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Otp(models.Model):
    otp = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"OTP: - {self.otp}"

class SecurityPin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Secure Pin: {self.pin}"

class SavedSecurityPin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_pin = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Saved secure Pin: {self.saved_pin}"




class Contact(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    msg = models.TextField(max_length=255)

    def __str__(self):
        return self.name


