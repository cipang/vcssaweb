import traceback

import boto3
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class SESBackend(BaseEmailBackend):
    """
    An email backend to send emails via Amazon Simple Email Service (SES).
    """

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.access_key_id = getattr(settings, "AWS_ACCESS_KEY_ID", None)
        self.secret_access_key = getattr(settings, "AWS_SECRET_ACCESS_KEY", None)
        self.region = getattr(settings, "AWS_SES_REGION_NAME", "us-east-1")
        self.fail_silently = fail_silently
        self.client = None

    def open(self):
        self.client = boto3.client("ses", region_name=self.region,
                                   aws_access_key_id=self.access_key_id,
                                   aws_secret_access_key=self.secret_access_key)

    def close(self):
        self.client = None

    @property
    def is_open(self) -> bool:
        return bool(self.client)

    def send_messages(self, email_messages):
        n = 0
        try:
            if not self.is_open:
                self.open()

            for message in email_messages:
                self.client.send_raw_email(RawMessage={"Data": message.message().as_string()},
                                           Source=message.from_email,
                                           Destinations=message.recipients())
                n += 1
        except:
            if not self.fail_silently:
                raise
            else:
                # Fail silently but we print out a message to the stdout.
                traceback.print_exc()
        return n
