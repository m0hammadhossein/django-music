from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from music.api.serializers import SongSerializer, CommentSerializer
from music.models import Song, Comment


class SongApiView(ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'text', 'artist')
    ordering_fields = ('created_on', 'likes')


class CommentApiView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created_on',)

    def get_queryset(self):
        return Comment.objects.filter(song__pk=self.kwargs['pk'], active=True, parent__isnull=True)

    def perform_create(self, serializer):
        song = get_object_or_404(Song, pk=self.kwargs['pk'])
        serializer.save(song=song, user=self.request.user)


class ReplyCommentApiView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    ordering_fields = ('created_on',)

    def get_queryset(self):
        return Comment.objects.filter(parent__pk=self.kwargs['pk'], active=True)

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'], parent__isnull=True)
        serializer.save(song=comment.song, parent=comment, user=self.request.user)
