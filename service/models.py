from django.db import models
from django.utils.timezone import now
from django.urls import reverse
import datetime


class BaseModel(models.Model):
    objects = models.Model
    DoesNotExist = models.Model

    class Meta:
        abstract = True


class Customer(BaseModel):
    name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    phone_number = models.IntegerField(blank=False)
    email_address = models.EmailField(blank=True)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Car(BaseModel):
    car = models.CharField(max_length=20, blank=False)
    pub_date = models.DateTimeField(default=now)
    model = models.CharField(max_length=20, blank=False)
    color = models.CharField(max_length=10, blank=False)
    license_plate = models.CharField(max_length=8, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car} {self.model}'

    def was_published_recently(self):
        return self.pub_date >= now() - datetime.timedelta(days=1)


class Service(BaseModel):
    service = models.CharField(max_length=20, blank=False)
    price = models.IntegerField(blank=False)
    time = models.IntegerField(blank=False)


class Employer(BaseModel):
    name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    phone_number = models.IntegerField(blank=False)
    email_address = models.EmailField(blank=True)
    address = models.CharField(max_length=30, blank=False)


class Jobs(BaseModel):
    job_status = {
        'IN_PROGRESS': 'in_progress',
        'FINISHED': 'finished',
        'UNFINISHED': 'unfinished',
    }
    # employer = None
    # jobs = models.Mul
    working_hours = models.IntegerField(blank=False)
    total_amount = models.FloatField(blank=False)
    finished_work_photo = models.ImageField(blank=False)
    before_work_photo = models.ImageField(blank=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)


class WorkPricing(BaseModel):
    work = models.CharField(max_length=50)
    prise_of_work = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f' {self.work} € {self.prise_of_work}'


class Event(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    works_and_prices = models.ManyToManyField(WorkPricing)
    photo_before = models.ImageField(blank=True, upload_to='before/')
    photo_after = models.ImageField(blank=True, upload_to='after/')
    received_money = models.IntegerField(blank=False)

    @property
    def get_html_url(self):
        url = reverse('service:modify_event', args=(self.id,))
        return f'<a href="{url}">{self.title}</a>'


class Login(BaseModel):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class Register(BaseModel):
    Vartotojas = models.CharField(max_length=20, blank=False)
    Slaptažodis = models.CharField(max_length=20, blank=False)
