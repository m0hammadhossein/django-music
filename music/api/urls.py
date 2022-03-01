from django.urls import path
from music.api.views import SongApiView, CommentApiView

urlpatterns = [
    path('', SongApiView.as_view(), name='song-api'),
    path('comment/<int:pk>/', CommentApiView.as_view(), name='comment-api'),
]
