from django.contrib import admin
from .models import Amenity,Feature,Room,Reservation,RoomImage

admin.site.register(Amenity)
admin.site.register(Feature)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(RoomImage)
