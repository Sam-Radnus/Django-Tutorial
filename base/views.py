import email
from venv import create
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from .forms import MyUserCreationForm
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm

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
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:   
            user=User.objects.get(email=email)
        except:
           messages.error(request, 'User does not exist')
        user=authenticate(request,email=email,password=password)  
        print(user)
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
    form=MyUserCreationForm()
    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) # to save the state of the data entered in order to prevent the user from entering erroneus input
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            print(form)
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

    topics=Topic.objects.all()[0:5]  #to limit the number of topics shown to 5
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    

    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

#pk=primary key
def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method=='POST':
       message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
       )
     
       room.participants.add(request.user)
       #room.like.add(1)
       return redirect('room',pk=room.id)
    stuff=get_object_or_404(Room,id=pk)
    total_likes=stuff.total_likes()
    context={'room':room,'room_messages':room_messages,'participants':participants,'total_likes':total_likes}        
    return render(request,'base/room.html',context)   

    
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room=Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        
        print(room.id)
        if 'next' in request.POST:
            print("/",request.POST.get('id'))
        return redirect('room',pk=room.id)
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user!=room.host:
        return HttpResponse('You are Tresspassing!!!')

    if request.method == 'POST':
       topic_name=request.POST.get('topic')
       topic,created=Topic.objects.get_or_create(name=topic_name)
       room.name=request.POST.get('name')
       room.topic=topic
       room.description=request.POST.get('description')
       room.save()
       return redirect('home')    
    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host: #Redundant
        return HttpResponse('You are Tresspassing!!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    print(":",request)
    message=Message.objects.get(id=pk)

    if request.user!=message.user: #Redundant
        return HttpResponse('Invalid Operation!!!')
    if request.method == 'POST':
        if 'prev' in request.POST:
            print("/",request.POST.get('prev'))
            message.delete() 
            return redirect(request.POST.get('prev'))   
        print("?",request)
        message.delete() 
        return redirect('home')   
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method=='POST':
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            
            return  redirect ('user-profile',pk=user.id)
    return render(request,'base/update_user.html',{'form':form})

def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else '' #whatever we passed onto the url 
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})

def activityPage(request):
    room_messages=Message.objects.all()                       
    return render(request,'base/activity.html',{'room_messages': room_messages})    
# def like(request):
#     new_like,created=like.objects.get_or_create(user=request.user)
#     if not created:
#        pass
#     else:
#        pass
def LikeView(request,pk):
    post=get_object_or_404(Room,id=request.POST.get('post_id'))
    print(post.likes)
    liked,new_like=Room.objects.get_or_create(id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
       post.likes.remove(request.user)
    else:
       post.likes.add(request.user)#save the likes to the table along with the user  
    return redirect('room',pk)