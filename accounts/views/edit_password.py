from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import re

@login_required(login_url="accounts:signin")
def EditPassword(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password", "")
        password_1 = request.POST.get("password_1", "")
        password_2 = request.POST.get("password_2", "")

        user = request.user

        if user.check_password(old_password):
            if not re.match(r'^[a-zA-Z0-9!@#$%^&*]+$', password_1):
                messages.error(request, 'The use of special characters is not allowed!')
                return redirect('accounts:edit-password')
            elif not password_1 == password_2:
                messages.error(request, 'Password mismatch. Please enter again!')
                return redirect('accounts:edit-password')
            else:
                user.set_password(password_1)
                user.save()
                logout(request)
                messages.success(request, 'You have successfully changed your password and can login again.')
                return redirect('accounts:signin')
        else:
            messages.error(request, 'The password you entered is incorrect')
            return redirect('accounts:edit-password')

    return render(request, 'accounts/edit_password.html')
