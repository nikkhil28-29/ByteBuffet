from django.contrib import admin
from django.urls import path,include
from . import views
from marketplace import views as MarketplaceViews

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
     
    path('', include('accounts.urls')),
    # path('verification/', include('verify_email.urls')),
    path('marketplace/', include('marketplace.urls')),

    path('cart/', MarketplaceViews.cart, name='cart'),
   
    # search	
    path('search/', MarketplaceViews.search, name='search'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('cart/', MarketPlace.views)
    path('checkout/', MarketplaceViews.checkout, name='checkout'),

    # ORDERS
    path('orders/', include('orders.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
