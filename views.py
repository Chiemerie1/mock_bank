
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from mock_bank.forms import (PopupForm, RegistrationForm, 
                    ProfileForm, SecurityPinForm, TransferForm, 
                    BankTranfer, ContactForm,
                    InternationalTransferForm,
                    
    )
from django.contrib.auth.forms import AuthenticationForm
from .models import Customers, Profile, Popup, ForeignTransactionInfo, InternationalTransaction, ReceivedFunds, Otp, SavedSecurityPin, SecurityPin



def sign_up(request):
    sign_up_form = RegistrationForm(request.POST)
    if request.method == "POST":
        if sign_up_form.is_valid():
            new_user =  sign_up_form.save()
            username = sign_up_form.cleaned_data.get("username")
            login(request, new_user)
            customer = Customers.objects.create(user_id=request.user.id)
            profile = Profile.objects.create(user_id=request.user.id)
            popup = Popup.objects.create(user_id=request.user.id)
            foreign =  InternationalTransaction.objects.create(user_id=request.user.id)

            received = ReceivedFunds.objects.create(user_id=request.user.id)
            return redirect("Cladexallied:console")
        else:
            for msg in sign_up_form.error_messages:
                messages.error(request, sign_up_form.error_messages[msg])
        
    return render(request=request,  template_name="Cladexallied/sign_up.html",
                context={
                    "signup": sign_up_form,
                }
            )



def log_in(request):
    user = request.user
    if user.is_authenticated:
        return redirect("Cladexallied:console")
    login_form = AuthenticationForm(request, data=request.POST)
    if request.method =="POST":
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user != None:
                login(request, user)
                return redirect("Cladexallied:security_pin")
            else:
                messages.error(request, "Wrong login credentials. Please enter a correct credential to access your dashboard")
            
        if not user.is_active:
            messages.info(request, "Your account has been temporarily locked due to suspicious activities detected from your IP address. Please contact us: Cladexalliedbank@email.com")

    return render(request=request, template_name="Cladexallied/login.html",
                    context={"signin": login_form})


def log_out(request):
    logout(request)
    return redirect("Cladexallied:homepage")


def homepage(request):
    return render(request=request, template_name="Cladexallied/homepage.html")


def console(request):

    balance = Customers.objects.get(user=request.user)
    balance


    return render(request=request, template_name="Cladexallied/console.html", 
                    context={
                        "profile": Profile.objects.all().filter(user=request.user),
                        "customer": Customers.objects.all().filter(user=request.user),
                    }
                )


def transfer(request):

    if request.method =="POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["transfer_amount"]
            customer = Customers.objects.get(user=request.user)
            customer.account_balance -= amount
            customer.save()
            _form = form.save(commit=False)
            _form.user = request.user
            _form.save()
            return redirect("Cladexallied:popup")
        else:
           return redirect("Cladexallied:unsuccessful")
    else:
        form = TransferForm()
    return render(request=request, template_name="Cladexallied/transfer.html",
                    context={
                        "transfer": form,
                        "bank_transfer": BankTranfer.objects.all().filter(user=request.user),
                        "customer": Customers.objects.all().filter(user=request.user),
                        "received": ReceivedFunds.objects.all().filter(user=request.user)
                    }
                )


def history(request):
    return render(
        request=request, template_name="Cladexallied/history.html",
        context={
            "bank_transfer": BankTranfer.objects.all().filter(user=request.user).order_by("-date"),
            "received": ReceivedFunds.objects.all().filter(user=request.user).order_by("-date"),
            "foreign": InternationalTransaction.objects.all().filter(user=request.user).order_by("-date")
        }
    )





def settings(request):
    #Updating user profile
    try:
        profile = request.user.profile
    except:
        profile = Profile()
        profile.user = request.user
        profile.save()
    form = ProfileForm(request.POST, instance=profile)
    if form.is_valid():
        _form = form.save(commit=False)
        _form.user = request.user
        _form.save()
        messages.success(request, "Profile updated successfully")


    form = ProfileForm()
    

    return render(request=request, template_name="Cladexallied/settings.html",
                    context={"settings": form,
                        "customer": Customers.objects.all().filter(user=request.user),
                        "profile": Profile.objects.all().filter(user=request.user),
                    }
                )


def popup(request):
    try:
        popup = request.user.popup
    except:
        popup = Popup()
        popup.user = request.user
        popup.save()
    form = PopupForm(request.POST, instance=popup)
    if form.is_valid():
        entered_otp = form.cleaned_data["code"]
        _form = form.save(commit=False)

        _form.user = request.user

        obj = Otp.objects.last()
        get_field = Otp._meta.get_field("otp")
        _otp = get_field.value_from_object(obj)

        if _otp == entered_otp:
            _form.save()
        else:
            refund = BankTranfer.objects.last()
            get_refund_field = BankTranfer._meta.get_field("transfer_amount")
            _refund = get_refund_field.value_from_object(refund)
            
            customer = Customers.objects.get(user=request.user)
            customer.save()

            BankTranfer.objects.order_by("-pk")[0].delete()
            return redirect("Cladexallied:unsuccessful")
        return redirect("Cladexallied:confirmation")
        

    form = PopupForm()
    

    return render(request=request, template_name="Cladexallied/popup.html",
                    context={
                        "popup": form,
                        "popup": Popup.objects.all().filter(user=request.user),
                        "bank_transfer": BankTranfer.objects.all().filter(user=request.user),
                        "customer": Customers.objects.all().filter(user=request.user),
                        "received": ReceivedFunds.objects.all().filter(user=request.user)
                        
                        })



