from djoser.serializers import UidAndTokenSerializer
from rest_framework.exceptions import PermissionDenied


class DisableNotificationsSerializer(UidAndTokenSerializer):
    default_error_messages = {"stale_token": "Stale token for given user."}

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.user.notifications:
            return attrs
        raise PermissionDenied(self.error_messages["stale_token"])
