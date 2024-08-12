# w pliku forms.py w aplikacji "panel"

class PrzystanekForm(forms.ModelForm):
    class Meta:
        model = Przystanek
        fields = ['nazwa', 'oddzial']