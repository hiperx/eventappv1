#eventproject/eventapp/eventapp/views.py 
from django.shortcuts import render, redirect
from events.models import ActiveEvent



def index(request):
    # Pobierz aktywne wydarzenie
    active_event = ActiveEvent.objects.filter(aktywny=True).first()

    if active_event:
        # Sprawdź rodzaj aktywnego wydarzenia
        if active_event.rodzaj_eventu == 'bal':
            # Przekieruj do formularza bal
            return redirect('bal:index') # zmiana z bal:bal_form na bal
        elif active_event.rodzaj_eventu == 'piknik':
            # Przekieruj do formularza piknik
            return redirect('piknik:index')

    # Dodaj obsługę przypadku braku aktywnego wydarzenia lub błędu
    return render(request, 'no_event.html')

 
 
