from django.urls import path
from music.api.views import SongListApiView, CommentApiView, ReplyCommentApiView, LikeAPiView, SongRetrieveApiView, \
    CommentUpdate, CommentsApiView

urlpatterns = [
    path('', SongListApiView.as_view(), name='song-list-api'),
    path('song/<int:pk>/', SongRetrieveApiView.as_view(), name='song-retrieve-api'),
    path('comment/<int:pk>/', CommentsApiView.as_view(), name='comment-api'),
    path('comment/view/<int:pk>/', CommentApiView.as_view(), name='comment-api'),
    path('rcomment/<int:pk>/', ReplyCommentApiView.as_view(), name='rcomment-api'),
    path('like/<int:pk>/', LikeAPiView.as_view(), name='like-api'),
]
