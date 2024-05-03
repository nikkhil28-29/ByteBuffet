from django.contrib import admin
from .models import Vendor, OpenHour

class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')
    list_editable = ('is_approved',)

class OpenHourAdmin(admin.ModelAdmin):
    list_display=('vendor', 'day', 'from_hour', 'to_hour')

# Register your models here.
admin.site.register(Vendor,VendorAdmin)
admin.site.register(OpenHour,OpenHourAdmin)
