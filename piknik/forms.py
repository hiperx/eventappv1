from django import forms
from .models import Piknik
from events.models import ActiveEvent
from piknik.models import Przystanek
from django.core.validators import RegexValidator

class PiknikRegistrationForm(forms.Form):
    login_validator = RegexValidator(
        regex='^[a-zA-Z]+$',
        message='Login powinien składać się tylko z liter a-z.',
    )

    login = forms.CharField(
        label='Login',
        max_length=255,
        widget=forms.TextInput(attrs={'autofocus': True}),
        validators=[login_validator],
        error_messages={
            'invalid': 'Login powinien składać się tylko z liter a-z.',
            'required': 'Pole nie może być puste'
        }
    )
    imie = forms.CharField(label='Imię', max_length=255, error_messages={'required': 'To pole jest wymagane.'})
    nazwisko = forms.CharField(label='Nazwisko', max_length=255, error_messages={'required': 'To pole jest wymagane.'})
    osoba_towarzyszaca = forms.BooleanField(label='Osoba towarzysząca', required=False)
    liczba_dzieci = forms.IntegerField(label='Liczba dzieci', widget=forms.Select(choices=[(0, 'Brak'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')]))
    wiek_dziecka_1 = forms.IntegerField(label='Wiek dziecka 1', required=False, widget=forms.Select(choices=[(i, i) for i in range(19)]))
    wiek_dziecka_2 = forms.IntegerField(label='Wiek dziecka 2', required=False, widget=forms.Select(choices=[(i, i) for i in range(19)]))
    wiek_dziecka_3 = forms.IntegerField(label='Wiek dziecka 3', required=False, widget=forms.Select(choices=[(i, i) for i in range(19)]))
    wiek_dziecka_4 = forms.IntegerField(label='Wiek dziecka 4', required=False, widget=forms.Select(choices=[(i, i) for i in range(19)]))
    wiek_dziecka_5 = forms.IntegerField(label='Wiek dziecka 5', required=False, widget=forms.Select(choices=[(i, i) for i in range(19)]))
    wiek_dziecka_6 = forms.IntegerField(label='Wiek dziecka 6', required=False, widget=forms.Select(choices=[(i, i) for i in range(19)]))
    wiek_dziecka_7 = forms.IntegerField(label='Wiek dziecka 7', required=False, widget=forms.Select(choices=[(i, i) for i in range(19)]))    
    transport_wlasny = forms.BooleanField(label='Transport własny', required=False)
    przystanek = forms.ModelChoiceField(
        label='Przystanek',
        queryset=Przystanek.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    zaakceptowane_regulamin = forms.BooleanField(
        label='Akceptuję regulamin eventu',
        required=True,
        error_messages={'required': 'Musisz zaakceptować regulamin eventu.'}
    )

    def __init__(self, *args, **kwargs):
        super(PiknikRegistrationForm, self).__init__(*args, **kwargs)

        # Pobierz aktywny event
        active_event = ActiveEvent.objects.filter(rodzaj_eventu='piknik', aktywny=True).first()

        # Pobierz posortowany queryset przystanków
        sorted_przystanki = Przystanek.objects.all().order_by('nazwa')

        # Ogranicz dostępne przystanki do tych związanych z aktywnym oddziałem
        if active_event:
            self.fields['przystanek'].queryset = Przystanek.objects.filter(oddzial=active_event.oddzial)
        
        # Przekazanie posortowanego queryset do pola przystanek
        self.fields['przystanek'].queryset = sorted_przystanki
    
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
