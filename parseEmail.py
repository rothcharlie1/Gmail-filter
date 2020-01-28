import readEmail
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText

def college_label():
  readEmail.ListLabels(service=build('gmail', 'v1', http=file.Storage('token.json').get().authorize(Http())), user_id='me')
  College = False

  for i in readEmail.labelsID: # Finds if there is already a label that has been named "College"
    if i == 'College':
      College = True
      break
  if College == False: # Creates a "College" label if it is not already a label
    print('Label Created')
    readEmail.CreateLabel(service=build('gmail', 'v1', http=file.Storage('token.json').get().authorize(Http())), user_id='me', label_object=readEmail.MakeLabel(label_name='College', mlv='show', llv='labelShow'))
  else:
    print('Label Exists')
  # edu_search()
  print(readEmail.FromList)

def edu_search(): # Searches for ".edu" in email address
  test = []
  for From in readEmail.FromList:
    add = From.find('.edu')
    if add != -1:
      print(From)