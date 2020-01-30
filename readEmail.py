# from email.mime.text import MIMEText
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import json

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'

FromList = {}
labelNames = []
idList = []
CollegeID = ''
SavedID = {}

# Acting as the main method of the code
def main():
  importer()
  college_label()
  edu_search()
  for i in idList:
    ModifyMessage(service=build('gmail', 'v1', http=file.Storage('token.json').get().authorize(Http())), user_id='me', msg_id=i, msg_labels=CreateMsgLabels() )
  print('Emails have been labeled.')


def importer(): # Imports all the emails from the gmail account
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets('client_secret_44702673440-vq3k3r554g4oh4lod094kl1okbmga5c7.apps.googleusercontent.com.json', SCOPES)  #i think this part establishes the connection between the program and the email and does authorization
      creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
     # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()  #fetches messages
    messages = results.get('messages', [])
  
    if not messages:
      print ("No messages found.")
    else:
      for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()  #loop through all messages, pull out message, add id to the list of ids, and run the content filter
        # idList.append(message['id'])
        doodoo=message['id']
        content_filter(msg, doodoo)
  
def find_index(lst: list, key, value): #this method finds a specific value for a specific key in a list and returns the index of it
    for i, dic in enumerate(lst):
      if dic[key] == value:
        return i
    return None

def content_filter(mesg, doodoo):    # Finds all email addresses and messages ID's and pairs them
  separated_list = mesg['payload']['headers'] #location of list of headers
    
  from_index = find_index(separated_list, 'name', 'From') 
  from_val = mesg['payload']['headers'][from_index]['value'] #gets where mail is from

  subject_index = find_index(separated_list, 'name', 'Subject') #gets subject
  try:
    subject_val = mesg['payload']['headers'][subject_index]['value']
  except:
    pass

  snippet_val = mesg['snippet'] #gets snippet

  FromList.update({from_val : doodoo}) # Appends email address and id , DOES NOT WORK
    
  # print(from_val) #outputs the 3 parameters of each email
  # print(subject_val)
  # print(snippet_val)
  # print()

def ModifyMessage(service, user_id, msg_id, msg_labels): # Adds labels to a message
  """Modify the Labels on the given Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The id of the message required.
    msg_labels: The change in labels.

  Returns:
    Modified message, containing updated labelIds, id and threadId.
  """
  try:
    message = service.users().messages().modify(userId=user_id, id=msg_id, body=msg_labels).execute()

    label_ids = message['labelIds']

    print('Message ID: %s - With Label IDs %s' % (msg_id, label_ids))
    return message
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


def CreateMsgLabels(): # Adds and removes labels, built for the the Modify Message method
  """Create object to update labels.

  Returns:
    A label update object.
  """
  return {'removeLabelIds': [], 'addLabelIds': [CollegeID]}

def CreateLabel(service, user_id, label_object): # Creates a label in the Gmail Account and saves label id to .txt file
  """Creates a new label within user's mailbox, also prints Label ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_object: label to be added.

  Returns:
    Created Label.
  """
  try:
    label = service.users().labels().create(userId=user_id, body=label_object).execute()
    global CollegeID
    global SavedID
    CollegeID = label['id']
    SavedID.update({'ID': label['id']})
    with open('label.txt', 'w') as outfile:
      json.dump(SavedID, outfile)

    return label
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def MakeLabel(label_name, mlv='show', llv='labelShow'): # Makes label and label ID for the Create Label method
  """Create Label object.

  Args:
    label_name: The name of the Label.
    mlv: Message list visibility, show/hide.
    llv: Label list visibility, labelShow/labelHide.

  Returns:
    Created Label.
  """
  label = {'messageListVisibility': mlv,
           'name': label_name,
           'labelListVisibility': llv}
  return label

def ListLabels(service, user_id): # Gets all the labels that are currently in the gmail account
  try:
    response = service.users().labels().list(userId=user_id).execute()
    labels = response['labels']
    for label in labels:
      labelNames.append(label['name'])
    return labels
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)

def edu_search(): # Searches for ".edu" in email address
  test = []
  for From in FromList:
    add = From.find('.edu')
    if add != -1:
      idList.append(FromList.get(From))

def college_label(): # Searches for the college label and decides whether or not to create the label in the gmail account
  global CollegeID
  ListLabels(service=build('gmail', 'v1', http=file.Storage('token.json').get().authorize(Http())), user_id='me')
  College = False

  for i in labelNames: # Finds if there is already a label that has been named "College"
    if i == 'Matt and Charlie\'s College Filter':
      College = True
      break
  if College == False: # Creates a "College" label if it is not already a label
    print('Label Created')
    CreateLabel(service=build('gmail', 'v1', http=file.Storage('token.json').get().authorize(Http())), 
    user_id='me', label_object=MakeLabel(label_name='Matt and Charlie\'s College Filter', mlv='show', llv='labelShow'))
  else:
    print('Label Exists')
    with open('label.txt') as json_file:
      SavedID = json.load(json_file)
      CollegeID=SavedID['ID']

  # edu_search()
  # print(FromList)


            
if __name__ == '__main__':
    main()

