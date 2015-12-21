from datetime import datetime, timedelta
import parsedatetime as pdt


class Reminder(object):
    ''' Represents a reminder that needs to be sent after a specific time '''

    def __init__(self, subject, text):
        ''' Construct a Reminder from the plaintext body of an email '''

        # Save a copy of the current time
        self._now = datetime.now()

        # Split the reminder body by line breaks to get timing information from
        # the first line
        lines = text.splitlines()

        # Parse the date and time to send the reminder
        cal = pdt.Calendar()
        self._send_time = cal.parseDT(lines[0], self._now)[0]

        # Save the content of the reminder
        self._subject = subject
        self._text = ''

        # Skip the line with send time and a blank line following
        for line in lines[2:]:
            self._text += line + '\r\n'

    def is_send_time(self):
        return self._now - self._send_time > timedelta(0)

    def send(self, mail_account, recipient):
        mail_account.send_message([recipient], self._subject, self._text)
