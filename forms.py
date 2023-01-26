
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, BankTranfer, Popup, Contact, InternationalTransaction, SecurityPin
from django.contrib.auth.models import User




class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", 
                    "last_name", "email",
                    "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user



class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = (
            "country",
            "Occupation", 
            "phone_number", 
            "marital_status",
            "account_type"
            )



class TransferForm(forms.ModelForm):

    class Meta:
        model = BankTranfer
        fields = (
            "Bank_to_transfer_to",
            "transfer_amount",
            "transfer_account_number",
            "account_holder",
            "account_holder_address",
            "reason_for_payment",
        )


class InternationalTransferForm(forms.ModelForm):

    class Meta:

        model = InternationalTransaction

        fields = (
            "bank_name",
            "account_holder",
            "transfer_amount",
            "account_number",
            "routing_number",
            "bank_address",
            "reason_for_payment"
        )        


class PopupForm(forms.ModelForm):

    class Meta:
        model = Popup
        fields = ("code",)



class SecurityPinForm(forms.ModelForm):

    class Meta:
        model = SecurityPin
        fields = ("pin",)


# class ChangePinForm(forms.ModelForm):
#     class Meta:
#         model = SavedSecurityPin
#         fields = ("old_pin"," new_pin", "confirm_pin")

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "phone_number", "email", "msg")
        