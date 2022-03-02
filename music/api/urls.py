from django.urls import path
from music.api.views import SongApiView, CommentApiView, ReplyCommentApiView

urlpatterns = [
    path('', SongApiView.as_view(), name='song-api'),
    path('comment/<int:pk>/', CommentApiView.as_view(), name='comment-api'),
    path('rcomment/<int:pk>/', ReplyCommentApiView.as_view(), name='rcomment-api'),
]
