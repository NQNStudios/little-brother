import datetime
from tzlocal import get_localzone
import dateutil.parser
import parsedatetime as pdt
import os


class Reminder(object):
    ''' Represents a reminder that needs to be sent after a specific time '''

    def __init__(self, subject, text, set_time, send_time):
        # Operate in the current server time zone
        self._tzinfo = get_localzone()

        self._subject = subject
        self._text = text
        self._set_time = set_time
        self._send_time = send_time

    @classmethod
    def parse(cls, subject, text, date):
        tzinfo = get_localzone()

        ''' Construct a Reminder from the plaintext body of an email '''
        # Parse the time the reminder was set
        set_time = dateutil.parser.parse(date).astimezone(tzinfo)

        # Split the reminder body by line breaks to get timing information from
        # the first line
        lines = text.splitlines()

        # Parse the date and time to send the reminder
        cal = pdt.Calendar()
        send_time = tzinfo.localize(cal.parseDT(lines[0], set_time)[0])

        # Extract the content of the reminder
        text = ''

        # Skip line with send time and all blank lines preceding the message
        skipped_blanks = False

        for line in lines[1:]:
            print('Checking line ' + line)
            if not skipped_blanks:
                if len(line) == 0:
                    continue
                else:
                    skipped_blanks = True

            text += line + '\r\n'

        print(subject + ' has text: ' + text)
        print(text)
        return cls(subject, text, set_time, send_time)

    @classmethod
    def create(cls, subject, text, send_time):
        ''' Construct a reminder from scratch with the intention of setting it
        for later
        '''

        subject = os.environ['LB_SUBJECT_KEYWORD'] + ' ' + subject
        return cls(subject, text, datetime.datetime.now(), send_time)

    def is_send_time(self):
        ''' Check if it's time to send this reminder '''
        print('Checking if reminder should be sent: ' + self._subject)
        return self._tzinfo.localize(datetime.datetime.now()) > self._send_time

    def send(self, mail_account, recipient):
        ''' Send this reminder to the configured recipient of Little Brother
        mail notifications
        '''
        print('Sending reminder: ' + self._subject)
        mail_account.send_message_markdown([recipient], self._subject,
                                           self._text)

    def set(self, mail_account):
        ''' Set this reminder to be sent by the Little Brother bot account
        at a later time
        '''
        text = str(self._send_time) + '\r\n\r\n' + self._text
        mail_account.send_message_plain([mail_account._email_address],
                                        self._subject, text)
