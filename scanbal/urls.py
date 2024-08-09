# scanbal/urls.py
from django.urls import path
from .views import ScanBalIndexView

app_name = 'scanbal'

urlpatterns = [
    path('', ScanBalIndexView.as_view(), name='scanbal'),
]
