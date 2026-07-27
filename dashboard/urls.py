from django.urls import path
from dashboard.views import home_view, sobre_view

app_name = "dashboard"
urlpatterns = [
    path("home/", home_view, name="home"),
    path("sobre/", sobre_view, name="sobre"),
]
