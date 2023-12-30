from django.urls import path
from . import views


urlpatterns=[
    path("registerUser/",views.registerUser,name='registerUser'),
    path("registerVendor/",views.registerVendor,name='registerVendor'),

    path("login/",views.login,name='login'),
    path("logout/",views.user_logout,name='logout'),

    path("myaccount/",views.myAccount,name='myAccount'),
    path("customerdashboard/",views.customerdashboard,name='customerdashboard'),
    path("vendordashboard/",views.vendordashboard,name='vendordashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),


]



