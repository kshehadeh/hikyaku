import os
import unittest

import hikyaku
from unittest import TestCase

from hikyaku.channels.email import AmazonEmailSettings, EmailNotification, SmtpEmailSettings


class TestEmailNotifier(TestCase):

    def setUp(self):
        self.config_file = os.path.join(os.path.dirname(__file__),'config.json')

    def test_amazon(self):
        settings = AmazonEmailSettings()
        settings.import_json(self.config_file)

        notification = EmailNotification(
            subject=settings.subject,
            html_body=settings.html_body,
            body=settings.body,
            recipients=settings.recipients,
            cc_recipients=settings.cc_recipients,
            bcc_recipients=settings.bcc_recipients,
            from_address=settings.from_address
        )

        result = hikyaku.send_aws_email_notification(settings,notification)
        self.assertTrue(result)

    def test_smtp(self):
        settings = SmtpEmailSettings()
        settings.import_json(self.config_file)

        notification = EmailNotification(
            subject=settings.subject,
            html_body=settings.html_body,
            body=settings.body,
            recipients=settings.recipients,
            cc_recipients=settings.cc_recipients,
            bcc_recipients=settings.bcc_recipients,
            from_address=settings.from_address
        )

        result = hikyaku.send_smtp_email_notification(settings,notification)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()

