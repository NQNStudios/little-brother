import datetime
from tzlocal import get_localzone
import dateutil.parser
import parsedatetime as pdt


class Reminder(object):
    ''' Represents a reminder that needs to be sent after a specific time '''

    def __init__(self, subject, text, date):
        ''' Construct a Reminder from the plaintext body of an email '''

        self._tzinfo = get_localzone()

        # Save a copy of the current time
        self._now = dateutil.parser.parse(date).astimezone(self._tzinfo)

        # Split the reminder body by line breaks to get timing information from
        # the first line
        lines = text.splitlines()

        # Parse the date and time to send the reminder
        cal = pdt.Calendar()
        self._send_time = self._tzinfo.localize(cal.parseDT(lines[0], self._now)[0])

        # Save the content of the reminder
        self._subject = subject
        self._text = ''

        # Skip line with send time and all blank lines preceding the message
        skipped_blanks = False

        for line in lines[1:]:
            if not skipped_blanks:
                if len(line) == 0:
                    continue
                else:
                    skipped_blanks = True

            self._text += line + '\r\n'

    def is_send_time(self):
        print('Checking if reminder ' + self._subject + ' should be sent')

        return self._tzinfo.localize(datetime.datetime.now()) > self._send_time

    def send(self, mail_account, recipient):
        print ('Sending reminder')
        mail_account.send_message([recipient], self._subject, self._text)
