import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SubscribeActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, sub, timestamp):
        return (
                six.text_type(sub.pk) + six.text_type(timestamp) + six.text_type(sub.is_active)
        )

email_activation_token = SubscribeActivationTokenGenerator()
email_unsubscribe_token = SubscribeActivationTokenGenerator()
