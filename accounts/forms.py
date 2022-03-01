from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError

User = get_user_model()

class SignUp(UserCreationForm):

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('این ایمیل از قبل موجود است.')
        return email

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField}
