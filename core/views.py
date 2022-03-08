from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from core.forms import EmployeeForm, CustomUserCreationForm
from core.models import Employee, CustomUser


def frontpage(request):
    return render(request, 'core/frontpage.html')


@login_required(login_url='/login')
def home(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'core/home.html', context)


@login_required(login_url='/login')
def add_employee(request):
    form = EmployeeForm()
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return HttpResponse("Form is not valid")
            return redirect('home')
    else:
        form = EmployeeForm()
    context = {'form': form}
    return render(request, 'core/add_employee.html', context)


@login_required(login_url='/login')
def edit_employee(request, id):
    instance = Employee.objects.get(id=id)
    employee = get_object_or_404(Employee, id=id)
    form = EmployeeForm()
    if request.method == "GET":
        form = EmployeeForm(instance=instance)
        return render(request, 'core/edit_employee.html', {'form': form, 'employee': employee})
    else:
        form = EmployeeForm(request.POST, instance=instance)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            return redirect('home')
        else:
            print("not saved")


@login_required(login_url='/login')
def delete_employee(request, id):
    user = Employee.objects.get(id=id)
    user.delete()
    return redirect('home')


# Signup
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form = CustomUserCreationForm(request.POST)
            user = form.save(commit=False)
            user.save()
            # current_site = get_current_site(request)

            messages.success(request, "You are signed up. you can login now.")
            return redirect("login")

    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


def login(request):
    logout(request)
    username = password = ''
    if request.POST:

        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect('home')
        elif CustomUser.objects.filter(email=username):
            messages.error(request, "Your email or password is incorrect")
        else:
            messages.error(request, "You are not registered. Please signup first")
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('frontpage')
