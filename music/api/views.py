from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from music.api.serializers import SongSerializer, CommentSerializer
from music.models import Song, Comment


class SongApiView(ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('title', 'text', 'artist')

class CommentApiView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(song__pk=self.kwargs['pk'], active=True)