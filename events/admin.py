from django.contrib import admin
from .models import ActiveEvent, Oddzial

class ActiveEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'rodzaj_eventu', 'rok', 'oddzial', 'aktywny']
    list_editable = ['aktywny']

admin.site.register(ActiveEvent, ActiveEventAdmin)

from django.contrib import admin
from .models import Oddzial

admin.site.register(Oddzial)