from __future__ import print_function

import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pdf2image import convert_from_path
import eml2png

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/documents']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API - in this case, getting emails in inbox
        service = build('gmail', 'v1', credentials=creds)
        resultsMessages = service.users().messages().list(userId='me', labelIds=['INBOX'], q="category:primary", maxResults=10).execute()
        messages = resultsMessages.get('messages', [])

        if not messages:
            print('No emails found.')
            return
        
        i = 0
        for message in messages:
            # write each subject into doc
            id = message["id"]
            msg = service.users().messages().get(userId='me', id=id, format='raw', metadataHeaders=None).execute()
            raw = base64.urlsafe_b64decode(msg['raw'])
            with open('emails/email' + str(i) + '.eml', 'wb') as eml_file:
                eml_file.write(raw)
            with open('emails/message'+ str(i)+'.png', 'wb') as f:
                f.write(eml2png.to_png('emails/email' + str(i) + '.eml'))
            i += 1


    except HttpError as error:
        # API failed
        print(f'Http error wtv that means: {error}')









# parse email to be inserted onto Google Doc
def parse_msg(service, msg_id, msg):
    # handle PDFs
    if 'parts' in msg['payload']:
        parts = msg.get('payload',[])['parts']
        for i in parts:
            if( i['filename'] ):
                att = service.users().messages().attachments().get(userId='me', messageId=msg_id,id=i['body']['attachmentId']).execute()
                data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = i['filename']
                with open(path, 'wb') as f:
                    f.write(file_data)
                pages = convert_from_path('f', 500)
                for page in pages:
                    page.save('out.jpg', 'JPEG')

    # handle non-attactments
    # if msg.get("payload").get("body").get("data"):
    #     return base64.urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
    # return msg.get("snippet") 


if __name__ == '__main__':
    main()

