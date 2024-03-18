import datetime as dt
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path

# setup Google dev console: https://youtu.be/j7JlI6IAdQ0?si=KojsK6d9KiRioJ0w

# Google folder ID
def load_config(): 
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


# load Google redentials
def get_credentials():
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds


# get specific Google doc ID
def get_doc_id(title, creds):
    config = load_config()

    # build the Drive and Docs API
    drive_service = build('drive', 'v3', credentials=creds)

    # Get Google folder ID
    folder_id = config.get('folder_id')
    if not folder_id:
        raise ValueError("folder_id is not set in the configuration")

    doc_title = title
    # create new doc in the specified folder
    doc_metadata = {
        'name': doc_title,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.document'
    }
    doc = drive_service.files().create(body=doc_metadata).execute()
    # get id of the new doc
    id = doc['id']
    return id



def doc_content(content, id, creds):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/document'])
    docs_service = build('docs', 'v1', credentials=creds)
    requests = [
        {
            'insertText': {'location': {'index':1}, 'text': content}
        }
    ]
    docs_service.documents().batchUpdate(documentId=id, body={'requests': requests}).execute()


def create_and_get_doc_url():
    title = 'test doc'  # get title from UI
    content = 'Hello world!'    # replace this with response
    creds = get_credentials()
    id = get_doc_id(title, creds)
    doc_url = f"https://docs.google.com/document/d/{id}"
    print('DOC URL', doc_url)
    doc_content(content, id, creds)

