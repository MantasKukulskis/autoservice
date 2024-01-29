from django.urls import path
from .views import show_polish, show_chemical, all_customers, add_customer, delete_customer, get_customer,\
    update_customer, add_car, add_unfinished_car_photo, add_finished_car_photo, show_contacts, show_work_pricing, \
    show_finished_jobs_photo, get_received_money, CalendarView, event
from django.conf.urls.static import static
from django.conf import settings

app_name = 'service'

# poliravimo urls
urlpatterns = [
    path("polish/", show_polish, name="show_polish"),
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("calendar/event/", event, name="event"),
    path("add_unfinished_car_photo/", add_unfinished_car_photo, name="add_unfinished_car_photo"),
    path("add_finished_car_photo/<int:customer_id>", add_finished_car_photo, name="add_finished_car_photo"),
]

# cheminio valymo urls
urlpatterns += [
    path("chemical/", show_chemical, name="show_chemical"),
]

# customers urls
urlpatterns += [
    path("customers/", all_customers, name="customers"),
    path("customers/<int:customer_id>", get_customer, name="customer"),
    path("get_received_money", get_received_money, name="get_received_money"),
    path("add_customer/", add_customer, name="add_customer"),
    path("customer/<int:customer_id>/add_car", add_car, name="add_car"),
    # path("<int:add_customer>", add_customer, name='add_customer'),
    path("customers/<int:customer_id>/delete", delete_customer, name='delete_customer'),
    path("customers/<int:customer_id>/update", update_customer, name='update_customer'),
]

# home urls
urlpatterns += [
    path("contacts/", show_contacts, name="show_contacts"),
    path("work_pricing/", show_work_pricing, name="work_pricing"),
    path("finished_jobs_photo/", show_finished_jobs_photo, name="finished_jobs_photo"),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
