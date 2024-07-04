from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("setCodeVerifier/<str:codeVerifier>", views.setCodeVerifier, name="setCodeVerifier"),
    path("spcallback", views.spCallback, name="callback"),
    path("username", views.getUsername, name="username")
]