def popup_int(request):
    try:
        popup = request.user.popup
    except:
        popup = Popup()
        popup.user = request.user
        popup.save()
    form = PopupForm(request.POST, instance=popup)
    if form.is_valid():
        entered_otp = form.cleaned_data["code"]
        _form = form.save(commit=False)

        _form.user = request.user

        obj = Otp.objects.last()
        get_field = Otp._meta.get_field("otp")
        _otp = get_field.value_from_object(obj)

        if _otp == entered_otp:
            _form.save()
        else:
            refund = InternationalTransaction.objects.last()
            get_refund_field = InternationalTransaction._meta.get_field("transfer_amount")
            _refund = get_refund_field.value_from_object(refund)
            
            customer = Customers.objects.get(user=request.user)
            customer.account_balance += _refund
            customer.save()

            InternationalTransaction.objects.order_by("-pk")[0].delete()
            return redirect("Cladexallied:unsuccessful")
        return redirect("Cladexallied:confirmation_int")
        

    form = PopupForm()
    

    return render(request=request, template_name="Cladexallied/popup.html",
                    context={
                        "popup": form,
                        "popup": Popup.objects.all().filter(user=request.user),
                        "bank_transfer": InternationalTransaction.objects.all().filter(user=request.user),
                        "customer": Customers.objects.all().filter(user=request.user),
                        "received": ReceivedFunds.objects.all().filter(user=request.user)
                        
                        })



def security_pin(request):

    if request.method == "POST":
        form = SecurityPinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data["pin"]
            form.save(commit=False)

            obj = SavedSecurityPin.objects.last()
            get_field = SavedSecurityPin._meta.get_field("saved_pin")
            _saved_pin = get_field.value_from_object(obj)

            if _saved_pin == pin:
                return redirect("Cladexallied:console")

            else:
                messages.info(request, "Incorrect pin")
                logout(request)
                return redirect("Cladexallied:login")
        elif form.is_valid == False:
            logout(request)
        

    form = SecurityPinForm()
    

    return render(request=request, template_name="Cladexallied/security.html",
                    context={
                        "form": form,
                        "security_pin": SecurityPin.objects.all(),
                        
                        })


def change_pin(request):


    if request.method == "POST":
        form = ChangePinForm(request.POST)
        old_pin = form.cleaned_data["old_pin"]
        new_pin = form.cleaned_data["new_pin"]
        confirm_pin = form.cleaned_data["confirm_pin"]

       

        sspin = SavedSecurityPin.object.get(user=request.user)

        print(old_pin)
        print(new_pin)
        print(confirm_pin)

        # if old_pin == _saved_pin and new_pin == confirm_pin:
        #     print("saved pin: {sspin.saved_pin}")
        #     print("confirm pin: {confirm_pin}")
        #     sspin.saved_pin = confirm_pin
        #     sspin.save()

    form = ChangePinForm()
    
    return render(
        request=request, template_name="Cladexallied/pin.html",
        context={
            "form": form,
        }
    )


            

def t_and_c(request):
    return render(
        request=request, template_name="Cladexallied/terms_and_conditions.html",

    )

def foreign_transfer(request):

    if request.method =="POST":
        form = InternationalTransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["transfer_amount"]
            customer_bal = Customers.objects.get(user=request.user)
            customer_bal.account_balance -= amount
            customer_bal.save()            
            _form = form.save(commit=False)
            _form.user = request.user
            _form.save()
            return redirect("Cladexallied:popup_int")
        else:
            return redirect("Cladexallied:unsuccessful")
    else:
        form = InternationalTransferForm()
        
    return render(
        request=request, template_name='Cladexallied/foreign_transfer.html',
        context={
            "form":form,
            "information": ForeignTransactionInfo.objects.all().filter(user=request.user),
            "received": ReceivedFunds.objects.all().filter(user=request.user),
            "customer": Customers.objects.all().filter(user=request.user),
            "foreign": InternationalTransaction.objects.all().filter(user=request.user)
        }
    )



def terms_and_services(request):
    return render(
        request=request, template_name="Cladexallied/terms_and_services.html",

    )

def about(request):
    return render(
        request=request, template_name="Cladexallied/about.html",
    )


def success(request):
    return render(
        request=request, template_name="Cladexallied/success.html",
    )

def unsuccessful(request):
    return render(
        request=request, template_name="Cladexallied/unsuccessful.html",
    )


def pin(request):

    return render(
        request=request, template_name="Cladexallied/pin.html",
    )


def card(request):
    return render(
        request=request, template_name="Cladexallied/card.html",
    )


def confirmation(request):
    return render(
        request=request, template_name="Cladexallied/confirmation.html",
         context={
            "bank_transfer": BankTranfer.objects.all().filter(user=request.user).order_by("-date")
        }
    )


def confirmation_int(request):
    return render(
        request=request, template_name="Cladexallied/confirmation_int.html",
         context={
            "foreign": InternationalTransaction.objects.all().filter(user=request.user).order_by("-date"),
        }
    )

def contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "message sent")
    else:
        form = ContactForm()
    return render(
        request=request, template_name="Cladexallied/contact.html",
        context={
            "contact": form,

        }
    )




