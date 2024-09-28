from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import traceback
# from verify_email.email_handler import send_verification_email
from slugify import slugify
from django.contrib.auth.tokens import default_token_generator

from django.utils.http import urlsafe_base64_decode

from django.core.exceptions import PermissionDenied

from .utils import detectUser ,send_verification_email

from django.http import HttpResponse
from .forms import UserForm
from .models import MyUser ,UserProfile
from vendor.forms import VendorForm
from vendor.models import Vendor
from django.contrib import messages #import messages


# Create your views here.
def registerUser(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():

            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']

            user=MyUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=MyUser.CUSTOMER    ## impr
            user.save()

            #send mail
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification.html'
            send_verification_email(request, user, mail_subject, email_template) #this function is made in utils 
            
            messages.success(request, "Your Accout has been succesfull regsiterd🍻." )
            
        else:
            print("error")
            messages.error(request, "Error. Form not sumitted😣.")


    else:
        form = UserForm()  

    context = {
        'form': form,
    }
    return render(request, 'accounts/registrationUser.html', context)



def registerVendor(request):
    if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in.')
            return redirect('dashboard')
   
    elif request.method == 'POST':

        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # vendor_license=
            user = MyUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = MyUser.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug=slugify(vendor_name)+"-"+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification.html'
            
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
            print(v_form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)

from django.contrib import auth
from django.contrib import messages

def login(request):
    try:
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in.')
            return redirect('myAccount')
        
        elif request.method == 'POST':
            # email = request.POST.get("email").strip()
            password = request.POST.get("password").strip() #strip()removes any leading, whitespace from the passw,.
            username = request.POST.get("username").strip()

            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print("Email:", username)
                print("Password:", password)
      

                messages.success(request, 'Login successful.')
                return redirect('myAccount')     # my accountT view function is created below
            else:
                print("Email:", username)
                print("Password:", password)
                messages.error(request, 'Invalid email or password. Please try again.')
                
        else:
            return render(request, 'accounts/login.html')  # Add this line for GET requests
    except Exception as e:
        traceback.print_exc()
        messages.error(request, 'An error occurred during login. Please try again.')
    return render(request, 'accounts/login.html')
 
@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('home')

@login_required(login_url='login')
def myAccount(request):               #redirect to customer/vendor dashboard
    user = request.user
    redirectUrl = detectUser(user)    #detectUser is in utils.py(helper.py)
    return redirect(redirectUrl)

# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

@login_required(login_url='login')  
@user_passes_test(check_role_customer)   #made  check_role_customer above 

def customerdashboard(request):
    return render(request, 'accounts/customerdashboard.html')
    

@login_required(login_url='login') 
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    vendor=Vendor.objects.get(user=request.user)
    context={
        'vendor':vendor,
    }
    return render(request, 'accounts/vendordashboard.html',context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = MyUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
    
#forgot password
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_pass_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forget_password.html')


def reset_password_validate(request, uidb64, token):
    # validte the user by decoding the token and user pk , respond o link sent to mail
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = MyUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = MyUser.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')