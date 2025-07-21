
from django.contrib.auth.models import User
from .models import Profile

from django.contrib.auth.backends import ModelBackend

from social_django.models import UserSocialAuth

class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    Profile.objects.get_or_create(user=user)


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Versuche zuerst mit Username
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user:
            return user
        # Wenn das fehlschlägt, suche nach E‑Mail
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


def get_spotify_token(user):
    try:
        us = user.social_auth.get(provider='spotify')
    except UserSocialAuth.DoesNotExist:
        return None
    return us.get_access_token().get('access_token')
