from django.urls import path
from music.api.views import SongApiView

urlpatterns = [
    path('', SongApiView.as_view(), name='song-api'),
]
