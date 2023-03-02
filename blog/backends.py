from django.contrib.auth.backends import BaseBackend
from blog.models import LibraryMember

class LibraryMemberAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = LibraryMember.objects.get(email=username)
            if user.check_password(password):
                return user
        except LibraryMember.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return LibraryMember.objects.get(pk=user_id)
        except LibraryMember.DoesNotExist:
            return None