from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("room/",views.RoomView.as_view()),
    path("room/<int:pk>",views.SingleRoomView.as_view()),
    path("reservation/<int:pk>/",views.BookReservationView.as_view()),
    path("check-reservation/",views.CheckReservationView.as_view()),
    path("cancel-reservation/<int:pk>",views.CancelReservationView.as_view()),
    path("register/",views.RegisterView.as_view())
]
