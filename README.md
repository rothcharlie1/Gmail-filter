# Gmail-filter
A multipurpose filter for Gmail labeling </br>
Built by C. Roth and M. Currie

Python was made to run in an object oriented fashion
The main method first imports all the emails and saves all the from addresses along with the unique message ID that it holds
It then creates a label in the gmail account that is named "Matt and Charlie's College Filter"
Everytime following that, the label ID will be pulled from a json that holds the label ID
The code then searches through all the email adresses to see if the address includes ".edu" at the end of the address
All the emails that are found to have the ".edu" at the end have their message ID's added to a list where the label is then applied to the message in the inbox.