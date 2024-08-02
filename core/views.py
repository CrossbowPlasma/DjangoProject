from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from .forms import SignUpform, CustomAuthenticationForm

# Home
def home(request):
    return render(request, 'core/home.html')

# Signup
def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpform(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created!')
        else:
            form = SignUpform()
        
        return render(request, 'core/signup.html', {'form': form})
    else:
        return redirect('profile', username  = request.user.username)

# Login
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomAuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                remember_me = form.cleaned_data.get('remember_me', False)
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    if remember_me:
                        saved_users = request.session.get('saved_users', [])
                        if [uname,upass] not in saved_users:
                            saved_users.append([uname,upass])
                            request.session['saved_users'] = saved_users
                    login(request, user)
                    messages.success(request, 'Logged in!')
                    return redirect('profile', username=request.user.username)
        else:
            form = CustomAuthenticationForm()
        
        return render(request, 'core/login.html', {'form': form})
    else:
        return redirect('profile', username  = request.user.username)

# Profile
def profile(request, username):
    if request.user.is_authenticated and request.user.username == username:
        form = UserChangeForm(instance=request.user)
        return render(request, 'core/profile.html', {'username':request.user.username, 'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
# Change Password
def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Password changed!")
                return redirect('profile', username  = request.user.username)
        else:
            form = PasswordChangeForm(user=request)

        return render(request, 'core/change_password.html', {'username':request.user.username, 'form':form})
    else:
        return HttpResponseRedirect('/login/')
    
# Switch User
def switch_user(request):
    if request.user.is_authenticated:
        saved_users = [user for user in request.session.get('saved_users', []) if user[0] != request.user.username]
        return render(request, 'core/switchuser.html', {'username':request.user.username, 'saved_users':saved_users})
    else:
        return HttpResponseRedirect('/login/')

# Restore User
def restore_user(request, uname,upass):
    saved_users = request.session.get('saved_users', [])
    if request.user.is_authenticated and [uname,upass] in saved_users:
        logout(request)
        request.session['saved_users'] = saved_users
        user = authenticate(username=uname, password=upass)
        login(request, user)
        messages.success(request, 'Logged in!')
        return redirect('profile', username=request.user.username)
    else:
        return HttpResponseRedirect('/login/')

# Logout and redirect
def logout_and_redirect(request, redirect_url):
    saved_users = request.session.get('saved_users', [])
    logout(request)
    request.session['saved_users'] = saved_users
    return redirect(redirect_url)