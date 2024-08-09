import os
import django
from eventapp import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventapp.settings")
    django.setup()

    # Importuj modele Django i wykonaj operacje na bazie danych
    from bal.models import Bal
    from events.models import ActiveEvent

    # Pobierz pierwszy aktywny event o rodzaju 'bal'
    aktywny_event = ActiveEvent.objects.filter(aktywny=True, rodzaj_eventu='bal').first()

    # Sprawdź, czy znaleziono aktywny event
    if aktywny_event:
        # Lista danych do dodania
        dane_do_dodania = [
            {"identyfikator": 111111111111159729, "login": "irenat", "imie": "Irena", "nazwisko": "Tomkowiak", "data_utworzenia": "2024-01-25 21:23:32.278226+00:00", "event":aktywny_event, "is_registred": True},


            # Dodaj inne dane tutaj...
        ]

        # Iteruj przez dane i utwórz rekordy
        for dane in dane_do_dodania:
            Bal.objects.create(**dane)
    else:
        print("Nie znaleziono aktywnego eventu o rodzaju 'bal'.")
