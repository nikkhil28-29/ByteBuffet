from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor


from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

#when i will refresh my , no need to give th my location to get near by restaurant on hom page 
#it will take stoarge from session storage
def get_set_curr_loc(request):
    if 'lat' in request.session:
        lat=request.session['lat']
        long=request.session['long']
        return long, lat
    elif 'lat' in request.GET:
        lat=request.GET.get('lat')
        long=request.GET.get('long')
        request.session['lat']=lat
        request.session['long']=long
        return long ,lat
    else:
        return None
        


#Only the actual registered vendor(also active/approved) will be listed on home page:::
def home(request):
    if get_set_curr_loc(request) is not None:
        lat=request.GET.get('lat')
        long=request.GET.get('long')
        
        # pnt=GEOSGeometry('POINT(%s %s)'% (long, lat))
        pnt=GEOSGeometry('POINT(%s %s)'% (get_set_curr_loc(request)))
        
        # all the vendor (id) which have the food , which have searched for
        vendors=Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=150))).annotate(distance1=Distance("user_profile__location", pnt)).order_by("distance1") #user_profile has location field
        #order the listed items by distance          #__lte= (<=)

        for i in vendors:
                i.kms = round(i.distance1.km, 2)    
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    return render(request, 'home.html', {'vendors': vendors})                   #or use context 
