
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Employee
from datetime import date
from datetime import datetime


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        logged_in_employee_zipcode = logged_in_employee.zip_code
        Customer = apps.get_model('customers.Customer')
        todays_customers = Customer.objects.filter(zip_code=logged_in_employee_zipcode)
        #customer_day = todays_customers.filter(weekly_pickup=today)
        #non_suspended_customer = customer_day.exclude(suspended_account=today)
        #customer_pick_up_due = non_suspended_customer.exclude(todays_pickups=confirmed)
        context = {
            'todays_customers': todays_customers
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))


def determine_day():
    today2 = date.today()
    today = today2.weekday()
    if today == 0:
        return "Monday"
    elif today == 1:
        return "Tuesday"
    elif today == 2:
        return "Wednesday"
    elif today == 3:
        return "Thursday"
    elif today == 4:
        return "Friday"
    elif today == 5:
        return "Saturday"
    elif today == 6:
        return "Sunday"

def confirm_pickup(request, customer_id):
    try:
        Customer = apps.get_model('customers.Customer')
        customer_to_update = Customer.objects.get(id=customer_id)
        customer_to_update.balance += 20
        customer_to_update.date_of_last_pickup = date.today()
        customer_to_update.save()

        return render(request, 'employees/index.html')

    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))







def view_schedule(request, weekday):
       Customer = apps.get_model('customers.Customer')
       pickup_day = Customer.objects.filter()


@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user,
                                address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')


@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zipcode')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)
