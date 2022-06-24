from rest_framework import serializers
from .models import Profile
from followers.models import Follower
from likes.models import Like
from django.db.models import Count

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            # print(following)
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
                 'id', 'owner', 'created_at', 'updated_at',
                 'name', 'content', 'image', 'is_owner', 
                 'following_id',
        ]
