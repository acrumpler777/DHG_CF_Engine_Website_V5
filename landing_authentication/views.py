from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
def handler404(request, exception):
    context = {}
    response = render(request, "landing_authentication/404.html", context=context)
    response.status_code = 404
    return response

def handler500(request):
    context = {}
    response = render(request, "landing_authentication/500.html", context=context)
    response.status_code = 500
    return response


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username and/or password is incorrect')

    context = {}
    return render(request, 'landing_authentication/login.html', context)


def logoutUser(request):
    logout(request)
    context = {}
    return render(request, 'landing_authentication/logout.html', context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #print(form)
        #print(form['first_name'].value())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('login')

        context = {'form': form}
        return render(request, 'landing_authentication/register.html', context)
    else:
        form = SignUpForm()
        context = {'form':form}
        return render(request, 'landing_authentication/register.html', context)


def landing(request):
    context = {}
    return render(request, 'landing_authentication/landing.html', context)


@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'landing_authentication/home.html', context)
