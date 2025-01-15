from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Amenity,Feature,Room,Reservation,RoomImage
from datetime import date
from django.contrib.auth.models import User


class AmenitySerializer(serializers.ModelSerializer):
  class Meta:
    model=Amenity
    fields="__all__"

class FeatureSerializer(serializers.ModelSerializer):
  class Meta:
    model=Feature
    fields="__all__"

class RoomImageSerializer(serializers.ModelSerializer):
  class Meta:
    model=RoomImage
    exclude=["room"]

class RoomSerializer(serializers.ModelSerializer):
  room_features=FeatureSerializer(many=True)
  room_amenities=AmenitySerializer(many=True)
  images=RoomImageSerializer(many=True)
  class Meta:
    model=Room
    fields=["id","room_name","room_type","room_status","room_price","room_description","room_amenities","room_features","images"]
    
class RoomData(serializers.ModelSerializer):
  class Meta:
    model=Room
    fields=["id","room_name"]

class ReservationSerializer(serializers.ModelSerializer):
    room=RoomData(read_only=True)
    class Meta:
        model = Reservation
        fields=["id","room","checkin_date","checkout_date"]

    def validate(self, data):
        checkin_date = data.get('checkin_date')
        checkout_date = data.get('checkout_date')
        room = self.context.get('room')  # Pass the room instance through the context

        # Check if reservation is in the past
        today = date.today()
        if checkin_date < today:
            raise serializers.ValidationError({"checkin_date":"Check-in date cannot be in the past."})
        
        if checkout_date < today:
            raise serializers.ValidationError({"checkout_date":"Check-out date cannot be in the past."})
        
        # Check if checkout is after checkin
        if checkin_date >= checkout_date:
            raise serializers.ValidationError({"checkout_date":"Checkout date must be after check-in date."})
        
        # Check for overlapping reservations
        overlapping_reservations = Reservation.objects.filter(
            room=room,
            checkin_date__lt=checkout_date,  # Existing check-in is before the new checkout
            checkout_date__gt=checkin_date   # Existing checkout is after the new check-in
        )
        
        if overlapping_reservations.exists():
            raise serializers.ValidationError({"overlap":"This room is already reserved for the selected dates."})
        
        return data
        
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model=User
    fields=["email","password","username"]
    extra_kwargs={"password":{"write_only":True}}
  def validate(self,data):
    email=data.get("email")
    username=data.get("username")
    
    if User.objects.filter(email=email).exists():
      raise serializers.ValidationError({"email":"Email already exist"})
      
    elif User.objects.filter(username=username).exists():
      raise serializers.ValidationError({"username":"username already exist"})
      
    return data
    
  def create(self,validated_data):
    password=validated_data.pop("password")
    user=User(**validated_data)
    user.set_password(password)
    user.save()
    return user
 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"]=user.email
        return token
