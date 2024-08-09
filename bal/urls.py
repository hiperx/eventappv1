# bal/urls.py
from django.urls import path
from .views import BalIndexView, ConfirmBalView, AlreadyRegistredView, AgainRegistrationView
#from django.conf.urls.static import static
#from django.conf import settings


app_name = 'bal'

urlpatterns = [
    path('', BalIndexView.as_view(), name='index'),
    path('confirm_bal/<int:identifier>/', ConfirmBalView.as_view(), name='confirm_bal'),    
    path('already_registred/<int:identifier>/', AlreadyRegistredView.as_view(), name='already_registred'),  # Dodaj identifier do URL-a
    path('again_registration/<int:identifier>/', AgainRegistrationView.as_view(), name='again_registration'),
]

#if settings.DEBUG:
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)