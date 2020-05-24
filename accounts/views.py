from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm
from movies.models import Genre

User = get_user_model()

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:home')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.add_message(request, messages.INFO, 'Welcome '+user.username +'!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def preference(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST.getlist(''))
        if form.is_valid():
            profile = form.save()
            messages.add_message(request, messages.INFO, 'Thank you for letting us know!')
            return redirect('home')
        else:
            print('what ..', form)
    else:
        form = UserProfileForm()
    genres = Genre.objects.all()
    context = {
        'form':form,
        'genres': genres
    }
    return render(request, 'accounts/preference.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.add_message(request, messages.INFO, "You've been successfully logged in")
            return redirect(request.GET.get('next') or 'home')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)



@login_required
def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, "You've been logged out.")
    return redirect('home')


def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context ={
        'form':form
    }
    return render(request, 'accounts/update.html', context)


@require_POST
@login_required
def delete(request):
    request.user.delete()
    messages.add_message(request, messages.ERROR, "Your account has been deleted.")
    return redirect('home')

def profile(request, username):
    #해당 유저 (username)의 정보를 보여줌
    person = get_object_or_404(User, username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)
