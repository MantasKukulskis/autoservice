import datetime

from django import forms
from django.forms import ModelForm, DateInput
from django.forms import modelform_factory

from service.models import Car, Service, Employer, Customer, Jobs, UnfinishedCarPhoto, FinishedCarPhoto, Event

# CarForm = modelform_factory(Car, fields=('car', 'model', 'color', 'license_plate', 'customer'))


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car', 'model', 'color', 'license_plate']

    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        self.fields['user_defined_code'] = forms.ModelChoiceField(queryset=Customer.objects.all())


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service', 'price', 'time']


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['name', 'last_name', 'phone_number', 'email_address', 'address']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'last_name', 'phone_number', 'email_address']


# class JobsForm(forms.ModelForm):
#     class Meta:
#         model = Jobs
#         fields = ['job_status', 'employer', 'jobs', 'working_hours', 'total_amount', 'finished_work_photo',
#                   'before_work_photo']


class UnfinishedCarPhotoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.publication_date = datetime.date.today()

    class Meta:
        model = UnfinishedCarPhoto
        exclude = ['publication_date']
        fields = ['car_photo', 'descripcion', 'publication_date']


class FinishedCarPhotoForm(forms.ModelForm):

    class Meta:
        model = FinishedCarPhoto
        exclude = ['publication_date']
        fields = "__all__"


class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
          'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

