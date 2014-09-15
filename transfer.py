#!/usr/bin/python

import httplib2
import apiclient.discovery
import apiclient.http
import oauth2client.client
import os

def get_drive_service():
    OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRETS = 'client_secrets.json'
    flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRETS, OAUTH2_SCOPE)
    flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
    authorize_url = flow.step1_get_authorize_url()
    print('Use this link for authorization: {}'.format(authorize_url))
    code = raw_input('Verification code: ').strip()
    credentials = flow.step2_exchange(code)
    http = httplib2.Http()
    credentials.authorize(http)
    drive_service = apiclient.discovery.build('drive', 'v2', http=http)
    return drive_service

def retrieve_all_files(service):
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()
            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError as e:
            print('An error occurred: {}'.format(e))
            break
    return result

def update_permission(service, file_id, permission_id, new_role):
    """Update a permission's role.
    
    Args:
    service: Drive API service instance.
    file_id: ID of the file to update permission for.
    permission_id: ID of the permission to update.
    new_role: The value 'owner', 'writer' or 'reader'.
    
    Returns:
    The updated permission if successful, None otherwise.
    """
    try:
        # First retrieve the permission from the API.
        permission = service.permissions().get(fileId=file_id, permissionId=permission_id).execute()
        permission['role'] = new_role
        return service.permissions().update(fileId=file_id, permissionId=permission_id, body=permission).execute()
    except errors.HttpError as e:
        print('An error occurred: {}'.format(e))
    return None

if __name__ == '__main__':
    service = get_drive_service()
    files = retrieve_all_files(drive_service)
