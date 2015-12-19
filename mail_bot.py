import imaplib
from email.mime.text import MIMEText

class MailBot(object):
    """ Connects to an IMAP email server at the given location. Sends and
    receives emails from the specified address.
    """

    def __init__(self, server, port, address, password):
        # Connect to the IMAP server
        self._server = imaplib.IMAP4_SSL(server, port)
        # Log in to the email account
        self._server.login(address, password)

        # TODO test code..
        self._server.select('Inbox')
        typ, data = self._server.search(None, 'ALL')
        for num in data[0].split():
            typ, data = self._server.fetch(num, '(RFC822)')
            print('Message %s\n%s\n' % (num, data[0][1]))

        self._server.close()

    def __del__(self):
        # Log out of the email account
        self._server.logout()
