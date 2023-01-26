from django.contrib import admin
from .models import (
    Profile, 
    Customers, 
    BankTranfer, 
    Popup, 
    Contact, 
    ForeignTransactionInfo,
    InternationalTransaction,
    ReceivedFunds,
    Otp,
    SavedSecurityPin
    ) 


# Register your models here.

admin.site.site_header = "Cladexallied Admin panel"
admin.site.site_title = "Welcome to Cladexallied Bank"
admin.site.index_title = "Cladexallied Bank"



class CustomersAdmin(admin.ModelAdmin):
    list_display = ("user", "account_number", "account_balance")



class LocalTranferAdmin(admin.ModelAdmin):
    list_display = ("user", "transfer_amount", "reason_for_payment", "ref_no")
    


class ReceivedFundsAdmin(admin.ModelAdmin):
    list_display = ("user", "from_account", "amount")


admin.site.register(Customers, CustomersAdmin)
admin.site.register(Profile)
admin.site.register(BankTranfer, LocalTranferAdmin)
admin.site.register(Popup)
admin.site.register(Contact)
admin.site.register(ForeignTransactionInfo)
admin.site.register(InternationalTransaction)
admin.site.register(ReceivedFunds, ReceivedFundsAdmin)
admin.site.register(Otp)
admin.site.register(SavedSecurityPin)