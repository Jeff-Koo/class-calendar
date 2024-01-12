from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model

from accounts.forms import SignInForm

User = get_user_model()

class SignInView(View):
    """ User registration view """

    template_name = "accounts/signin.html"
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            emailUsername = forms.cleaned_data["emailUsername"]
            password = forms.cleaned_data["password"]
            
            if '@' in emailUsername:
                email = emailUsername
            else:
                try:
                    user = User.objects.get(username__iexact=emailUsername)
                    email = user.email
                except User.DoesNotExist:
                    email = "None User"

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # messages.error(request, 'USER Does Not Exist!')
                return redirect('accounts:signin')
            
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)
