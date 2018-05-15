import imaplib
import sys
import email
import email.header
import datetime


email_account = 'username'
email_password = 'p@ssw0rd'
email_folder = 'INBOX/toHeliumV'
email_server = 'demo.siedl.net'


def process_mailbox(M):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = decode[0]
        print('Message %s: %s' % (num, subject))
        print('Raw Date:', msg['Date'])
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print("Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S"))


M = imaplib.IMAP4(email_server)

try:
    rv, data = M.login(email_account, email_password)
except imaplib.IMAP4.error as e:
    print('Login failed: {}'.format(e))
    sys.exit(1)

print(rv, data)

rv, mailboxes = M.list()
if rv == 'OK':
    print('Mailboxes:')
    print(mailboxes)

rv, data = M.select(email_folder)
if rv == 'OK':
    print('Processing mailbox {} ..'.format(email_folder))
    process_mailbox(M)
    M.close()
else:
    print('Unable to open mailbox: {}'.format(rv))

M.logout()
