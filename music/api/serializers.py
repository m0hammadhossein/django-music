from rest_framework import serializers
from music.models import Song, Comment


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    created_on = serializers.CharField(source='tms_created_on', read_only=True)

    def get_user(self, obj):
        return (obj.user.get_full_name() or obj.user.username)

    class Meta:
        model = Comment
        exclude = ('parent', 'song', 'active')
        read_only_fields = ('reply_count', 'user')
