from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


# AppUser model
User = get_user_model()


class CustomUserBackend(ModelBackend):
    """
    Custom app user authentication backend to provide for username/email and password authentication.
    A case insensitive search is used for usernanme/email field.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User._default_manager.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            return None
