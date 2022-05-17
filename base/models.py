from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# id for models are automatically generated /default :1,2
class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True) #if topic was placed below Room then we must put Topic under Singles Commas i.e 'Topic',on_delete=models.CASCADE
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True);
    #participants=
    updated =models.DateTimeField(auto_now=True)   #automatic 
    created =models.DateTimeField(auto_now_add=True)  #it will only save a value once i.e the time it is created

    def __str__(self):
        return self.name

class Message(models.Model):
    #CASCADE means if the room gets deleted all the messages corresponding to that room gets deleted
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]