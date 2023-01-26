from django.urls import path, include, reverse
from . import views
from django.views.generic import RedirectView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings






app_name = "Cladexallied"


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login/", views.log_in, name="login"),
    path("sign_up/", views.sign_up, name="signup"),
    path("console/", views.console, name="console"),
    path("logout/", views.log_out, name="logout"),
    path("transfer/", views.transfer, name="transfer"),
    path("settings/", views.settings, name="settings"),
    path("popup/", views.popup, name="popup"),
    path("popup_int/", views.popup_int, name="popup_int"),
    path("terms_and_conditions/", views.t_and_c, name="t_and_c"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("terms_and_services/", views.terms_and_services, name="terms_and_services"),
    path("foreign/", views.foreign_transfer, name="foreign"),
    path("success/", views.success, name="success"),
    path("unsuccessful/", views.unsuccessful, name="unsuccessful"),
    path("history/", views.history, name="history"),
    path("security_pin/", views.security_pin, name="security_pin"),
    path("pin/", views.pin, name="pin"),
    path("card/", views.card, name="card"),
    path("confirmation/", views.confirmation, name="confirmation"),
    path("confirmation_int/", views.confirmation_int, name="confirmation_int"),
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)