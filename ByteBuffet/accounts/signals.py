from django.db.models.signals import post_save ,pre_save
from django.dispatch import receiver 
from .models import MyUser,UserProfile

@receiver(post_save,sender=MyUser)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('user profilr')

    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            print("user profile is created")
        except:
            UserProfile.objects.craete(user=instance)
            print("profile was not exist , But i ceated one")
        print('User is updated')


@receiver(pre_save, sender=MyUser)
def pre_save_profile_receiver(sender,instance,**kwargs):
    print(instance.username,'this user is being saved')