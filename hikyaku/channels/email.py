from hikyaku.base import HikyakuNotification, HikyakuSettings, HikyakuNotifier
import boto3
import logging
import emails


class SmtpEmailSettings(HikyakuSettings):
    def __init__(self, **kwargs):
        super(SmtpEmailSettings, self).__init__()
        self.host = kwargs['host'] if 'host' in kwargs else ""
        self.username = kwargs['username'] if 'username' in kwargs else ""
        self.password = kwargs['password'] if 'password' in kwargs else ""
        self.port = kwargs['port'] if 'port' in kwargs else ""
        self.mode = kwargs['mode'] if 'mode' in kwargs else ""

    def get_config_name(self):
        return "smtp"


class AmazonEmailSettings(HikyakuSettings):

    def __init__(self, **kwargs):
        super(AmazonEmailSettings, self).__init__()
        self.region_name = kwargs['region_name'] if 'region_name' in kwargs else ""
        self.charset = kwargs['charset'] if 'region_name' in kwargs else 'utf-8'
        self.reply_to_addresses = kwargs['reply_to_addresses'] if 'reply_to_addresses' in kwargs else []

    def get_config_name(self):
        return "aws"


class EmailNotification(HikyakuNotification):
    def __init__(self, subject, body, html_body, recipients, from_address,
                 cc_recipients=None, bcc_recipients=None,**kwargs):

        super(EmailNotification, self).__init__(**kwargs)
        assert subject
        assert(html_body or body)
        assert(isinstance(recipients,(list,tuple,dict)))
        assert(isinstance(from_address,(str,unicode) or from_address is None))
        self.subject = subject
        self.html_body = html_body
        self.body = body
        self.recipients = recipients
        self.cc_recipients = cc_recipients
        self.bcc_recipients = bcc_recipients
        self.from_address = from_address


class AmazonEmailNotifier(HikyakuNotifier):

    def __init__(self, *args, **kwargs):
        self.last_result = None
        super(AmazonEmailNotifier, self).__init__(*args, **kwargs)

    def send(self):
        client = boto3.client('ses',region_name=self.settings.region_name)
        res = client.send_email(Source='kshehadeh@aws.ua-ecm.com',
                                Destination={
                                    'ToAddresses': self.notification.recipients,
                                    'CcAddresses': self.notification.cc_recipients,
                                    'BccAddresses': self.notification.bcc_recipients
                                },
                                Message={
                                    'Subject': {
                                        'Data': self.notification.subject,
                                        'Charset': self.settings.charset
                                    },
                                    'Body': {
                                        'Text': {
                                            'Data': self.notification.body
                                        },
                                        'Html': {
                                            'Data': self.notification.html_body
                                        }
                                    }
                                },
                                ReplyToAddresses=[self.notification.from_address]
                                )
        self.last_result = res
        if res and (res['ResponseMetadata']['HTTPStatusCode'] == 200):
            return True
        else:
            return False


class SmtpEmailNotifier(HikyakuNotifier):

    def __init__(self, *args, **kwargs):
        self.last_result = None
        super(SmtpEmailNotifier, self).__init__(*args, **kwargs)

    def send(self):
        message = emails.Message(html=self.notification.html_body,
                                 text=self.notification.body,
                                 mail_from=self.notification.from_address,
                                 mail_to=self.notification.recipients,
                                 cc=self.notification.cc_recipients,
                                 bcc=self.notification.bcc_recipients,
                                 subject=self.notification.subject)

        settings = {
            'host':self.settings.host,
            'port': self.settings.port,
            'ssl': self.settings.mode == 'ssl',
            'tls': self.settings.mode == 'tls',
            'user': str(self.settings.username),
            'password': str(self.settings.password)
        }
        self.last_result = message.send(smtp=settings)
        return self.last_result and self.last_result.status_code == 250
