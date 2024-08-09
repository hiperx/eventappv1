# eventapp/urls.py
from django.urls import path, include
from django.contrib import admin
from .views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('panel.urls')),
    path('', index, name='index'),
    # Dodaj inne ścieżki do twoich aplikacji tutaj    
    path('bal/', include(('bal.urls', 'bal'), namespace='bal')),
    path('piknik/', include(('piknik.urls', 'piknik'), namespace='piknik')),
    path('scanbal/', include('scanbal.urls')),
    # inne ścieżki...
]


