from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name=models.CharField(max_length=150,unique=True)
    description=RichTextUploadingField()

# Create your models here.
class Book(models.Model):
    name=models.CharField(max_length=150)
    description=RichTextUploadingField()
    brand=models.CharField(max_length=150)
    date=models.DateField()
    file=models.FileField(upload_to='MyFile/',blank=True,null=True)
    catogery=models.ForeignKey(to='Category',to_field='name',on_delete=models.CASCADE,blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)
    takhfif=models.IntegerField(blank=True,null=True)
    image=models.ImageField(upload_to='image/',blank=True,null=True)

    def get_absolute_url(self):
        return reverse("myApp:detail",kwargs={"pk" : self.id})

    




class Suggestion(models.Model):
    name=models.CharField(max_length=150)
    email=models.EmailField()
    description=RichTextUploadingField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email=models.EmailField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Reserve(models.Model):
    user=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    price = models.IntegerField(blank=True, null=True)
    takhfif = models.IntegerField(blank=True, null=True)
    quantity=models.IntegerField(blank=True, null=True)
    sell=models.BooleanField(default=False)
    brand = models.CharField(max_length=150,blank=True, null=True)
