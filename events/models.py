#events/model.py
from django.db import models

class Oddzial(models.Model):
    nazwa = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name_plural = "Oddzial"

    def __str__(self):
        return self.nazwa

class ActiveEvent(models.Model):
    EVENT_CHOICES = [
        ('bal', 'Bal'),
        ('piknik', 'Piknik'),
        # Dodaj inne rodzaje eventów w miarę potrzeb
    ]

    rodzaj_eventu = models.CharField(max_length=255, choices=EVENT_CHOICES)
    rok = models.IntegerField()
    oddzial = models.ForeignKey(Oddzial, on_delete=models.SET_NULL, null=True)
    aktywny = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Active event"

    def save(self, *args, **kwargs):
        if self.aktywny:
            # Jeśli nowy event jest oznaczony jako aktywny, dezaktywuj pozostałe
            ActiveEvent.objects.exclude(pk=self.pk).update(aktywny=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rodzaj_eventu}{self.rok}{self.oddzial}"
