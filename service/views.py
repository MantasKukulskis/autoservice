from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CustomerForm, EventForm, WorkPricingForm
from .models import Customer, Car, Event, WorkPricing
from django.forms import modelform_factory
from datetime import datetime, date, timedelta
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
from django.urls import reverse
import calendar


def index(request):
    return HttpResponse(request, "service html")


def show_polish(request):
    return render(request, 'service/polish.html')


def show_contacts(request):
    return render(request, 'service/contacts.html')


def show_finished_jobs_photo(request):
    return render(request, 'service/finished_jobs_photo.html')


def show_chemical(request):
    return render(request, 'service/chemical.html')


def all_customers(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'service/customers.html', context)


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("service:customers")
    else:
        form = CustomerForm()
    context = {'form': form}
    return render(request, 'service/add_customer.html', context)


def delete_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect("service:customers")
    context = {'customer': customer}
    return render(request, "service/delete_customer.html", context)


def get_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    cars = Car.objects.filter(customer=customer)
    money = Event.objects.filter(customer=customer)
    money = sum(m.received_money for m in money)
    context = {
        'customer': customer,
        'cars': cars,
        'money': money,
    }
    return render(request, 'service/customer.html', context)


def update_customer(request, customer_id):
    instance = Customer.objects.get(pk=customer_id)
    form = CustomerForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("service:customer", customer_id=customer_id)
    return render(request, "service/update_customer.html", {'form': form})


def add_car(request, customer_id):
    AuthorFormSet = modelform_factory(Car, fields=('car', 'model', 'color', 'license_plate'))
    if request.method == "POST":
        form = AuthorFormSet(request.POST)
        if form.is_valid():
            car = Car(
                car=form.cleaned_data['car'],
                model=form.cleaned_data['model'],
                color=form.cleaned_data['color'],
                license_plate=form.cleaned_data['license_plate'],
                customer=Customer.objects.get(pk=customer_id),

            )
            car.save()
            return redirect("service:customer", customer_id)
    form = AuthorFormSet()
    context = {"form": form}
    return render(request, "service/add_car.html", context)


# def add_unfinished_car_photo(request):
#     if request.method == "POST":
#         form = UnfinishedCarPhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("service:customers")
#         else:
#             context = {'form': form}
#             return render(request, "service/add_unfinished_car_photo.html", context)
#     context = {"form": UnfinishedCarPhotoForm()}
#     return render(request, "service/add_unfinished_car_photo.html", context)
#
#
# def add_finished_car_photo(request, customer_id):
#     new = FinishedCarPhotoForm()
#     if request.method == "POST":
#         new = FinishedCarPhotoForm(request.POST, request.FILES)
#         if new.is_valid():
#             new.save()
#             return redirect("service:customers")
#     form = new
#     context = {'form': form, 'customer_id': customer_id}
#     return render(request, "service/add_finished_car_photo.html", context)
#
#
def get_received_money(request):
    money = Event.objects.all()
    result = {}
    for m in money:
        customer = m.customer
        suma = m.received_money
        if customer in result.keys():
            result[customer]['received_money'] += suma
        else:
            result[customer] = {'received_money': suma}
    context = {'result': result}

    return render(request, 'service/get_received_money.html', context)


class CalendarView(generic.ListView):
    model = Event
    template_name = 'service/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('service:calendar'))
    return render(request, 'service/event.html', {'form': form})


def work_pricing(request):
    price = WorkPricing.objects.all()
    context = {'price': price, 'work_id': 1}
    return render(request, 'service/work_pricing.html', context)


def add_work(request):
    if request.method == 'POST':
        form = WorkPricingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("service:work_pricing")
    else:
        form = WorkPricingForm()
    context = {'form': form}
    return render(request, 'service/add_work.html', context)


def update_work(request, work_id):
    instance = WorkPricing.objects.get(pk=work_id)
    form = WorkPricingForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("service:work_pricing")
    context = {'form': form}
    return render(request, "service/update_work.html", context=context)


def delete_work(request, work_id):
    work = WorkPricing.objects.get(pk=work_id)
    if request.method == 'POST':
        work.delete()
        return redirect("service:work_pricing")
    context = {'work': work}
    return render(request, "service/delete_work.html", context)
