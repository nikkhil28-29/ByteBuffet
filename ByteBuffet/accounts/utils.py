from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.core.mail import EmailMessage, message

from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    

def send_verification_email(request,user,mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    # from_email = 'bytebuffet00@gmail.com'


    current_site = get_current_site(request)
    message = render_to_string(email_template,{
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email=user.email
    print("FROM_EMAIL:", from_email)
    print("TO_EMAIL:", to_email)

    mail=EmailMessage(mail_subject,message,from_email,to=[to_email]) #package to send emil
    mail.content_subtype='html'
    try:
        mail.send()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    # mail.send()
        