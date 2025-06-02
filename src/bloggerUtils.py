import os   
import sys
from tabulate import tabulate
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import pickle
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/blogger']

class BloggerUtils:
    def __init__(self):
        self.service = self.get_blogger_service()

    def get_blogger_service(self):
        credentials_path = r'C:\Users\johnj\secure_configs\AgenticResearch\jryle_credentials.json'
        if not os.path.exists(credentials_path):
            print(f"Error: 'credentials.json' file not found at {credentials_path}.")
            sys.exit(1)
        if not os.path.exists('credentials.dat'):
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            credentials = flow.run_local_server(port=8081)
            with open('credentials.dat', 'wb') as credentials_dat:
                pickle.dump(credentials, credentials_dat)
        else:
            with open('credentials.dat', 'rb') as credentials_dat:
                credentials = pickle.load(credentials_dat)
        if credentials.expired:
            credentials.refresh(Request())
        return build('blogger', 'v3', credentials=credentials)

    def get_blogger_blogs(self):
        results = self.service.blogs().listByUser(userId='self').execute()
        items = results.get('items', [])
        if not items:
            print('No blogs found.')
        else:
            print('Blogs:')
            for item in items:
                print(f"{item['title']} ({item['url']})")

    def get_blogger_posts(self, blogId):
        results = self.service.posts().list(blogId=blogId).execute()
        items = results.get('items', [])
        if not items:
            print('No posts found.')
        else:
            print('Posts:')
            for item in items:
                print(f"{item['title']} ({item['url']})")

    def create_blogger_post(self, blogId, title, content):
        service = self.get_blogger_service()
        today_date = datetime.now().strftime("%Y-%m-%d")
        post_body = {
            'title': f"{title}",
            'content': content
        }
        try:
            response = service.posts().insert(blogId=blogId, body=post_body).execute()
            print(f"Post created: {response['url']}")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

