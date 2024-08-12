#eventapp/panel/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    PanelIndexView, 
    generate_excel_report, 
    ListaOsobWypisanychView, 
    ListaOsobZapisanychView, 
    WyłączZapisyView, 
    generate_excel_report_wypisani, 
    excel_report_piknik_transport, 
    excel_report_piknik_przystanek, 
    lista_przystankow, 
    edytuj_przystanek, 
    usun_przystanek, 
    uruchom_event
)

app_name = 'panel'

urlpatterns = [
    
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='panel:panel-index'), name='logout'),
    path('', PanelIndexView.as_view(), name='panel-index'),
    path('generate_excel_report/', generate_excel_report, name='generate_excel_report'),
    path('generate_excel_report_wypisani/', generate_excel_report_wypisani, name='generate_excel_report_wypisani'),
    path('excel_report_piknik_transport/', excel_report_piknik_transport, name='excel_report_piknik_transport'),
    path('excel_report_piknik_przystanek/', excel_report_piknik_przystanek, name='excel_report_piknik_przystanek'),
    path('lista_osob_wypisanych/', ListaOsobWypisanychView.as_view(), name='lista_osob_wypisanych'),
    path('lista_osob_zapisanych/', ListaOsobZapisanychView.as_view(), name='lista_osob_zapisanych'),

    path('lista_przystankow/', lista_przystankow, name='lista_przystankow'),
    path('edytuj_przystanek/<int:przystanek_id>/', edytuj_przystanek, name='edytuj_przystanek'),
    path('usun_przystanek/<int:przystanek_id>/', usun_przystanek, name='usun_przystanek'),

    
    path('uruchom_event/', uruchom_event, name='uruchom_event'),

    path('wylacz_zapisy/', WyłączZapisyView.as_view(), name='wylacz_zapisy'),
    # ... other URL patterns ...
]

