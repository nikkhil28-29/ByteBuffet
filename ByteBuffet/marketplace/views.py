from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Prefetch
# from django.db.models import Prefetch

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache

from django.shortcuts import get_object_or_404, redirect, render

from .context_processors import cart_counter, get_cart_amounts
from accounts.models import UserProfile
from menu.models import Category, FoodItem,Vendor
# from menu.models import Vendor
from .models import Cart
from django.contrib.auth.decorators import login_required

#GIS
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(  #no foreign key in Category to fecth food, so Pefecth fooditem fr
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        ) 
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html',context)

@never_cache
def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        print(request.user.email)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            print(food_id)
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                print(fooditem.category)
                print(fooditem.food_title)

                try:
                    CheckKart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    print(CheckKart.quantity)

                    CheckKart.quantity += 1
                    CheckKart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': cart_counter(request), 'qty': CheckKart.quantity, 'cart_amount':get_cart_amounts(request)})
                    
                except ObjectDoesNotExist:
                    CheckKart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': cart_counter(request), 'qty': CheckKart.quantity, 'cart_amount':get_cart_amounts(request)})
                    #  'cart_amount': get_cart_amounts(request)
#  'cart_amount': get_cart_amounts(request)
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
            except Exception as e:
                print(e)
                return JsonResponse({'status': 'Failed', 'message': 'An error occurred!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

@never_cache
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    CheckKart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if CheckKart.quantity > 1:
                        CheckKart.quantity -= 1
                        CheckKart.save()
                    else:
                        CheckKart.delete()
                        CheckKart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': cart_counter(request), 'qty': CheckKart.quantity, 'cart_amount':get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

@never_cache
@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')   #order by creaed at while listing it
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

@never_cache
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', })
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})



            # method for search restaurat on home page

def search(request):
    if not 'src_address' in request.GET:
        return redirect('marketplace')
    else:
        vendors=None
        address=request.GET['src_address']  #name=src_address in html , from where this func/url is called
        latitude=request.GET['lat'] 
        longitude=request.GET['long'] 
        radius=request.GET['radius'] 
        keyword = request.GET.get('keyword')   #search for food/restaurant

        # vendors=Vendor.objects.filter(user__is_active=True, is_approved=True, vendor_name__icontains=keyword)
        search_vendor_by_food=FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True) #that vendor is in mdoel

        if latitude and longitude and radius:
            pnt=GEOSGeometry('POINT(%s %s)'% (longitude, latitude))
            
            # all the vendor (id) which have the food , which have searched for
            vendors=Vendor.objects.filter(Q(id__in=search_vendor_by_food) | Q(user__is_active=True, is_approved=True, 
            vendor_name__icontains=keyword), user_profile__location__distance_lte=(pnt, D(km=radius))).annotate(distance1=Distance("user_profile__location", pnt)).order_by("distance1") #user_profile has location field
            #order the listed items by distance          #__lte= (<=)

            for i in vendors:
                i.kms = round(i.distance1.km, 2)    # send distance from particuslar vendor


        vendor_count=vendors.count() if vendors is not None else 0

            

        context={
            'vendor_count':vendor_count,
            'vendors':vendors,
            'src_location':address
        }

    return render(request, 'marketplace/listings.html', context)
