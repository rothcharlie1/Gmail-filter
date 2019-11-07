from email.mime.text import MIMEText
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'

def main():
   importer()

def importer():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret_44702673440-vq3k3r554g4oh4lod094kl1okbmga5c7.apps.googleusercontent.com.json', SCOPES)  #i think this part establishes the connection between the program and the email and does authorization
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
     # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()  #fetches messages
    messages = results.get('messages', [])

    idList = []  
    if not messages:
        print ("No messages found.")
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()  #loop through all messages, pull out message, add id to the list of ids, and run the content filter
            idList.append(message['id'])
            content_filter(msg)
  
def find_index(lst, key, value): #this method finds a specific value for a specific key in a list and returns the index of it
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return None

def content_filter(mesg):    
    separated_list = mesg['payload']['headers'] #location of list of headers
    
    from_index = find_index(separated_list, 'name', 'From') 
    from_val = mesg['payload']['headers'][from_index]['value'] #gets where mail is from

    subject_index = find_index(separated_list, 'name', 'Subject') #gets subject
    subject_val = mesg['payload']['headers'][subject_index]['value']

    snippet_val = mesg['snippet'] #gets snippet
    
    print(from_val) #outputs the 3 parameters of each email
    print(subject_val)
    print(snippet_val)
    print()


    
    
   
# def create_message(sender, to, subject, message_text):
#   """Create a message for an email.

#   Args:
#     sender: Email address of the sender.
#     to: Email address of the receiver.
#     subject: The subject of the email message.
#     message_text: The text of the email message.

#   Returns:
#     An object containing a base64url encoded email object.
#   """
#   message = MIMEText(message_text)
#   message['to'] = to
#   message['from'] = sender
#   message['subject'] = subject
#   return {'raw': base64.urlsafe_b64encode(message.as_string())}

# def send_message(service, user_id, message):
#   """Send an email message.

#   Args:
#     service: Authorized Gmail API service instance.
#     user_id: User's email address. The special value "me"
#     can be used to indicate the authenticated user.
#     message: Message to be sent.

#   Returns:
#     Sent Message.
#   """
#   try:
#     message = (service.users().messages().send(userId=user_id, body=message)
#                .execute())
#     print ('Message Id: %s' % message['id'])
#     return message
#   except errors.HttpError as error:
#     print (f'An error occurred: {error}')
#     return None
   
            
if __name__ == '__main__':
    main()

