from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import MyUser ,UserProfile
from vendor.forms import VendorForm
from django.contrib import messages #import messages


# Create your views here.
def registerUser(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():

            # password=form.cleaned_data['password']
            # user=form.save(commit=False) # form is not yet submited , yet to submit

            # user.set_password(password)

            # user.role=MyUser.CUSTOMER
            # user.save()

            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']

            user=MyUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=MyUser.CUSTOMER
            user.save()
            
            messages.success(request, "Your Accou t has been succesfull regsiterd🍻." )
            
        else:
            print("error")
            messages.error(request, "Error. Form not sumitted😣.")


    else:
        form = UserForm()  

    context = {
        'form': form,
    }
    return render(request, 'accounts/registrationUser.html', context)


# def registerVendor(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         v_form=VendorForm(request.POST,request.FILES)

#         if form.is_valid() and v_form.is_valid():
#             user = form.save(commit=False)
#             user.role = MyUser.VENDOR
#             user.save()

#             # Save the vendor information
#             vendor = v_form.save(commit=False)
#             vendor.user = user  # Link the vendor to the user
#             vendor.save()

#             messages.success(request, "Vendor registration successful 🎉.")

#             # return redirect('home')

            
#         else:
#                 print("error")
#                 messages.error(request, "Error. Form not sumitted😣.")



#     else:
#         form = UserForm()
#         v_form=VendorForm()


#         context={
#             'form':form,
#             'v_form':v_form,
#         }

#         return render(request,'accounts/registerVendor.html',context)

def registerVendor(request):
   
    if request.method == 'POST':

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
            # vendor_name = v_form.cleaned_data['vendor_name']
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

         
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