import os
import unittest
from unittest import TestCase

import hikyaku
from hikyaku.channels.slack import SlackSettings, SlackNotification


class TestSlackNotifier(TestCase):

    def setUp(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'config.json')

    def test_slack_channel(self):
        settings = SlackSettings()
        settings.import_json(self.config_file)

        notification = SlackNotification(
            channel="ecomm-test",
            text="This is a *test*",
        )

        result = hikyaku.send_slack_notification(settings,notification)
        self.assertTrue(result)

    def test_slack_user(self):
        settings = SlackSettings()
        settings.import_json(self.config_file)

        notification = SlackNotification(
            users=["U06CEDDUZ"],
            text="This is a *test*",
        )

        result = hikyaku.send_slack_notification(settings,notification)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
