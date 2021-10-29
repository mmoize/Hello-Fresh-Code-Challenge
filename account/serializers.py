  
from rest_framework import serializers
from authentication.serializers import UserSerializer
from menu_plan.serializers import WeeklymenuSerializer
from .models import Profile



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    url = serializers.HyperlinkedRelatedField(view_name="account:profile-detail", read_only=True, lookup_field="pk")
    weeklymenu = WeeklymenuSerializer(view_name="menu_plan:weeklymenu-detail", read_only=True, source="weeklymenu")
    class Meta:
        model = Profile
        fields = ['url', 'id','user','username', 'week', 'weekly_menu']

    
    