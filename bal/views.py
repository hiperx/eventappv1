# bal/views.py
from django.shortcuts import render, redirect
from django.views import View
from .forms import BalRegistrationForm
from .models import Bal
from events.models import ActiveEvent
from django.http import JsonResponse
from django.forms import ValidationError

class BalIndexView(View):
    template_name = 'bal/index.html'

    def get(self, request, *args, **kwargs):
        active_event = ActiveEvent.objects.filter(rodzaj_eventu='bal', aktywny=True).first()
        if active_event:
            form = BalRegistrationForm(initial={'event': active_event})
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'bal/no_active_event.html')

    def post(self, request, *args, **kwargs):
        identifier = request.POST.get('identyfikator')

        if not identifier:
            # Dodaj obsługę sytuacji, gdy identyfikator jest pusty
            return render(request, self.template_name, {'error': 'Pole identyfikatora nie może być puste!'})

        # Sprawdź, czy identyfikator już istnieje w bazie danych
        existing_bal = Bal.objects.filter(identyfikator=identifier).first()

        if existing_bal:
            # Dodaj obsługę istniejącego identyfikatora
            # existing_bal.refresh_from_db()  # Wymuszenie aktualizacji obiektu z bazy danych

            if existing_bal.is_registred:
                # Przekieruj do widoku already_registred, przekazując identifier
                return render(request, 'bal/already-registred.html', {'identifier': identifier})
            elif existing_bal.is_registred is False:
                return render(request, 'bal/again-registration.html', {'identifier': identifier, 'login': existing_bal.login})

        # Jeśli identyfikator nie istnieje, przekieruj do widoku potwierdzenia
        return redirect('bal:confirm_bal', identifier=identifier)

class ConfirmBalView(View):
    template_name = 'bal/confirm_bal.html'

    def get(self, request, identifier, *args, **kwargs):
        form = BalRegistrationForm(initial={'identyfikator': identifier})
        print(identifier)
        return render(request, self.template_name, {'form': form, 'identifier': identifier})
        

    def post(self, request, identifier, *args, **kwargs):
        form = BalRegistrationForm(request.POST)
        error_message = None

        try:
            if form.is_valid():
                login = form.cleaned_data['login']
                imie = form.cleaned_data['imie']
                nazwisko = form.cleaned_data['nazwisko']

                active_event = ActiveEvent.objects.filter(aktywny=True, rodzaj_eventu='bal').first()

                if active_event:
                    existing_user = Bal.objects.filter(login=login, event=active_event).first()

                    if existing_user:
                        existing_user.is_registred = False
                        existing_user.save()
                        error_message = "Wprowadzono niepoprawny login. Spróbuj raz jeszcze."
                    else:
                        Bal.objects.create(
                            identyfikator=identifier,
                            login=login,
                            imie=imie,
                            nazwisko=nazwisko,
                            event=active_event,
                            is_registred=True
                        )
                        print(identifier)
                        return JsonResponse({'success': True})
        except ValidationError as e:
            print('Wystąpił błąd:', str(e))
            error_message = "Login powinien składać się tylko z liter a-z."

        if error_message:
            return JsonResponse({'success': False, 'errors': error_message})
        else:
            return JsonResponse({'success': False, 'errors': 'Login został wprowadzony niepoprawnie, podaj go raz jeszcze, <br>pamiętaj że może się on składać tylko z liter.'})
            
class AlreadyRegistredView(View):
    template_name = 'bal/already-registred.html'

    def get(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        form = BalRegistrationForm(initial={'identyfikator': identifier})
        return render(request, self.template_name, {'form': form, 'identifier': identifier})

    def post(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        login = request.POST.get('login')

        # Sprawdź, czy istnieje użytkownik o podanym loginie i is_registred ustawione na True
        user = Bal.objects.filter(login=login, is_registred=True).first()
        print(user)
        if user:
            # Ustaw is_registred na False i zapisz obiekt
            user.is_registred = False
            user.save()
            success_message = "Użytkownik został pomyślnie wypisany z balu."
            return render(request, self.template_name, {'success_message': success_message, 'identifier': identifier})
        else:
            error_message = "Podany login nie jest poprawny, spróbuj raz jeszcze!"
            return render(request, self.template_name, {'error_message': error_message, 'identifier': identifier})

class AgainRegistrationView(View):
    template_name = 'bal/again-registration.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        login = request.POST.get('login')

        try:
            existing_bal = Bal.objects.get(identyfikator=identifier, login=login)
        except Bal.DoesNotExist:
            error_message = "Podany login nie jest poprawny, spróbuj raz jeszcze!"
            return render(request, self.template_name, {'identifier': identifier, 'error_message': error_message})

        # Dodaj kod obsługujący dane z formularza, jeśli to konieczne
        existing_bal.is_registred = True
        existing_bal.save()

        success_message = "Użytkownik został ponownie zapisany na bal."
        return render(request, self.template_name, {'identifier': identifier, 'success_message': success_message})


