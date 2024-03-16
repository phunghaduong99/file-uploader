import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from werkzeug.utils import secure_filename


# Call the Drive v3 API
scope = ['https://www.googleapis.com/auth/drive']
service_account_json_key = 'secret.json'
credentials = service_account.Credentials.from_service_account_file(
                              filename=service_account_json_key,
                              scopes=scope)
drive_service = build('drive', 'v3', credentials=credentials)
PARENT_FOLDER_ID= "1RL5nVtP96hQ-wQPbKAH3B5JuYpNxZ_sV" ##folder hgtp

def upload_file(file, parentFolderId):
    fileName = secure_filename(file.filename) 
    file_metadata = {'name': fileName , 'parents': [parentFolderId]}
    media = MediaFileUpload( fileName )
    fileId = drive_service.files().create(body=file_metadata, media_body=media).execute()
    return fileId
    
def delete_files(file_or_folder_id):
    """Delete a file or folder in Google Drive by ID."""
    try:
        drive_service.files().delete(fileId=file_or_folder_id).execute()
        print(f"Successfully deleted file/folder with ID: {file_or_folder_id}")
    except Exception as e:
        print(f"Error deleting file/folder with ID: {file_or_folder_id}")
        print(f"Error details: {str(e)}")
    return "OK"

def download_file(file_id, destination_path):
    file = drive_service.files().get(fileId=file_id).execute()
    file_name = file.get("name")
    print(f'File name is: {file_name}')
    """Download a file from Google Drive by its ID."""
    requestt = drive_service.files().get_media(fileId=file_id)
    print(requestt)
    fh = io.FileIO(destination_path +"/"+ file_name, mode='wb')
    downloader = MediaIoBaseDownload(fh, requestt)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

def createRemoteFolder(folderName, parentID = None):
    # Create a folder on Drive, returns the newely created folders ID
    body = {
          'name': folderName,
          'mimeType': "application/vnd.google-apps.folder"
        }
    if parentID:
        body['parents'] = [parentID]
    root_folder = drive_service.files().create(body = body, fields='id').execute()
    return root_folder['id']

def deleteRemoteFolder(folderId):
    # Create a folder on Drive, returns the newely created folders ID
    drive_service.files().delete(fileId=folderId).execute()
    return 'OK'


def list_folder(mimeType):
    """List folders and files in Google Drive."""
    results = drive_service.files().list(
        q=f"'{PARENT_FOLDER_ID}' in parents and trashed=false" if PARENT_FOLDER_ID else None,
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print("No folders or files found in Google Drive.")
        return []
    else:
        print("Folders and files in Google Drive:")
        items = [x for x in items if x['mimeType'] == mimeType]
        for item in items:
            print(f"Name: {item['name']}, ID: {item['id']}, Type: {item['mimeType']}")
            # if delete:
                # delete_files(item['id'])
        return items