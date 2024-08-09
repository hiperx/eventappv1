#piknik/admin.py
from django import forms
from django.contrib import admin
from .models import Piknik, Przystanek
from events.models import ActiveEvent
from piknik.models import Przystanek


class PiknikAdminForm(forms.ModelForm):
    class Meta:
        model = Piknik
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(PiknikAdminForm, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = ActiveEvent.objects.filter(rodzaj_eventu='piknik', aktywny=True)

        if 'event' in self.fields:
            active_event = self.fields['event'].queryset.first()
            if active_event and 'przystanek' in self.fields:
                oddzial_przystanki = Przystanek.objects.filter(oddzial=active_event.oddzial)
                self.fields['przystanek'].queryset = oddzial_przystanki



class PiknikAdmin(admin.ModelAdmin):
    form = PiknikAdminForm
    list_display = ['id', 'identyfikator', 'login', 'imie', 'nazwisko', 'osoba_towarzyszaca', 'liczba_dzieci', 'transport_wlasny', 'przystanek', 'event', 'is_registred', 'data_utworzenia', 'data_modyfikacji']
    search_fields = ['login', 'imie', 'nazwisko']

admin.site.register(Piknik, PiknikAdmin)

class PrzystanekAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'oddzial')

admin.site.register(Przystanek, PrzystanekAdmin)