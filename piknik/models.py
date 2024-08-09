from django.db import models
from events.models import ActiveEvent, Oddzial
from django.core.exceptions import ValidationError

class Piknik(models.Model):
    identyfikator = models.IntegerField()
    login = models.CharField(max_length=255)
    imie = models.CharField(max_length=255, blank=False)
    nazwisko = models.CharField(max_length=255, blank=False)
    osoba_towarzyszaca = models.BooleanField()
    liczba_dzieci = models.IntegerField(choices=[(0, 'Brak'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    #przystanek = models.ForeignKey('Przystanek', on_delete=models.SET_NULL, null=True, blank=False)
    przystanek = models.ForeignKey('Przystanek', on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(ActiveEvent, on_delete=models.SET_NULL, null=True, blank=True)
    transport_wlasny = models.BooleanField(default=True)
    is_registred = models.BooleanField(default=False)
    data_utworzenia = models.DateTimeField(auto_now_add=True)
    data_modyfikacji = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Piknik"

    def save(self, *args, **kwargs):
        if not self.event:
            # Jeśli nie określono eventu, ustaw domyślny event (ostatni aktywny event)
            self.event = ActiveEvent.objects.filter(aktywny=True).first()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}, {self.data_utworzenia}, {self.data_modyfikacji}'


class Przystanek(models.Model):
    nazwa = models.CharField(max_length=255)
    oddzial = models.ForeignKey(Oddzial, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Przystanek"

    def __str__(self):
        return self.nazwa
    
    
