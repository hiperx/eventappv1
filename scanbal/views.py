from django.shortcuts import render
from django.views import View
from bal.models import Bal
from django.http import JsonResponse

class ScanBalIndexView(View):
    template_name = 'scanbal/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        identifier = request.POST.get('identifier')
        
        if not identifier:
            # Dodaj obsługę sytuacji, gdy identyfikator jest pusty
            return render(request, self.template_name, {'error': 'Pole identyfikatora nie może być puste!'})            

        user = Bal.objects.filter(identyfikator=identifier, event__rodzaj_eventu='bal', event__oddzial__nazwa='POZ1', event__rok=2024).first()
        
        if user:
            if user.is_registred:
                return render(request, self.template_name, {'success': 'Witamy, zapraszamy na BAL! \n Użytkownik pomyślnie zapisany na event.'})
            else:

                return render(request, self.template_name, {'error': 'Przepraszamy, użytkownik nie znajduje się na liście.\n Był zapisany na bal ale sam wypisał się z balu.'})

        else:
            return render(request, self.template_name, {'error': 'Przepraszamy, użytkownik nie został zapisany na bal.'})
