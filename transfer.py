#!/usr/bin/python

import httplib2
import googleapiclient.discovery
import googleapiclient.http
import googleapiclient.errors
import oauth2client.client
import sys
import pprint
import os

def get_drive_service():
    OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRETS = 'client_secrets.json'
    flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRETS, OAUTH2_SCOPE)
    flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
    authorize_url = flow.step1_get_authorize_url()
    print('Use this link for authorization: {}'.format(authorize_url))
    if sys.version_info[0] > 2:
        code = input('Verification code: ').strip()
    else:
        code = raw_input('Verification code: ').strip()
    credentials = flow.step2_exchange(code)
    http = httplib2.Http()
    credentials.authorize(http)
    drive_service = googleapiclient.discovery.build('drive', 'v2', http=http)
    return drive_service

def get_permission_id_for_email(service, email):
    try:
        id_resp = service.permissions().getIdForEmail(email=email).execute()
        return id_resp['id']
    except googleapiclient.errors.HttpError as e:
        print('An error occured: {}'.format(e))

def show_info(service, drive_item, prefix, permission_id):
    try:
        print(os.path.join(prefix, drive_item['title']))
        print('Would set new owner to {}.'.format(permission_id))
    except KeyError:
        print('No title for this item:')
        pprint.pprint(drive_item)

def grant_ownership(service, drive_item, prefix, permission_id, show_already_owned):
    full_path = os.path.join(os.path.sep.join(prefix), drive_item['title']).encode('utf-8', 'replace')

    #pprint.pprint(drive_item)

    current_user_owns = False
    for owner in drive_item['owners']:
        if owner['permissionId'] == permission_id:
            if show_already_owned:
                print('Item {} already has the right owner.'.format(full_path))
            return
        elif owner['isAuthenticatedUser']:
            current_user_owns = True

    print('Item {} needs ownership granted.'.format(full_path))

    if not current_user_owns:
        print('    But, current user does not own the item.'.format(full_path))
        return

    try:
        permission = service.permissions().get(fileId=drive_item['id'], permissionId=permission_id).execute()
        permission['role'] = 'owner'
        print('    Upgrading existing permissions to ownership.')
        return service.permissions().update(fileId=drive_item['id'], permissionId=permission_id, body=permission, transferOwnership=True).execute()
    except googleapiclient.errors.HttpError as e:
        if e.resp.status != 404:
            print('An error occurred updating ownership permissions: {}'.format(e))
            return

    print('    Creating new ownership permissions.')
    permission = {'role': 'owner',
                  'type': 'user',
                  'id': permission_id}
    try:
        service.permissions().insert(fileId=drive_item['id'], body=permission, emailMessage='Automated recursive transfer of ownership.').execute()
    except googleapiclient.errors.HttpError as e:
        print('An error occurred inserting ownership permissions: {}'.format(e))

def process_all_files(service, callback=None, callback_args=None, minimum_prefix=None, current_prefix=None, folder_id='root'):
    if minimum_prefix is None:
        minimum_prefix = []
    if current_prefix is None:
        current_prefix = []
    if callback_args is None:
        callback_args = []

    print('Gathering file listings for prefix {}...'.format(current_prefix))

    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            children = service.children().list(folderId=folder_id, **param).execute()
            for child in children.get('items', []):
                item = service.files().get(fileId=child['id']).execute()
                #pprint.pprint(item)
                if item['kind'] == 'drive#file':
                    if current_prefix[:len(minimum_prefix)] == minimum_prefix:
                        print(u'File: {} ({}, {})'.format(item['title'], current_prefix, item['id']))
                        callback(service, item, current_prefix, **callback_args)
                    if item['mimeType'] == 'application/vnd.google-apps.folder':
                        print(u'Folder: {} ({}, {})'.format(item['title'], current_prefix, item['id']))
                        next_prefix = current_prefix + [item['title']]
                        comparison_length = min(len(next_prefix), len(minimum_prefix))
                        if minimum_prefix[:comparison_length] == next_prefix[:comparison_length]:
                            process_all_files(service, callback, callback_args, minimum_prefix, next_prefix, item['id'])
                            callback(service, item, current_prefix, **callback_args)
            page_token = children.get('nextPageToken')
            if not page_token:
                break
        except googleapiclient.errors.HttpError as e:
            print('An error occurred: {}'.format(e))
            break

if __name__ == '__main__':
    if sys.version_info[0] > 2:
        minimum_prefix = sys.argv[1]
        new_owner = sys.argv[2]
        show_already_owned = False if len(sys.argv) > 3 and sys.argv[3] == 'false' else True
    else:
        minimum_prefix = sys.argv[1].decode('utf-8')
        new_owner = sys.argv[2].decode('utf-8')
        show_already_owned = False if len(sys.argv) > 3 and sys.argv[3].decode('utf-8') == 'false' else True
    print('Changing all files at path "{}" to owner "{}"'.format(minimum_prefix, new_owner))
    minimum_prefix_split = minimum_prefix.split(os.path.sep)
    print('Prefix: {}'.format(minimum_prefix_split))
    service = get_drive_service()
    permission_id = get_permission_id_for_email(service, new_owner)
    print('User {} is permission ID {}.'.format(new_owner, permission_id))
    process_all_files(service, grant_ownership, {'permission_id': permission_id, 'show_already_owned': show_already_owned }, minimum_prefix_split)
    #print(files)
