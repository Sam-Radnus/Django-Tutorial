from django.shortcuts import render
from .models import Room
# Create your views here.


# rooms = [
#     {'id':1,'name':'lets learn python!'},
#     {'id':2,'name':'lets learn django!'},
#     {'id':3,'name':'lets learn flask!'},
# ]
def home(request):
    #objects-model manager
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(request,'base/home.html',context)
#pk=primary key
def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}        
    return render(request,'base/room.html',context)   


