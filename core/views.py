import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from core.forms import EmployeeForm, CustomUserCreationForm
from core.models import Employee, CustomUser


# import requests
# from requests.exceptions import HTTPError

# Index page
def frontpage(request):
    return render(request, 'core/frontpage.html')


# Employee List Page
@login_required(login_url='/login')
def home(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'core/home.html', context)


# Add Employee
@login_required(login_url='/login')
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return redirect('home')
    else:
        form = EmployeeForm()
    context = {'form': form}
    return render(request, 'core/add_employee.html', context)


# Edit Employee
@login_required(login_url='/login')
def edit_employee(request, pk):
    instance = Employee.objects.get(id=pk)
    employee = get_object_or_404(Employee, id=pk)

    if request.method == "GET":
        form = EmployeeForm(instance=instance)
        return render(request, 'core/edit_employee.html', {'form': form, 'employee': employee})
    else:
        form = EmployeeForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return form.errors


# Delete Employee
@login_required(login_url='/login')
def delete_employee(request, pk):
    if request.method == "POST":
        try:
            user = Employee.objects.get(id=pk)
            user.delete()
        except Employee.DoesNotExist:
            messages.error(request, "The user does not exist")

        return redirect('home')

    else:
        return redirect('home')


# Signup
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form = CustomUserCreationForm(request.POST)
            form.save()
            messages.success(request, "You are signed up. you can login now.")
            return redirect("login")
        else:
            return form.errors
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


# Login
def login_user(request):
    if request.POST:

        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect('home')
        elif CustomUser.objects.filter(email=username).exists():
            messages.error(request, "Your email or password is incorrect")
        else:
            messages.error(request, "You are not registered. Please signup first")
        return render(request, 'core/login.html')
    else:
        return render(request, 'core/login.html')



# Logout
def logout_view(request):
    return redirect('frontpage')


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# @login_required(login_url='/login')
def payment_page(request):
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']

    # razorpay_client.utility.verify_webhook_signature(webhook_body, webhook_signature, webhook_secret)

    callback_url = 'callback/'

    # we need to pass these details to frontend.
    context = {'razorpay_order_id': razorpay_order_id, 'razorpay_merchant_key': settings.RAZOR_KEY_ID,
               'razorpay_amount': amount, 'currency': currency, 'callback_url': callback_url}

    return render(request, 'core/payment.html', context=context)
    # return JsonResponse(context)


@csrf_exempt
def callback(request):
    # only accept POST request.
    if request.method == "POST":

        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)

            if result:
                amount = 20000  # Rs. 200
                try:
                    # capture the payment
                    razorpay_client.payment.capture(payment_id, amount)

                    if not razorpay_client:
                        return render(request, 'core/payment_fail.html')

                    else:

                        # render success page on successful capture of payment
                        return JsonResponse(params_dict)
                        # return render(request, 'core/payment_success.html')
                        # else:
                        #     return redirect('payment')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'core/payment_fail.html')
            else:

                # if signature verification fails.
                return render(request, 'core/payment_fail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
