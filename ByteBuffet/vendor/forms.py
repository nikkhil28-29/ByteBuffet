from django import forms
from .models import Vendor, OpenHour

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField( required=True,widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']

class OpenHourForm(forms.ModelForm):

    class Meta:
        model=OpenHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
        


    