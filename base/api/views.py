from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.api.serializers import RoomSerializer
from base.models import Room
from .serializers import RoomSerializer
 
@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes) # turns the list to corresponding JSON format

@api_view(['GET'])   #it will only allow GET request
def getRooms(request):
    rooms=Room.objects.all()
    serializer=RoomSerializer(rooms,many=True) # many defines are we serializing multiple objects or we serializing one
    return Response(serializer.data)

@api_view(['GET'])   #it will only allow GET request
def getRoom(request,pk):
    room=Room.objects.get(id=pk)
    serializer=RoomSerializer(room,many=False) # it will return a single object
    return Response(serializer.data)