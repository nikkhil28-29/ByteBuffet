# from enum import unique
from django.db import models
from accounts.models import MyUser, UserProfile
from accounts.utils import send_notification_approve
from datetime import time, date, datetime


class Vendor(models.Model):
    user = models.OneToOneField(MyUser, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True) 
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    

    #over riding the save method(to update any intance of model) in djnago by custom save method
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    
                    mail_subject = "Congratulations! Your restaurant has been approved 🍻."
                    send_notification_approve(mail_subject, mail_template, context)
                else:
                   
                    mail_subject = "We're sorry! You are not eligible for marketplace."
                    send_notification_approve(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)

DAYS=[
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday"))
]

CONTACT_HOURS = [(time(h, m).strftime("%I:%M %p"), time(h, m).strftime("%I:%M %p")) for h in range(0, 24) for m in range(0, 60, 30)]



class OpenHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)  # manyto many relations
                                                                    
    day = models.IntegerField(choices=DAYS)
    from_hour=models.CharField(choices=CONTACT_HOURS, max_length=10, blank=True)
    to_hour=models.CharField(choices=CONTACT_HOURS, max_length=10, blank=True)
    is_closed=models.BooleanField(default=False)

    class Meta:
        ordering =('day', 'from_hour')
        unique_together=('day', 'from_hour', 'to_hour')
 