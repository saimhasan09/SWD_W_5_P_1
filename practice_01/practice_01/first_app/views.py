from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate,login, logout, update_session_auth_hash
from django.contrib import messages

# Create your views here.


# home page
def home(request):
    return render(request, './home.html')



# signup page
def signup(request ):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully')
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, './signup.html', {'form': form})


# login page
def user_login(request):
    if request.user is not authenticate:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data= request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                userpass = form.cleaned_data['password']
                user = authenticate(username= name, password= userpass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                    return redirect('profile')
        else:
            form = AuthenticationForm()
        return render(request, './login.html', {'form':form})
    return redirect('profile')


# profile page
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('login')
            
# logout
def user_logout(request):
    logout(request)
    messages.success(request, 'User has been logged out successfully')
    return redirect('homepage')


# password change form with old password
def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user = request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = PasswordChangeForm(user = request.user)
        return render(request, './passchange.html', {'form': form})
    else:
        return redirect('login')


# password change without old password
def pass_change2(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user= request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request, './passchange.html', {'form': form})
    else:
        return redirect('login')
