from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache

from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Prefetch
from .context_processors import cart_counter, get_cart_amounts
from accounts.models import UserProfile
from menu.models import Category, FoodItem
from menu.models import Vendor
from .models import Cart
from django.contrib.auth.decorators import login_required

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

# def add_to_cart(request, food_id):    #from ajax
#     if request.user.is_authenticated:
#         print(request.user.email)
#         if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

#             print(food_id)
#         # headers.get('x-requested-with') == 'XMLHttpRequest':  #whether the requested is an AJAX request.
#             try:
#                 fooditem = FoodItem.objects.get(id=food_id)
#                 print(fooditem.category)
#                 print(fooditem.food_title)

#                 try:
#                     CheckKart = Cart.objects.get(user=request.user, fooditem=fooditem)
#                     print(CheckKart.quantity)

#                     CheckKart.quantity += 1
#                     CheckKart.save()
#                     return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': cart_counter(request), 'qty': CheckKart.quantity, 'cart_amount': get_cart_amounts(request)})
                    
#                 except ObjectDoesNotExist:
#                     CheckKart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
#                     return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': cart_counter(request), 'qty': CheckKart.quantity, 'cart_amount': get_cart_amounts(request)})
#             except FoodItem.DoesNotExist:
#                 return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
#             except Exception as e:
#                 print(e)  
#         else:
#             return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
#     else:
#         return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

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
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': cart_counter(request), 'qty': CheckKart.quantity})
                    
                except ObjectDoesNotExist:
                    CheckKart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': cart_counter(request), 'qty': CheckKart.quantity})
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
                    return JsonResponse({'status': 'Success', 'cart_counter': cart_counter(request), 'qty': CheckKart.quantity})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')   #order by creaed at while listing it
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})


