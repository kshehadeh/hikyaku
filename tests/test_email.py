import os
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
            subject="Test Subject",
            html_body="<h1>Test HTML Body</h1>",
            body="Test Text Body",
            recipients=["karim@karim.cloud"],
            cc_recipients=["kshehadeh@underarmour.com"],
            bcc_recipients=["karim.shehadeh@gmail.com"],
            from_address="kshehadeh@ua-ecm.com"
        )

        result = hikyaku.send_aws_email_notification(settings,notification)
        self.assertTrue(result)

    def test_smtp(self):
        settings = SmtpEmailSettings()
        settings.import_json(self.config_file)

        notification = EmailNotification(
            subject="Test Subject",
            html_body="<h1>Test HTML Body</h1>",
            body="Test Text Body",
            recipients=["karim@karim.cloud"],
            cc_recipients=["kshehadeh@underarmour.com"],
            bcc_recipients=["karim.shehadeh@gmail.com"],
            from_address="kshehadeh@ua-ecm.com"
        )

        result = hikyaku.send_smtp_email_notification(settings,notification)
        self.assertTrue(result)


