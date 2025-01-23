from django.test import TestCase
from datetime import date, timedelta
from .models import Reservation, Room
from django.contrib.auth.models import User

class CheckExpiredTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testusername", password="testpassword")
        self.room = Room.objects.create(room_name="A4", room_type="Single", room_status="Booked", room_price=300)

    def test_check_expired(self):
        reservation1 = Reservation.objects.create(
            user=self.user,
            room=self.room,
            checkin_date=date.today() - timedelta(days=6),
            checkout_date=date.today() - timedelta(days=5),
            is_expired=False
        )
        reservation1.check_expired()
        
        
        
        self.assertEqual(self.room.room_status,"Available")
        self.assertTrue(reservation1.is_expired)
        self.assertFalse(not reservation1.is_expired)
