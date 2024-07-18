from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("queryTabs", views.queryTabs, name="queryTabs"),
    path("getTabInfo", views.getTabInfo, name="getTabInfo"),
    path("getTotalTabs", views.getTotalTabNum, name="getTotalTabs")
]