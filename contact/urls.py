from django.conf.urls import url
from rest_framework import routers

from .views import ContactListView
from .views import ContactView

router = routers.DefaultRouter()

urlpatterns = [
    url(r'create$', ContactView.as_view(), name='contact-create'),
    url(r'(?P<id>[\d+])$', ContactView.as_view(), name='contact-retrieve'),
    url(r'(?P<id>[\d+])/update$', ContactView.as_view(), name='contact-update'),
    url(r'(?P<id>[\d+])/basic-update$', ContactView.as_view(), name='contact-basic-update'),
    url(r'(?P<id>[\d+])/delete$', ContactView.as_view(), name='contact-delete'),
    url(r'^$', ContactListView.as_view(), name='contact-list'),
]
