from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.forms import modelform_factory
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
import calendar
from datetime import datetime, date, timedelta
from .forms import CustomerForm, EventForm, WorkPricingForm
from .models import Customer, Car, Event, WorkPricing
from .utils import Calendar


def index(request):
    return HttpResponse(request, "service html")


def show_contacts(request):
    return render(request, 'service/contacts.html')


def show_finished_jobs_photo(request):
    photos = Event.objects.order_by('-id')[:10]
    return render(request, 'service/finished_jobs_photo.html', {'photos': photos})


@login_required
def all_customers(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 15)
    page_number = request.GET.get("page", 1)
    page_object = paginator.get_page(page_number)
    return render(request, 'service/customers.html', {"page_object": page_object})


class CustomerListView(ListView):
    paginate_by = 15
    model = Customer


@login_required
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


@login_required
def delete_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect("service:customers")
    context = {'customer': customer}
    return render(request, "service/delete_customer.html", context)


@login_required
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


@login_required
def update_customer(request, customer_id):
    instance = Customer.objects.get(pk=customer_id)
    form = CustomerForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("service:customer", customer_id=customer_id)
    return render(request, "service/update_customer.html", {'form': form})


@login_required
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


@login_required
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
    final_result = [{key: value} for key, value in result.items()]
    paginator = Paginator(final_result, 15)
    page_number = request.GET.get("page", 1)
    page_object = paginator.get_page(page_number)

    return render(request, 'service/get_received_money.html', {"page_obj": page_object})


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
    form = EventForm(request.POST or None, request.FILES or None, instance=instance)
    if request.POST and form.is_valid():
        if form.cleaned_data['end_time'] > form.cleaned_data['start_time']:
            form.save()
        else:
            messages.error(request, 'Darbų pabaigos diena negali būti ankstesnė už darbų pradžios datą')
            return redirect('service:event')

        return HttpResponseRedirect(reverse('service:calendar'))
    return render(request, 'service/event.html', {'form': form})


def work_pricing(request):
    price = WorkPricing.objects.all()
    paginator = Paginator(price, 15)
    page_number = request.GET.get("page", 1)
    page_object = paginator.get_page(page_number)
    return render(request, 'service/work_pricing.html', {"page_obj": page_object})


class PriceListView(ListView):
    paginate_by = 15
    model = WorkPricing


@login_required
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


@login_required
def update_work(request, work_id):
    instance = WorkPricing.objects.get(pk=work_id)
    form = WorkPricingForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect("service:work_pricing")
    context = {'form': form}
    return render(request, "service/update_work.html", context=context)


@login_required
def delete_work(request, work_id):
    work = WorkPricing.objects.get(pk=work_id)
    # work = get_object_or_404(WorkPricing, pk=work_id)
    if request.method == 'POST':
        work.delete()
        return redirect("service:work_pricing")
    context = {'work': work}
    return render(request, "service/delete_work.html", context)
