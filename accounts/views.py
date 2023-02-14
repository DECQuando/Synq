from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model

from .forms import SignUpForm

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
