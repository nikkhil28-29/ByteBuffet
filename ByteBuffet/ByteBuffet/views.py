from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor

def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8] #ONLY 8 RESULT WILL BE SHOE=WN IN HTML
    return render(request, 'home.html', {'vendors': vendors}) #or use context 
