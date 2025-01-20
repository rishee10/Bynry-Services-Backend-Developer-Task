from django.urls import path
from .views import LoginView, RegisterView, LogoutView, SubmitRequestView, TrackRequestsView, ManageRequestsView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('submit_request/', SubmitRequestView.as_view(), name='submit_request'),
    path('track_requests/', TrackRequestsView.as_view(), name='track_requests'),
    path('manage_request/', ManageRequestsView.as_view(), name='manage_request'),
]
