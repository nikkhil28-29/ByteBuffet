from django.contrib import admin
from django.urls import path,include
from . import views
from marketplace import views as MarketplaceViews

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
     path('cart/', MarketplaceViews.cart, name='cart'),
     
    path('', include('accounts.urls')),
    path('verification/', include('verify_email.urls')),
    path('marketplace/', include('marketplace.urls')),	

    # path('cart/', MarketPlace.views)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
