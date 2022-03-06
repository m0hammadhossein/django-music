from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from music.api.views import SongListApiView, CommentApiView, ReplyCommentApiView, LikeAPiView, SongRetrieveApiView, \
    CommentsApiView

urlpatterns = [
    path('', SongListApiView.as_view(), name='song-list-api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('song/<int:pk>/', SongRetrieveApiView.as_view(), name='song-retrieve-api'),
    path('comment/<int:pk>/', CommentsApiView.as_view(), name='comment-api'),
    path('comment/view/<int:pk>/', CommentApiView.as_view(), name='comment-api'),
    path('rcomment/<int:pk>/', ReplyCommentApiView.as_view(), name='rcomment-api'),
    path('like/<int:pk>/', LikeAPiView.as_view(), name='like-api'),
]
