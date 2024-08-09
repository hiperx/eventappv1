# piknik/forms.py
from django import forms
from .models import Piknik
from events.models import ActiveEvent
from piknik.models import Przystanek
from django.core.validators import RegexValidator

# class PiknikRegistrationForm(forms.Form):
#     login = forms.CharField(label='Login', max_length=255, widget=forms.TextInput(attrs={'autofocus': True}))
#     imie = forms.CharField(label='Imię', max_length=255, error_messages={'required': 'To pole jest wymagane.'})
#     nazwisko = forms.CharField(label='Nazwisko', max_length=255, error_messages={'required': 'To pole jest wymagane.'})
#     osoba_towarzyszaca = forms.BooleanField(label='Osoba towarzysząca', required=False)
#     liczba_dzieci = forms.IntegerField(label='Liczba dzieci', widget=forms.Select(choices=[(0, 'Brak'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]))
#     przystanek = forms.ChoiceField(label='Przystanek', choices=[('glogowska', 'Głogowska'), ('hetmanska', 'Hetmańska'), ('gorczyn', 'Górczyń')], widget=forms.Select(choices=[('glogowska', 'Głogowska'), ('hetmanska', 'Hetmańska'), ('gorczyn', 'Górczyń')]))


class PiknikRegistrationForm(forms.Form):
    login = forms.CharField(label='Login', max_length=255, widget=forms.TextInput(attrs={'autofocus': True}))
    imie = forms.CharField(label='Imię', max_length=255, error_messages={'required': 'To pole jest wymagane.'})
    nazwisko = forms.CharField(label='Nazwisko', max_length=255, error_messages={'required': 'To pole jest wymagane.'})
    osoba_towarzyszaca = forms.BooleanField(label='Osoba towarzysząca', required=False)
    liczba_dzieci = forms.IntegerField(label='Liczba dzieci', widget=forms.Select(choices=[(0, 'Brak'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]))
    transport_wlasny = forms.BooleanField(label='Transport własny', required=False)
    przystanek = forms.ModelChoiceField(
        label='Przystanek',
        queryset=Przystanek.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(PiknikRegistrationForm, self).__init__(*args, **kwargs)

        # Pobierz aktywny event
        active_event = ActiveEvent.objects.filter(rodzaj_eventu='piknik', aktywny=True).first()

        # Ogranicz dostępne przystanki do tych związanych z aktywnym oddziałem
        if active_event:
            self.fields['przystanek'].queryset = Przystanek.objects.filter(oddzial=active_event.oddzial)
    
    login_validator = RegexValidator(
        regex='^[a-zA-Z]+$',
        #message='Login powinien składać się tylko z liter a-z.',
        #code='invalid_login'
    )

    login = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'autofocus': True}),
        validators=[login_validator],
        error_messages={'invalid': 'Login powinien składać się tylko z liter a-z.',
                        'required': 'Pole nie może być puste'}
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
    

    def clean(self):
        cleaned_data = super().clean()
        transport_wlasny = cleaned_data.get('transport_wlasny')
        przystanek = cleaned_data.get('przystanek')

        if not transport_wlasny and not przystanek:
            raise forms.ValidationError("Musisz wybrać albo 'Przystanek', albo zaznaczyć 'Transport własny'.")

        return cleaned_data
    
    def clean_przystanek(self):
        transport_wlasny = self.cleaned_data.get('transport_wlasny')
        przystanek = self.cleaned_data.get('przystanek')

        if transport_wlasny:
            return None

        return przystanek
