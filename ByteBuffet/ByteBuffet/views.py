from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor


#Only the actual registered vendor(also active/approved) will be listed on home page:::
def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    return render(request, 'home.html', {'vendors': vendors})                   #or use context 
