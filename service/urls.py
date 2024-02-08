from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import add_customer, delete_customer, get_customer,\
    update_customer, add_car, show_contacts, get_received_money, add_work, update_work, delete_work, \
    show_finished_jobs_photo, CalendarView, event, CustomerListView, PriceListView


app_name = 'service'

# poliravimo urls
urlpatterns = [
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("calendar/event/", event, name="event"),
    path("calendar/event/<int:event_id>/modify", event, name="modify_event"),
]

# customers urls
urlpatterns += [
    path("customers/", CustomerListView.as_view(), name="customers"),
    path("customers/<int:customer_id>", get_customer, name="customer"),
    path("get_received_money", get_received_money, name="get_received_money"),
    path("add_customer/", add_customer, name="add_customer"),
    path("add_work/", add_work, name="add_work"),
    path("customer/<int:customer_id>/add_car", add_car, name="add_car"),
    path("<int:work_id>/delete_work", delete_work, name='delete_work'),
    path("<int:work_id>/update_work", update_work, name='update_work'),
    path("customers/<int:customer_id>/update", update_customer, name='update_customer'),
    path("customers/<int:customer_id>/delete", delete_customer, name='delete_customer'),
]

# home urls
urlpatterns += [
    path("contacts/", show_contacts, name="show_contacts"),
    path("work_pricing/", PriceListView.as_view(), name="work_pricing"),
    path("finished_jobs_photo/", show_finished_jobs_photo, name="finished_jobs_photo"),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
