from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import datetime

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveConnector:
    __file_name = None
    __file_path = None
    __folder_id = None

    def __init__(self, file_path, folder_id=None):
        self.__file_name = self.generate_file_name("database", "db")
        self.__file_path = file_path
        self.__folder_id = folder_id

    def authenticate_google_drive(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                credentials_file = 'credentials_google_cloud.json'
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('drive', 'v3', credentials=creds)

    def upload_file_to_drive(self, service, file_name, file_path, folder_id):
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)

        try:
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
                supportsAllDrives=True # Unidades compartidas = True; False o quitar esta linea si no es compartida la carpeta destino
            ).execute()
            print(f"File ID: {file.get('id')}")
        except Exception as error:
            print(f"An error occurred: {error}")

    def generate_file_name(self, base_name, extension):
        today = datetime.datetime.now()
        date_str = today.strftime('%Y_%m_%d_%H_%M')
        file_name = f"{base_name}_{date_str}.{extension}"
        return file_name

    def update_backup(self):
        try:
            service = self.authenticate_google_drive()
            self.upload_file_to_drive(service, self.__file_name, self.__file_path, self.__folder_id)
        except Exception as error:
            print(f"An error occurred when make BACKUP: {error}")

    def get_actual_local_path(self, file_name):
        actual_directory = os.path.dirname(os.path.abspath(__file__))
        complet_path = os.path.join(actual_directory, file_name)
        return complet_path