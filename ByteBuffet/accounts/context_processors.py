# to render te profile datas from cover.html to all(dashboar,orders,...)

from accounts.models import UserProfile
from vendor.models import Vendor

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None  # when i click signout, it will not showw an erorr, raher tha it will log out
    return dict(vendor=vendor)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)

