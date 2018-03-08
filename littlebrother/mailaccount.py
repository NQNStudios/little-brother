import os
import imaplib
import smtplib
import markdown
from email.mime.text import MIMEText
from email.header import Header


class MailAccount(object):
    """ Connects with SSL to an IMAP and an SMTP email
    server at the given locations.  Sends and receives email from the specified
    address.
    """

    def __init__(self, imap_server, imap_port, smtp_server, smtp_port,
                 address, password):
        # Connect to the IMAP server
        self._imap_server = imaplib.IMAP4_SSL(imap_server, imap_port)
        # Connect to the SMTP server
        self._smtp_server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        # Log in to the email account
        self._imap_server.login(address, password)
        self._smtp_server.login(address, password)

        # Save the email address we're logged into
        self._email_address = address

    def __del__(self):
        # Log out of the email account on the IMAP server
        self._imap_server.logout()
        # Disconnect from the SMTP server
        self._smtp_server.close()

    @classmethod
    def from_environment_vars(cls):
        """ Construct an instance of MailAccount using a configuration
        defined in environment variables
        """

        imap_server = os.environ['LB_IMAP_SERVER']
        imap_port = os.environ['LB_IMAP_PORT']
        smtp_server = os.environ['LB_SMTP_SERVER']
        smtp_port = os.environ['LB_SMTP_PORT']
        address = os.environ['LB_ADDRESS']
        password = os.environ['LB_PASSWORD']

        return cls(imap_server, imap_port, smtp_server, smtp_port,
                   address, password)

    @property
    def imap(self):
        """ The bot's connected IMAP server """
        return self._imap_server

    def send_message_plain(self, recipients, subject, body_text):
        """ Send a markdown-formatted email to the specified list of addresses
        """

        # Construct the message as a MIMEText
        message = MIMEText(body_text.encode('utf-8'), 'plain', 'utf-8')
        message['From'] = self._email_address
        message['To'] = recipients[0]
        message['Subject'] = Header(subject.encode('utf-8'), 'utf-8')

        self._smtp_server.sendmail(self._email_address, recipients,
                                   message.as_string())

    def send_message_markdown(self, recipients, subject, body_markdown):
        """ Send a markdown-formatted email to the specified list of addresses
        """

        # Convert the markdown to HTML
        body_html = markdown.markdown(body_markdown)

        # Construct the message as a MIMEText
        message = MIMEText(body_html.encode('utf-8'), "html", 'utf-8')
        message['From'] = self._email_address
        message['To'] = recipients[0]
        message['Subject'] = Header(subject.encode('utf-8'), 'utf-8')

        self._smtp_server.sendmail(self._email_address, recipients,
                                   message.as_string())
