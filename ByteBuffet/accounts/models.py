from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,User
from django.db.models.fields.related import OneToOneField
from django.conf import settings

class MyUserManager(BaseUserManager): #it does not contain any fields ,,,it will contain only merhods
    def create_user(self, email, first_name,last_name, username,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("username must have an username")


        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name,username=username)

        user.set_password(password) #hashing the password before storing it in the database.
        user.save(using=self._db) #This saves the user object to the database.
        return user

    def create_superuser(self, email, first_name, last_name,username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name,username=username)
        user.is_admin = True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True

        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    VENDOR=1
    CUSTOMER=2

    ROLE_CHOICE=(
        (VENDOR,'Vendor'),
        (CUSTOMER,'Customer'),
    )


    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    phone_number=models.CharField(max_length=12, blank=True)

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True,null=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name","last_name",]


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def get_role(self):
        if self.role==1:
            user_role='Vendor'
        elif self.role==2:
            user_role='Customer'

        return user_role
    
    # def set_password(self, raw_password):
    # # Override the set_password method to prevent password changes by admin
    #     if self.id is not None and self.is_admin:
    #         return  # Do not allow password changes by admin
    #     super().set_password(raw_password)
    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin



class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='users/profile_pics/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos/', blank=True, null=True)
    address_1 = models.CharField(max_length=255, blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.FloatField(max_length=20,blank=True, null=True)
    longitude = models.FloatField(max_length=20,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)




    def __str__(self):
        return self.user.email
    
    # def full_address(self):
    #     return f'{self.address_1} , {self.address_2}'
    def full_address(self):
    # Check if address_1 and address_2 are not None or empty
        address_parts = [part for part in [self.address_1, self.address_2] if part]

    # Join the non-empty parts with a comma and space
        return ', '.join(address_parts)


# post_save.connect(post_save_create_profile_receiver,sender=MyUser)