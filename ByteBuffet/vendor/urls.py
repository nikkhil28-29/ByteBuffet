from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from accounts import views as AccountViews




urlpatterns=[
        path('', AccountViews.vendordashboard, name='vendor'),
        path('profile/', views.vprofile, name='vprofile'),

]