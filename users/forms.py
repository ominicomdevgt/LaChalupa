from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from bootstrap_datepicker_plus import DatePickerInput
from django.forms import ValidationError
from registration.models import Country, City
from django.contrib.auth.forms import PasswordResetForm


class LogingForm(forms.ModelForm):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','password']
    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("username")
        password = cleaned_data.get("password")
        # Don't forget to return the cleaned_data after everything
        return cleaned_data
class UserRegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Tu contraseña no es la misma",
    }
    username = forms.EmailField(label='Correo Electrónico')
    first_name = forms.CharField(label='Nombre Completo')
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput(),
        help_text="""
                    - Tu Contraseña debe de ser mayor a 8 caracteres <br>
                    - Tu contraseña no puede ser solamente numérica <br>
                    - Tu contraseña debe tener una letra mayúscula, un número y un símbolo 
        """,
    )
    password2 = forms.CharField(label='Confirmar Contraseña',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','first_name','password1','password2']
        help_texts = {
            "password1": "Debes ingresar una cédula válida",
            'username': 'Debe de ser único'
        }
    def clean_password(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('La contraseña es muy pequeña al menos 8 caracteres')
        return super(UserRegisterForm, self).clean_password1()

         

class UserUpdateForm(forms.ModelForm):    

    class Meta:
        model = User
        fields = ['first_name','last_name']


class Profileste(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'birthday', 'DNI','telephone','gender','country','city','direction']
        help_texts = {
            "Cédula": "Debes de ingresar una cédula válida",
           # 'telephone': 'Tienes que ser mayor de edad'
        }


class ProfileForm(forms.ModelForm):
    
    Gender = (
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),

    )
   
    birthday = forms.DateField(label='Fecha de Nacimiento',
        widget=forms.TextInput(attrs={'type': 'date'}),
        help_text='Tienes que ser mayor de edad',
        error_messages = {
            'required': 'Porfavor ingresar una fecha'
        }
    )
    telephone = forms.CharField(label='No. de celular',widget=forms.NumberInput(), help_text='Tiene que terner 8 digitos')
    direction = forms.CharField(label='Dirección', required=False)
    DNI = forms.CharField(label='Cédula', error_messages = {
            'required': 'Porfavor ingresar una Cédula Valida',
            'unique':'La Cédula ya esta registrada'})
    telephone = forms.IntegerField(label='Celular', error_messages = {
            'required': 'Porfavor ingresar una número de Celular'})
    gender = forms.ChoiceField(label='Género', choices=Gender, error_messages = {
            'required': 'Porfavor ingresar su género'})
    country = forms.ModelChoiceField(label='Departamento',queryset=Country.objects.all().order_by('name'),error_messages = {
            'required': 'Porfavor ingresar Departamento'})
    city = forms.ModelChoiceField(label='Municipio',queryset=City.objects.all(),error_messages = {
            'required': 'Porfavor ingresar Municipio'})
    class Meta:
        model = Profile
        fields = ['image', 'birthday', 'DNI','gender','country','city','direction','telephone']
        help_texts = {
            "Cédula": "Debes de ingresar una cédula válida",
           # 'telephone': 'Tienes que ser mayor de edad'
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['city'].queryset = City.objects.all()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'birthday', 'DNI','gender','country','city','direction','telephone']
        help_texts = {
            "Cédula": "Debes de ingresar una cédula válida",
           # 'telephone': 'Tienes que ser mayor de edad'
        }

class ProfileFormAdmin(forms.ModelForm):
    
    Gender = (
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),

    )
   
    birthday = forms.DateField(label='Fecha de Nacimiento',
        widget=forms.TextInput(attrs={'type': 'date'}),
        help_text='Tienes que ser mayor de edad',
        error_messages = {
            'required': 'Porfavor ingresar una fecha'
        }
    )
    telephone = forms.CharField(label='No. de celular',widget=forms.NumberInput(), help_text='Tiene que terner 8 digitos')
    direction = forms.CharField(label='Dirección', required=False)
    DNI = forms.CharField(label='Cédula', error_messages = {
            'required': 'Porfavor ingresar una Cédula Valida',
            'unique':'La Cédula ya esta registrada'})
    telephone = forms.IntegerField(label='Celular', error_messages = {
            'required': 'Porfavor ingresar una número de Celular'})
    gender = forms.ChoiceField(label='Género', choices=Gender, error_messages = {
            'required': 'Porfavor ingresar su género'})
    country = forms.ModelChoiceField(label='Departamento',queryset=Country.objects.all().order_by('name'),error_messages = {
            'required': 'Porfavor ingresar Departamento'})
    city = forms.ModelChoiceField(label='Municipio',queryset=City.objects.all(),error_messages = {
            'required': 'Porfavor ingresar Municipio'})
    class Meta:
        model = Profile
        fields = ['image', 'birthday', 'DNI','gender','country','city','direction','telephone']
        help_texts = {
            "Cédula": "Debes de ingresar una cédula válida",
           # 'telephone': 'Tienes que ser mayor de edad'
        }
        
        
   

class ProfileForm_NoImg(forms.ModelForm):
    
    birthday = forms.DateField(label='Fecha de Nacimiento',
        widget=forms.TextInput(attrs={'type': 'date'}),
        help_text='Tienes que ser mayor de edad',
        error_messages = {
            'required': 'Porfavor ingresar una fecha'
        }
    )
    telephone = forms.CharField(label='Celular',widget=forms.NumberInput(), help_text='Tiene que terner 8 digitos')
    direction = forms.CharField(label='Dirección', required=False)
    
    class Meta:
        model = Profile
        fields = ['birthday', 'DNI','telephone','country','city','direction']
        help_texts = {
            "Cédula": "Debes de ingresar una cédula válida",
           # 'telephone': 'Tienes que ser mayor de edad'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

class PersonForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'birthday', 'DNI','telephone','country','city','direction']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')



class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "Este correo no se encuentra registrado."
            self.add_error('email', msg)
        return email