# piknik/views.py
from django.shortcuts import render, redirect
from django.views import View
from .forms import PiknikRegistrationForm
from .models import Piknik 
from events.models import ActiveEvent
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils import timezone

class PiknikIndexView(View):
    template_name = 'piknik/index.html'

    def get(self, request, *args, **kwargs):
        active_event = ActiveEvent.objects.filter(rodzaj_eventu='piknik', aktywny=True).first()
        if active_event:
            form = PiknikRegistrationForm(initial={'event': active_event})
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'piknik/no_active_event.html')

    def post(self, request, *args, **kwargs):
        identifier = request.POST.get('identyfikator')
 
        if not identifier:
            return render(request, self.template_name, {'error': 'Pole identyfikatora nie może być puste!'})

        existing_piknik = Piknik.objects.filter(identyfikator=identifier).first()


        if existing_piknik:
            if existing_piknik.is_registred:
                return render(request, 'piknik/already-registred.html', {'identifier': identifier})
            elif existing_piknik.is_registred is False:
                return render(request, 'piknik/again-registration.html', {'identifier': identifier, 'login': existing_piknik.login})

        return redirect('piknik:confirm_piknik', identifier=identifier)



class ConfirmPiknikView(View):
    template_name = 'piknik/confirm_piknik.html'

    def get(self, request, identifier, *args, **kwargs):
        form = PiknikRegistrationForm(initial={'identyfikator': identifier})
        return render(request, self.template_name, {'form': form, 'identifier': identifier})
    

    def post(self, request, identifier, *args, **kwargs):
        form = PiknikRegistrationForm(request.POST)
        error_message = None

        try:
            if form.is_valid():
                login = form.cleaned_data['login']
                imie = form.cleaned_data['imie']
                nazwisko = form.cleaned_data['nazwisko']
                osoba_towarzyszaca = form.cleaned_data['osoba_towarzyszaca']
                liczba_dzieci = form.cleaned_data['liczba_dzieci']
                transport_wlasny = form.cleaned_data['transport_wlasny']
                przystanek = form.cleaned_data['przystanek']
                wiek_dziecka_1 = form.cleaned_data.get('wiek_dziecka_1')
                wiek_dziecka_2 = form.cleaned_data.get('wiek_dziecka_2')
                wiek_dziecka_3 = form.cleaned_data.get('wiek_dziecka_3')
                wiek_dziecka_4 = form.cleaned_data.get('wiek_dziecka_4')
                wiek_dziecka_5 = form.cleaned_data.get('wiek_dziecka_5')
                wiek_dziecka_6 = form.cleaned_data.get('wiek_dziecka_6')
                wiek_dziecka_7 = form.cleaned_data.get('wiek_dziecka_7')
                zaakceptowane_regulamin = form.cleaned_data.get('zaakceptowane_regulamin')

                active_event = ActiveEvent.objects.filter(aktywny=True, rodzaj_eventu='piknik').first()

                if active_event:
                    existing_user = Piknik.objects.filter(login=login, event=active_event).first()
                    if existing_user:
                        error_message = "Użytkownik o podanym loginie już istnieje. Proszę wybrać inny login."
                        existing_user.is_registred = False
                        existing_user.save()
                        return JsonResponse({'success': False, 'errors': error_message})
                    else:
                        Piknik.objects.create(
                            identyfikator=identifier,
                            login=login,
                            imie=imie,
                            nazwisko=nazwisko,
                            osoba_towarzyszaca=osoba_towarzyszaca,
                            liczba_dzieci=liczba_dzieci,
                            transport_wlasny=transport_wlasny,
                            przystanek=przystanek,
                            event=active_event,
                            is_registred=True,
                            wiek_dziecka_1=wiek_dziecka_1,
                            wiek_dziecka_2=wiek_dziecka_2,
                            wiek_dziecka_3=wiek_dziecka_3,
                            wiek_dziecka_4=wiek_dziecka_4,
                            wiek_dziecka_5=wiek_dziecka_5,
                            wiek_dziecka_6=wiek_dziecka_6,
                            wiek_dziecka_7=wiek_dziecka_7,
                            zaakceptowane_regulamin=zaakceptowane_regulamin
                        )
                        return JsonResponse({'success': True})
            else:
                #error_message = 'Wprowadzono nieprawidłowe dane. Spróbuj ponownie.'
                error_message = form.errors.as_json()  # Zwróć szczegóły błędów formularza
        except Exception as e:
            error_message = str(e)


        return JsonResponse({'success': False, 'errors': error_message})



class AlreadyRegistredView(View):
    template_name = 'piknik/already-registred.html'

    def get(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        form = PiknikRegistrationForm(initial={'identyfikator': identifier})
        return render(request, self.template_name, {'form': form, 'identifier': identifier})

    def post(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        login = request.POST.get('login')

        # Sprawdź, czy istnieje użytkownik o podanym loginie i is_registred ustawione na True
        user = Piknik.objects.filter(login=login, is_registred=True).first()
        print(user)
        if user:
            # Ustaw is_registred na False i zapisz obiekt
            user.is_registred = False
            user.save()
            success_message = "Użytkownik został pomyślnie wypisany z pikniku."
            return render(request, self.template_name, {'success_message': success_message, 'identifier': identifier})
        else:
            error_message = "Podany login nie jest poprawny, spróbuj raz jeszcze!"
            return render(request, self.template_name, {'error_message': error_message, 'identifier': identifier})
        
class AgainRegistrationView(View):
    template_name = 'piknik/again-registration.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        login = request.POST.get('login')

        try:
            existing_piknik = Piknik.objects.get(identyfikator=identifier, login=login)
        except Piknik.DoesNotExist:
            error_message = "Podany login nie jest poprawny, spróbuj raz jeszcze!"
            return render(request, self.template_name, {'identifier': identifier, 'error_message': error_message})

        # Dodaj kod obsługujący dane z formularza, jeśli to konieczne
        existing_piknik.is_registred = True

        # Pobierz istniejący obiekt Piknik
        existing_piknik = Piknik.objects.get(identyfikator=identifier, login=login)

        # Zmiana daty utworzenia i modyfikacji na aktualny czas
        existing_piknik.created = timezone.now()
        existing_piknik.modified = timezone.now()

        # Zapisz zmieniony obiekt
        
        existing_piknik.save()

        success_message = "Użytkownik został ponownie zapisany na piknik."
        return render(request, self.template_name, {'identifier': identifier, 'success_message': success_message})


