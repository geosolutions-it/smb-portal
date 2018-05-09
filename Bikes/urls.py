from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^perfect/$', views.home, name='home'),
]