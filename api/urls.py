from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path
from . import views

urlpatterns = [
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/room/",views.RoomView.as_view()),
    path("api/room/<int:pk>/",views.SingleRoomView.as_view()),
    path("reservation/<int:pk>/",views.BookReservationView.as_view()),
    path("api/check-reservation/",views.CheckReservationView.as_view()),
    path("api/cancel-reservation/<int:pk>/",views.CancelReservationView.as_view()),
    path("api/register/",views.RegisterView.as_view()),
    path("",views.html_view,name="home")
]
