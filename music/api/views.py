from rest_framework.generics import ListAPIView
from music.api.serializers import SongSerializer
from music.models import Song


class SongApiView(ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer