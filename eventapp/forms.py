from django import forms
from events.models import Oddzial

class OddzialForm(forms.Form):
    oddzial = forms.ModelChoiceField(queryset=Oddzial.objects.all())
