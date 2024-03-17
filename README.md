# HGTP Google Drive Uploader 
HGTP's uploader for uploading/downloading files to GG drive

## Basic Setup 

- Put the secret.json as the key for accessing to the GG drive.

- Run requirement.txt for installing the required library
```bash
$ pip3 install -r requirements.txt 
```
- Run application by **app.py**.

## Basic provided API 
### I. FOLDER API
### I.1 '/cloud/folder', method='POST'
- Use for create a new folder inside a parent folder.
- Parent folder ID is indentified for a unique folder, can extract inside a google drive link.
https://drive.google.com/drive/u/0/folders/1RL5nVtP96hQ-wQPbKAH3B5JuYpNxZ_sV
- Required params in body (raw json):
```bash
{
    "folderName": "image",
    "parentFolderId": "1RL5nVtP96hQ-wQPbKAH3B5JuYpNxZ_sV"
}
```
### I.2 '/cloud/folder', method='DELETE'
- Use for delete any existed folder.
- Required params in body (raw json):
```bash
{
    "folderId": "19iFfCqV70VEWJI2UvjmrfX5BzZBjDrC7" ## change the correspoding ID
}
```


### I.3 '/cloud/folder', method='GET'
- Use for list all files/folders inside in any folder. 
- Required params in url params  
```bash
http://localhost:8080/cloud/folder?mimeType=image/png&parentFolderId=1fFa8uKDWoFVaXcy0Guk8zpRXxeD1FZLd
```
- mimeType is type of the file. Use **mimeType** for get filtering and getting exact list of images.
- parentFolderId is the target folder.
### II. FILE API
### II.1 '/cloud/file/uploader', method='POST'
- Use for upload a new file to a remote folder.
- Required params in body (form-data):
```bash
{
    "file": "FILE_FROM_CLIENT",
    "parentFolderId": "1RL5nVtP96hQ-wQPbKAH3B5JuYpNxZ_sV"
}
```

### II.2 '/cloud/file', method='DELETE'
- Use for delete any existed remote file.
- Required params in body (raw json):
```bash
{
    "fileID": "1yJgVaHySJDM0-NvV_VwZRWvVdzMnKQHa"
}
```


### II.3 '/cloud/file/download', method='POST'
- Use for download any existed remote file and save in local destination.
- Required params in body (raw json):
```bash
{
    "fileId": "142BliVvDSIkQSOFm-Jg6uBU6Wf1AqHJe",
    "dest": "./storage"
}
```
