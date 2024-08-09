# bal/forms.py
from django import forms
from django.core.validators import RegexValidator

class BalRegistrationForm(forms.Form):
    login = forms.CharField(label='Login', max_length=255, widget=forms.TextInput(attrs={'autofocus': True}))
    imie = forms.CharField(label='Imię', max_length=255, error_messages={'required': 'To pole jest wymagane.'})
    nazwisko = forms.CharField(label='Nazwisko', max_length=255, error_messages={'required': 'To pole jest wymagane.'})

    login_validator = RegexValidator(
        regex='^[a-zA-Z]+$',
        message='Login powinien składać się tylko z liter a-z.',
        code='invalid_login'
    )

    login = forms.CharField(
        label='Login',
        max_length=255,
        widget=forms.TextInput(attrs={'autofocus': True}),
        validators=[login_validator]
    )
    
    def clean_imie(self):
        # Konwertuj imię na formę, gdzie każdy wyraz zaczyna się dużą literą
        imie = self.cleaned_data.get('imie')
        if imie:
            return imie.title()
        return imie

    def clean_nazwisko(self):
        # Konwertuj nazwisko na formę, gdzie pierwsza litera jest z dużą literą
        nazwisko = self.cleaned_data.get('nazwisko')
        if nazwisko:
            return nazwisko.title()
        return nazwisko
    
    def clean_login(self):
        # Konwertuj login na małe litery przed zapisaniem do bazy danych
        login = self.cleaned_data.get('login')
        if login:
            return login.lower()
        return login