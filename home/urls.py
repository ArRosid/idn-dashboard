from django.urls import path
from home.views import home, hi_idn

app_name = "home"

urlpatterns = [
    path("", home, name="home"),
    path("hi_idn/", hi_idn, name="hi_idn"),
]
