from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.forms import EmailAuthenticationForm

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(
        form_class=EmailAuthenticationForm,
        redirect_authenticated_user=True,
        template_name="accounts/login.html"
    ), name="login"),
]
