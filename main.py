import os
from email import email
from mail_account import MailAccount
from reminder import Reminder

if __name__ == "__main__":
    # Connect to the bot mail account
    mail_account = MailAccount.from_environment_vars()

    # Retrieve the configured reminder keyword from environment variable
    # configuration
    subject_keyword = os.environ['LB_SUBJECT_KEYWORD']

    # Open the inbox
    mail_account.imap.select('Inbox')

    # Retrieve every unanswered email whose subject line includes the keyword.
    # These represent reminders that have yet to be sent
    search_criteria = '(UNANSWERED) (SUBJECT "' + subject_keyword + '")'
    typ, data = mail_account.imap.search(None, search_criteria)

    # Retrieve the content of every reminder that's waiting to be sent
    messages = {}

    for num in data[0].split():
        typ, data = mail_account.imap.fetch(num, '(BODY.PEEK[])')
        messages[num] = email.message_from_string(data[0][1])

    # Retrieve the desired recipient from environment variable configuration
    recipient = os.environ['LB_REMINDER_RECIPIENT']

    # Process every reminder
    for num, message in messages.iteritems():
        text = ''

        for part in message.get_payload():
            if part.get_content_type() == 'text/plain':
                text = part.get_payload()

        reminder = Reminder(message['Subject'], text, message['Date'])

        print('Checking if a reminder should be sent')

        if reminder.is_send_time():
            print ('Sending reminder')
            reminder.send(mail_account, recipient)

            # Mark that the reminder has been sent by flagging as ANSWERED
            mail_account.imap.store(num, '+FLAGS', '\\Answered')

    # Close the inbox
    mail_account.imap.close()
