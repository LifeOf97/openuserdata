from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomAppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username.lower()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email.lower()


class CustomAppUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
