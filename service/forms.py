from django import forms
from django.forms import ModelForm, DateInput, ValidationError
from service.models import Car, Service, Employer, Customer, Event, WorkPricing, Login, Register


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


class EventForm(ModelForm):
    class Meta:
        works_and_prices = forms.ModelMultipleChoiceField(queryset=WorkPricing.objects.all().order_by('work'),
                                                          label="WorkPricing", widget=forms.CheckboxSelectMultiple,
                                                          blank=True)
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


class WorkPricingForm(ModelForm):
    class Meta:
        model = WorkPricing
        fields = '__all__'


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)

    class Meta:
        model = Login
        fields = '__all__'


class PasswordChangeForm(ModelForm):
    new_password = forms.CharField(max_length=30)

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if len(new_password) < 8:
            raise ValidationError("Slaptažodis negali būti trumpesnis, nei 8 simboliai")
        if new_password.isalpha() or new_password.isnumeric():
            raise ValidationError("Slaptažodis turi turėti skaičius ir raides")
        return new_password


class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Register
        fields = '__all__'
