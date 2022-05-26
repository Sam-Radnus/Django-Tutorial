from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True,null=True)
    bio=models.TextField(null=True)
     
    avatar=models.ImageField(null=True,default="avatar.svg")

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =[]


#Create your models here.
#id for models are automatically generated /default :1,2
class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True) #if topic was placed below Room then we must put Topic under Singles Commas i.e 'Topic',on_delete=models.CASCADE
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True);
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    like=models.ManyToManyField(User,related_name='like',blank=True)
    updated =models.DateTimeField(auto_now=True)   #automatic 
    created =models.DateTimeField(auto_now_add=True)  #it will only save a value once i.e the time it is created
      

    class Meta:
        ordering = ['-updated','-created']  # '-' puts the new data field before all the prefilled data
    def __str__(self):
        return self.name

class Message(models.Model):
    #CASCADE means if the room gets deleted all the messages corresponding to that room gets deleted
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated','-created']  # '-' puts the new data field before all the prefilled data
     
        def __str__(self):
            return self.body[0:50]