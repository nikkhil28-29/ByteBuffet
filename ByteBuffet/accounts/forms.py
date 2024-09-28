from django import forms
from .models import UserProfile,MyUser
from .validators import allow_only_images_validator    #from account.py 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=MyUser
        fields=["first_name","last_name","username","email","phone_number","password"]

    def clean(self):
        cleaned_data=super(UserForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get("confirm_password")

        if password!=confirm_password:
            raise forms.ValidationError("Password is not same")
        
        if len(password) < 8:
            raise forms.ValidationError("Password must contain at least 8 characters")
        
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter")
        
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one numeric digit")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in password):
            raise forms.ValidationError("Password must contain at least one special character")
        
        return cleaned_data
        

#For vendor profile update by itself from website
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Addresssssssss', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'phone_number']

    