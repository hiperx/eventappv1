from django.db import models
from events.models import ActiveEvent

class Bal(models.Model):
    identyfikator = models.IntegerField(unique=True) 
    login = models.CharField(max_length=255, unique=True)
    imie = models.CharField(max_length=255, blank=False)
    nazwisko = models.CharField(max_length=255, blank=False)
    event = models.ForeignKey(ActiveEvent, on_delete=models.SET_NULL, null=True, blank=True)
    is_registred = models.BooleanField(default=False) 
    data_utworzenia = models.DateTimeField(auto_now_add=True)
    data_modyfikacji = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['identyfikator', 'login', 'event']
        verbose_name_plural = "Bal"
    
