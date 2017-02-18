Google Drive Recursive Ownership Tool
==

Supported Files
--

    G Suite for Government and G Suite for Education accounts can change ownership of any file owned by the current user, including uploaded/synced files suchs as PDFs.
    Other Google Accounts such as G Suite for Business or Personal Google Accounts can only transfer ownership of Google files (Docs, Sheets, Sildes, Forms, Drawings, My Maps, and folders).
    NOTE: Ownership can only be transferred to members of the same G Suite or Google domain. Ex. @gmail.com can only transfer to other @gmail.com addresses.

Setup
--

    git clone https://github.com/davidstrauss/google-drive-recursive-ownership
    pip install --upgrade google-api-python-client

Usage
--

    If transfer.py is contained in a folder listed in your system's PATH this can be run from anywhere. Otherwise it needs to be run from the directory where transfer.py is located.

    python transfer.py PATH-PREFIX NEW-OWNER-EMAIL SHOW-ALREADY-OWNER

        - PATH-PREFIX assumes use of "/" or "\" as appropriate for your operating system.
        - SHOW-ALREADY-OWNER "true"|"false" (default true) to hide feedback for files already set correctly

    Windows Example:
        python transfer.py "Folder 1\Folder 2\Folder 3" new_owner@example.com true

    Mac/Linux Example:
        python transfer.py "Folder 1/Folder 2/Folder 3" new_owner@example.com false