from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import MyUser
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

