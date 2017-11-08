from hikyaku.base import HikyakuNotifier, HikyakuSettings, HikyakuNotification
from slackclient import SlackClient
import logging


class SlackSettings(HikyakuSettings):

    def __init__(self, slack_api_token=None, **kwargs):
        super(SlackSettings, self).__init__(**kwargs)
        self.api_token = slack_api_token

    def get_config_name(self):
        return "slack"


class SlackNotification(HikyakuNotification):
    """
    Slack notifications use  the python slack API.


    Direct messages use the conversation api:
    http://slackapi.github.io/python-slackclient/conversations.html#creating-a-direct-message-or-multi-person-direct-message

    Channel messages use the chat API:


    """
    def __init__(self, text, channel=None, users=None, **kwargs):
        assert(text)
        assert(isinstance(channel,(str,unicode)) or not channel)
        assert(isinstance(users,(list,tuple)) or not users)

        self.channel = channel
        self.users = users
        self.text = text

        super(SlackNotification, self).__init__(**kwargs)


class SlackNotifier(HikyakuNotifier):

    def __init__(self,*args,**kwargs):
        self.last_result = None
        super(SlackNotifier, self).__init__(*args,**kwargs)

    def send(self):
        slack_token = self.settings.api_token
        sc = SlackClient(slack_token)

        if self.notification.channel:
            # if a specific channel was given we can just post a message to the existing channel.
            self.last_result = sc.api_call(
                "chat.postMessage",
                channel=self.notification.channel,
                text=self.notification.text
            )
            if self.last_result and self.last_result['ok']:
                return True
            else:
                return False
        elif self.notification.users:

            if isinstance(self.notification.users,(list,tuple)):
                users = ",".join(self.notification.users)
            else:
                users = self.notification.users

            # first we need to either create or get the conversation with the person or persons given
            result = sc.api_call(
                "conversations.open",
                users=users
            )

            if result and result['ok']:
                # now send the message to the "channel" which is either a direct message or multi-direct message
                channel = result['channel']['id']
                self.last_result = sc.api_call(
                    "chat.postMessage",
                    channel=channel,
                    text=self.notification.text
                )
                if self.last_result:
                    return 'ok' in self.last_result and self.last_result['ok']
                else:
                    return False

        else:
            raise ValueError("Request for notification did not contain channel or user recipients")
