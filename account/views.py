from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from account.models import Profile
from core.utils import MultipartJsonParser
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import ProfileSerializer



class UserProfileView(ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    parser_classes = [MultipartJsonParser, JSONParser]
    lookup_field = "id"

    def get_serializer_context(self):
        context = super(UserProfileView, self).get_serializer_context()
        if len(self.request.data) > 0:
                context.update({
                'Profile_Data': self.request.data
            })

        return context

