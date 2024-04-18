from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

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
        redirectUrl =reverse('vendordashboard')
        return redirectUrl
    elif user.role == 2:
        redirectUrl =reverse('customerdashboard')
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = ('/admin')
        return redirectUrl
    

def send_verification_email(request,user,mail_subject, email_template): # afte it activating funvtion is in views.py
    from_email = settings.DEFAULT_FROM_EMAIL
                                                                    # from_email = 'XXXXXXX@gmail.com'
    
    current_site = get_current_site(request)                        #Site object or a RequestSite object. This variable can be used to access the domain and name attributes of the current site.
    message = render_to_string(email_template,{    
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),          #The token is used to verify that the user is the one who requested the verification email
    })
    to_email=user.email
    print("FROM_EMAIL:", from_email)
    print("TO_EMAIL:", to_email)

    mail=EmailMessage(mail_subject,message,from_email,to=[to_email]) #package to send emil
    mail.content_subtype='html'                                      # means that the message content is in HTML format and not plain text.
    try:
        mail.send()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

from email_validator import validate_email, EmailNotValidError

def check(email):
    try:
        # Validate the email address
        email = validate_email(email).email
        print("True")
    except EmailNotValidError as e:
        # Print the error message
        print(str(e))


def send_notification_approve(mail_subject, mail_template, context):

    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template,context)
    
    if(isinstance(context['to_email'], str)):
        
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']

        print("FROM_EMAIL:", from_email)
        print("TO_EMAIL:", to_email)
        # email = validate_email(to_email).email
        # print("True")
        # print(str(e))


    try:
        # Validate email if it's a string
        if isinstance(to_email, str):
            email = validate_email(to_email).email
            to_email = [email]

        mail = EmailMessage(mail_subject, message, from_email, to=to_email)
        mail.content_subtype = 'html'
        mail.send()
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")
    
  

    


