from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model, login, authenticate

from .forms import SignUpForm

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('synqapp:welcome')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return response
