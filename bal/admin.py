#bal/admin.py
from django import forms
from django.contrib import admin
from .models import Bal
from events.models import ActiveEvent

from django.contrib.admin.models import LogEntry


class BalAdminForm(forms.ModelForm):
    class Meta:
        model = Bal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BalAdminForm, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = ActiveEvent.objects.filter(rodzaj_eventu='bal', aktywny=True)


    def clean(self):
        cleaned_data = super().clean()
        identyfikator = cleaned_data.get('identyfikator')
        login = cleaned_data.get('login')
        event = cleaned_data.get('event')

        if Bal.objects.filter(identyfikator=identyfikator, login=login, event=event).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Użytkownik z tym identyfikatorem i loginem już istnieje w ramach tego eventu.')


class BalAdmin(admin.ModelAdmin):
    form = BalAdminForm
    list_display = ['id', 'identyfikator', 'login', 'imie', 'nazwisko', 'event', 'is_registred', 'data_utworzenia', 'data_modyfikacji']
    search_fields = ['login', 'imie', 'nazwisko']

admin.site.register(Bal, BalAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message']
    search_fields = ['user__username', 'object_repr', 'change_message']

admin.site.register(LogEntry, EntryAdmin)
