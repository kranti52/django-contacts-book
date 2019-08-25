from django.conf.urls import url

from .views import LoginView
from .views import RegisterView

urlpatterns = [
    url(r'register/$', RegisterView.as_view(), name='account-register'),
    url(r'login/$', LoginView.as_view(), name='account-signin'),
]
