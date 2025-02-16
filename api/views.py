from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer,RoomSerializer,AmenitySerializer,FeatureSerializer,ReservationSerializer,UserSerializer,SingleRoomSerializer
from .models import Room,Feature,Amenity,Reservation
from rest_framework import status
from django.db import transaction
from django.http import HttpResponse

def html_view(request):
    return HttpResponse("<h1>Welcome to My Site</h1>")
class CustomTokenObtainPairView(TokenObtainPairView):
  serializer_class=CustomTokenObtainPairSerializer


class RoomView(APIView):
  permission_classes=[AllowAny]
  def get(self,request):
    rooms=Room.objects.filter(room_status="Available")
    roomserializer=RoomSerializer(rooms,many=True)
    return Response(roomserializer.data,status=status.HTTP_200_OK)
    
class SingleRoomView(APIView):
  permission_classes=[AllowAny]
  def get(self,request,pk):
    try:
      room=Room.objects.get(id=pk)
    except Room.DoesNotExist:
      return Response({"error":"room not found"},status=status.HTTP_404_NOT_FOUND)
    roomserializer=SingleRoomSerializer(room)
    
    return Response(roomserializer.data,status=status.HTTP_200_OK)
    
class BookReservationView(APIView):
  permission_classes=[IsAuthenticated]
  
  @transaction.atomic
  def post(self,request,pk):
    user=request.user
    try:
      room=Room.objects.get(id=pk)
    except Room.DoesNotExist:
      return Response({"error":"room does not exist"},status=status.HTTP_404_NOT_FOUND)
    serializer=ReservationSerializer(data=request.data,context={"room":room})
    if serializer.is_valid():
      reservation=Reservation(user=user,room=room,checkin_date=serializer.validated_data["checkin_date"],checkout_date=serializer.validated_data["checkout_date"])
      room.room_status="Booked"
      room.save()
      reservation.save()
      return Response({"message":"reservation booked"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CheckReservationView(APIView):
  permission_classes=[IsAuthenticated]
  def get(self,request):
    reservations=Reservation.objects.filter(user=request.user)
    for reservation in reservations:
      reservation.check_expired()
    reservationserilizer=ReservationSerializer(reservations,many=True)
    
    return Response(reservationserilizer.data,status=status.HTTP_200_OK)
    
class CancelReservationView(APIView):
  permission_classes=[IsAuthenticated]
  def delete(self,request,pk):
    try:
      reservation=Reservation.objects.get(id=pk)
      if reservation.user != request.user:
        return Response({"error":"you dont have permission to cancel this reservation"},status=status.HTTP_403_FORBIDDEN)
      reservation.room.room_status="Available"
      reservation.room.save()
      reservation.delete()
      return Response({"message":"Reservation deleted successfully"},status=status.HTTP_200_OK)
    except Reservation.DoesNotExist:
      return Response({"error":"Reservation does not exists"},status=status.HTTP_404_NOT_FOUND)
      
class RegisterView(APIView):
  def post(self,request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)