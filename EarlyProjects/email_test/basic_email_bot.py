#import relevant packages
import imapclient
import pyzmail
HOST = 'imap.gmail.com'
USERNAME = 'jackfrostscript@gmail.com'
PASSWORD = 'bar3nak3dlad13s'


#imap server configure request
script_email = imapclient.IMAPClient('imap.gmail.com') 
#login to test email
script_email.login(USERNAME,PASSWORD)
#List Available Folders
folder_lists = script_email.list_folders()
#print(folder_lists)
#Access the inbox folder
script_email.select_folder('INBOX', readonly=True)
emails = script_email.search(['ALL'])
#print("Email UIDs:")
#print(emails)
#Fetch email body information
raw_msgs = script_email.fetch(emails, ['BODY[]'])
#Parse Emails
msgs = []
for uids in emails:
    msgs.append(pyzmail.PyzMessage.factory(raw_msgs[uids][b'BODY[]']))
#Print All Senders of Current Emails
senders = []
for parsed_msgs in msgs:
    senders.append(parsed_msgs.get_addresses('from'))
print('Number of Emails:')
print(len(emails))
print("Sender Emails:")
for f in senders:
    print(f[0][1])

