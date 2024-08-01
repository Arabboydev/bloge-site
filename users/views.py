from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from users import models
from users import forms
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class RegisterView(View):
    def get(self, request):
        registration_form = forms.RegistrationForm()
        context = {
            'form': registration_form
        }
        return render(request, 'register.html', context=context)

    def post(self, request):
        registration_form = forms.RegistrationForm(data=request.POST, files=request.FILES)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': registration_form
            }
            return render(request, 'register.html', context=context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'form': login_form
        }
        return render(request, 'login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('blogs:home')
        else:
            context = {
                'form': login_form
            }
            return render(request, 'login.html', context=context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('blogs:home')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        update_form = forms.EditMyProfileForm(instance=request.user)
        context = {'form': update_form}
        return render(request, 'profile_edit.html', context=context)

    def post(self, request):
        update_form = forms.EditMyProfileForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('users:profile')
        else:
            context = {'form': update_form}
            return render(request, 'profile_edit.html', context=context)
