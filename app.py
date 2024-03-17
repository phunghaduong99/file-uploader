
from flask import Flask
from utils import list_folder, download_file, createRemoteFolder, upload_file,  deleteRemoteFolder, delete_files
from flask import Flask, jsonify, redirect, request, Response
from http import HTTPStatus
import os
from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)
@app.route("/")
def main():
    return "Welcome!"

############# FOLDER #################
@app.route('/cloud/folder', methods=['POST'])
def create_remote_folder_api():
    data = request.get_json()
    folderName = data.get('folderName', '')
    if folderName == '':
        return   Response(
       "Please insert folder name.",
        status= HTTPStatus.BAD_REQUEST,
    ) 
    parentFolderId = data.get('parentFolderId', '')
    if parentFolderId == '':
        return   Response(
       "Please insert parentFolder Id.",
        status= HTTPStatus.BAD_REQUEST,
    ) 
    else:
        root_folder_id = createRemoteFolder(folderName, parentFolderId )
        return jsonify({
            'root_folder_id': root_folder_id
        }), HTTPStatus.OK

@app.route('/cloud/folder', methods=['DELETE'])
def delete_remote_folder_api():
    data = request.get_json()
    folderId = data.get('folderId', '')
    if folderId == '':
        return   Response(
       "Please insert folder Id.",
        status= HTTPStatus.BAD_REQUEST,
    ) 
    else:
        status = deleteRemoteFolder(folderId )
        return jsonify({
            'status': status
        }), HTTPStatus.OK

@app.route('/cloud/folder', methods=['GET'])
def list_in_folder_api():
    mimeType = request.args.get('mimeType', '')
    parentFolderId = request.args.get('parentFolderId', '')
    return list_folder(mimeType, parentFolderId)


############# FILE #################
@app.route('/cloud/file', methods=['DELETE'])
def delete_remote_file_api():
    data = request.get_json()
    fileID = data.get('fileID', '')
    if fileID == '':
        return   Response(
       "Please insert file Id.",
        status= HTTPStatus.BAD_REQUEST,
    ) 
    else:
        status = delete_files(fileID )
        return jsonify({
            'status': status
        }), HTTPStatus.OK


@app.route('/cloud/file/uploader', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        f = request.files['file']
        parentFolderId = request.form.get('parentFolderId')
        if f:
            f.save(secure_filename(f.filename))
            file_id = upload_file(f, parentFolderId)
            if os.path.isfile(secure_filename(f.filename)):
                os.remove(secure_filename(f.filename))
            return jsonify({
                'file_id': file_id
            }), HTTPStatus.OK
    else:
        return   Response(
        "Error",
        status= HTTPStatus.BAD_REQUEST)


@app.route('/cloud/file/download', methods=['POST'])
def download_file_api():
    data = request.get_json()
    fileId = data.get('fileId', '')
    if fileId == '':
        return   Response(
       "Please insert file ID.",
        status= HTTPStatus.BAD_REQUEST,
    ) 
    destinationPath = data.get('dest', '')
    if destinationPath == '':
        return   Response(
       "Please insert destination path.",
        status= HTTPStatus.BAD_REQUEST,
    ) 
    else:
         download_file(fileId,  destinationPath)
         return Response(
       "OK",
        status= HTTPStatus.ACCEPTED)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)