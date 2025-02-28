from django.db import models
from django.contrib.auth.models import User
from datetime import date
from cloudinary.models import CloudinaryField

class Amenity(models.Model):
  AMENITY_CATEGORIES=[
    ("Room Amenities","Room Amenities"),
    ("Bathroom Amenities","Bathroom Amenities"),
    ("Dining Amenities","Dining Amenities"),
    ("Leisure and Entertainment Amenities","Leisure and Entertainment Amenities"),
    ("Business Amenities","Business Amenities"),
    ("General Hotel Amenities","General Hotel Amenities"),
    ("Outdoor and Recreational Amenities","Outdoor and Recreational Amenities")
  ]
  amenity_name=models.CharField(max_length=50)
  amenity_category=models.CharField(max_length=100,choices=AMENITY_CATEGORIES)
  
  def __str__(self):
    return self.amenity_name
  
class Feature(models.Model):
  FEATURE_CATEGORIES=[
    ("Safety and Security","Safety and Security"),
    ("Accessibility Features","Accessibility Features"),
    ("Technology Features","Technology Features"),
    ("Sustainability Features","Sustainability Features"),
    ("Design and Aesthetic Features","Design and Aesthetic Features")
  ]
  feature_name=models.CharField(max_length=50)
  feature_category=models.CharField(max_length=70,choices=FEATURE_CATEGORIES)
  
  def __str__(self):
    return self.feature_name

class Room(models.Model):
  ROOM_TYPE=[("Single","Single"),
            ("Double","Double"),
            ("Suite","Suite")]
  
  ROOM_STATUS=[("Available","Available"),
              ("Booked","Booked")]
  room_name=models.CharField(max_length=50)
  room_type=models.CharField(max_length=40,choices=ROOM_TYPE)
  room_status=models.CharField(max_length=40,choices=ROOM_STATUS)
  room_price=models.FloatField(default=0)
  room_description=models.TextField(blank=True,null=True)
  room_amenities=models.ManyToManyField(Amenity,related_name="amenities")
  room_features=models.ManyToManyField(Feature,related_name="features")
  
  def __str__(self):
    return self.room_name
    
class RoomImage(models.Model):
  room=models.ForeignKey(Room,related_name="images",on_delete=models.CASCADE)
  image=CloudinaryField("image")
  def __str__(self):
    return f"for {self.room.room_name}"
  
class Reservation(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
  room=models.ForeignKey(Room,on_delete=models.CASCADE,related_name="room")
  checkin_date=models.DateField()
  checkout_date=models.DateField()
  is_expired=models.BooleanField(default=False)
  
  def delete(self,*args,**kwargs):
    if(self.room.room_status=="Booked"):
      self.room.room_status="Available"
      self.room.save()
    super().delete(*args,**kwargs)
    
  def check_expired(self):
    today = date.today()
    if self.checkout_date < today and not self.is_expired:
      self.room.room_status="Available"
      self.is_expired=True 
      self.room.save()
      self.save()
      
    if self.checkout_date > today and self.is_expired:
      self.is_expired=False
      self.room.room_status="Booked"
      self.room.save()
      self.save()
  
  def __str__(self):
    return f"Reservation for room {self.room} by {self.user}"

