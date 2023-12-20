from email.policy import default
from unicodedata import name
from xml.dom.minidom import Document
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from matplotlib.pyplot import cla
'''
class user(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    uname = models.CharField(max_length=255)
    number = models.IntegerField()
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    regid = models.CharField(max_length=50, blank=True,null=True)
    voted = models.BooleanField(default=False,blank=True,null=True)


'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''
class constestant(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    regeid = models.CharField(max_length=255)
    positions = models.CharField(max_length=255)
    potrait = models.ImageField(upload_to='media/')
    thedocument = models.ImageField(upload_to='media/')
    approved =models.BooleanField(default=False)
    votes = models.IntegerField(default=0)


class admin(models.Model):
    namr = models.CharField(max_length=255)



# Create your models here.
