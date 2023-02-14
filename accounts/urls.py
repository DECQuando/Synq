from django.contrib.auth.views import LoginView
from django.urls import path

from .views import SignUpView
from accounts.forms import EmailAuthenticationForm

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(
        form_class=EmailAuthenticationForm,
        redirect_authenticated_user=True,
        template_name="accounts/login.html"
    ), name="login"),
    path('signup/', SignUpView.as_view(), name='signup'),
]
