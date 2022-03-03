from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from music.api.permissions import IsUserComment
from music.api.serializers import SongListSerializer, CommentSerializer, SongRetrieveSerializer
from music.models import Song, Comment


class SongListApiView(ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'text', 'artist')
    ordering_fields = ('created_on', 'likes')

class SongRetrieveApiView(RetrieveAPIView):
    serializer_class = SongRetrieveSerializer
    queryset = Song.objects.all()

class CommentsApiView(ListCreateAPIView):
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
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created_on',)

    def get_queryset(self):
        return Comment.objects.filter(parent__pk=self.kwargs['pk'], active=True)

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'], parent__isnull=True)
        serializer.save(song=comment.song, parent=comment, user=self.request.user)


class LikeAPiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        if not request.user.liked_posts.filter(pk=pk).exists():
            song = get_object_or_404(Song, pk=pk)
            song.users.add(request.user)
            song.likes += 1
            song.save()
            return Response({'status': 'ok'}, status=201)
        return Response({'status': 'already liked'}, status=200)

    def delete(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        try:
            request.user.liked_posts.remove(song)
            song.likes -= 1
            song.save()
            return Response(status=204)
        except:
            raise Http404


class CommentApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsUserComment,)
