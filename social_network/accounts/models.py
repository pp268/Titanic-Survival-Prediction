from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
GENDER_CHOICES = (('Male','Male'), ('Female','Female'))


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    dob =models.DateField(blank=True ,default='1990-01-01')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="Male",blank=False)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True,default='34AD2.jpg')
    city=models.CharField(max_length=100,blank=True,null=True)
    about=models.CharField(max_length=100,blank=True,default='')
    work=models.CharField(max_length=100,blank=True,default='')
    def __str__(self):
        return self.user.username

    # def save(self):
    #     super().save()
    #
    #     img=Image.open(self.profile_pic.path)
    #
    #     if img.height >500 or img.width >500:
    #         output_size=(500,500)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pic.path)
def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile=Profile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile,sender=User)
