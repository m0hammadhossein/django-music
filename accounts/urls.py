from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetDoneView,PasswordResetCompleteView
from django.urls import path
from accounts.views import LoginView, LogoutView, PasswordReset, PasswordChange, PasswordResetConfirm, SignUp, \
    RegisterDone, Activate, Profile

app_name = 'accounts'

urlpatterns = [
    path('register/', SignUp.as_view(), name='register'),
    path('profile/', Profile.as_view(), name='profile'),
    path('register/done/', RegisterDone.as_view(), name='register_done'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('emailVerification/<uidb64>/<token>', Activate.as_view(), name='activate'),
]
