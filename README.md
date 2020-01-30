# Gmail-filter

A filter for labeling College emails.

Built by Charles Roth and Matt Currie

# Development

Built with the Gmail API with Python 3 in Visual Studio Code.

Google is very bad at updating their documentation, and it annoyed me so bad I decided to make this documentation nice. 

## Some Important Code Bits

Full, unabridged code is in the readEmail.py file.

Here we authenticate the user's Google account and retrieve a set of messages from the user's account. 

    store = file.Storage('token.json')

    creds = store.get()

    if not creds or creds.invalid:

    flow = client.flow_from_clientsecrets('client_secret_44702673440-vq3k3r554g4oh4lod094kl1okbmga5c7.apps.googleusercontent.com.json', SCOPES) #i think this part establishes the connection between the program and the email and does authorization

    creds = tools.run_flow(flow, store)

    service = build('gmail', 'v1', http=creds.authorize(Http()))

    \# Call the Gmail API to fetch INBOX

    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute() #fetches messages

    messages = results.get('messages', [])

Here we find find a dictionary in a list of dictionaries by a specific key-value pair. This took way longer than it should have. 
    
    def find_index(lst: list, key, value): #this method finds a specific value for a specific key in a list and returns the index of it
    for i, dic in enumerate(lst):
      if dic[key] == value:
        return i
    return None

Here we do some simple text lookup to find any emails with .edu domains. 

    def edu_search(): # Searches for ".edu" in email address
    test = []
    for From in FromList:
      add = From.find('.edu')
    if add != -1:
      idList.append(FromList.get(From))

And finally here is the most important method: here we list the labels and check to see if our custom label already exists. If it does, we load its ID from a json file and use that ID to move messages to that label. If it doesn't, we make one. 

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
        CreateLabel(service=build('gmail', 'v1', http=file.Storage('token.json').get().authorize(Http())), user_id='me', label_object=MakeLabel(label_name='Matt and Charlie\'s College Filter', mlv='show', llv='labelShow'))
      else:
        print('Label Exists')
        with open('label.txt') as json_file:
          SavedID = json.load(json_file)
          CollegeID=SavedID['ID']

## How to use Gmail Filter

First, clone or download the repository. 

Run the shortcut GMail College Filter - MCCR. Preferably, put this shortcut on your desktop to run this filter every once in a while. It does not automatically run on new emails. 

A command line interface will appear, and you will be required to sign in to your Google account. Our application does not send any information to any outside source, even us. Your emails are safe. 

After authentication, a label will be created for you, and your emails will slowly be filtered into that label. 

This will take a while. 

Run the shortcut whenever you want to filter any new emails. 
