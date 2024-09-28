from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns=[
        path('', views.myAccount),

    path("registerUser/",views.registerUser,name='registerUser'),
    path("registerVendor/",views.registerVendor,name='registerVendor'),

    path("login/",views.login,name='login'),
    path("logout/",views.user_logout,name='logout'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    #account , activation


    path("myaccount/",views.myAccount,name='myAccount'),
    path("customerdashboard/",views.customerdashboard,name='customerdashboard'),
    path("vendordashboard/",views.vendordashboard,name='vendordashboard'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

    path('vendor/', include('vendor.urls')),
    path('customers/', include('customers.urls')),

]



