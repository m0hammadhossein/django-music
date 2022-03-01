from django.urls import path, include
from music.views import index

app_name = 'music'

urlpatterns = [
    path('',index, name='home'),
    path('api/', include('music.api.urls'))
]
