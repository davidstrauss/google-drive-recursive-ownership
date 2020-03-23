# Google Drive Recursive Ownership Tool

### Supported Files

G Suite for Government and G Suite for Education accounts can change ownership of any file owned by the current user, including uploaded/synced files suchs as PDFs.

Other Google Accounts such as G Suite for Business or Personal Google Accounts can only transfer ownership of Google files (Docs, Sheets, Sildes, Forms, Drawings, My Maps, and folders).

NOTE: Ownership can only be transferred to members of the same G Suite or Google domain. Ex. @gmail.com can only transfer to other @gmail.com addresses.

NOTE: The Google Drive API does not allow suppressing notifications for change of ownership if the _if_ the new owner does not already have access to the file. However, if the new owner _already_ has access to the file, upgrading their permissions to ownership will _not_ generate a notification.

### Setup

    git clone https://github.com/davidstrauss/google-drive-recursive-ownership
    pip install --upgrade google-api-python-client oauth2client six

### Usage

First, replace the [sample](https://github.com/gsuitedevs/python-samples/blob/d4fa75401e9b637f67da6fe021801d8b4cbd8cd0/drive/driveapp/client_secrets.json) `client_secrets.json` with your own [client secrets](https://github.com/googleapis/google-api-python-client/blob/master/docs/client-secrets.md). Otherwise, authorizations you create will be usable by anyone with access to the sample key (the entire internet).

Next, if `transfer.py` is contained in a folder listed in your system's `PATH` this can be run from anywhere. Otherwise it needs to be run from the directory where `transfer.py` is located.

    python  transfer.py  PATH-PREFIX  NEW-OWNER-EMAIL  SHOW-ALREADY-OWNER
    
 - `PATH-PREFIX` assumes use of "/" or "\" as appropriate for your operating system.

   * The `PATH-PREFIX` folder must be in **My Drive** section. For shared folders right click and select _Add to My Drive_.

 - `SHOW-ALREADY-OWNER` "`true`"|"`false`" (default `true`) to hide feedback for files already set correctly.
    
Windows Example:

    python transfer.py "Folder 1\Folder 2\Folder 3" new_owner@example.com true

Mac/Linux Example:

    python transfer.py "Folder 1/Folder 2/Folder 3" new_owner@example.com false
