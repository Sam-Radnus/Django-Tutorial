from urllib.request import Request
from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic
from .forms import RoomForm
# Create your views here.


# rooms = [
#     {'id':1,'name':'lets learn python!'},
#     {'id':2,'name':'lets learn django!'},
#     {'id':3,'name':'lets learn flask!'},
# ]

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')


    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:   
            user=User.objects.get(username=username)
        except:
           messages.error(request, 'User does not exist')
        user=authenticate(request,username=username,password=password)  
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Credentials Dont Match') 
    context={'page':page}
    return render(request,'base/login_register.html',context)
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) # to save the state of the data entered in order to prevent the user from entering erroneus input
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'error occurred')    
    return render(request,'base/login_register.html',{'form':form})    
def home(request):
    #objects-model manager
    q=request.GET.get('q') if request.GET.get('q')!=None else '' #whatever we passed onto the url 
    
    rooms=Room.objects.filter(
        Q(topic__name__contains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )

    topics=Topic.objects.all()
    room_count=rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html',context)
#pk=primary key
def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}        
    return render(request,'base/room.html',context)   

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user!=room.host:
        return HttpResponse('You are Tresspassing!!!')

    if request.method == 'POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')    
    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse('You are Tresspassing!!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

