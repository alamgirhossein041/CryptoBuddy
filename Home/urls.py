from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('report/',include('Report.urls')),
    path('',views.home_page,name="home_page"),
    path('crypto-news/', views.news,name='news'),
]
