from django.urls import path

from .views import UserProfileView


app_name = 'account'



userprofileview_detail = UserProfileView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})



urlpatterns = [
    path('profile/<int:id>/', userprofileview_detail,name='userprofileview_detail'),
]