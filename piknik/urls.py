# piknik/urls.py
from django.urls import path
from .views import PiknikIndexView, ConfirmPiknikView, AlreadyRegistredView, AgainRegistrationView

app_name = 'piknik'

urlpatterns = [
    path('', PiknikIndexView.as_view(), name='index'),
    path('confirm/<int:identifier>/', ConfirmPiknikView.as_view(), name='confirm_piknik'),
    path('already_registred/<int:identifier>/', AlreadyRegistredView.as_view(), name='already_registred'),
    path('again_registration/<int:identifier>/', AgainRegistrationView.as_view(), name='again_registration'),
]
