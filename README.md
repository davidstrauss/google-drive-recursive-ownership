Google Drive Recursive Ownership Tool
==

Note
--

[Google Drive allows transfering ownership only of Google Docs, Sheets, Slides, or Forms](https://support.google.com/drive/answer/2494893).

Setup
--

    git clone https://github.com/davidstrauss/google-drive-recursive-ownership
    pip install --upgrade google-api-python-client

Usage
--

    python transfer.py PATH-PREFIX NEW-OWNER-EMAIL SHOW-ALREADY-OWNER

- PATH-PREFIX assumes use of "/" or "\" as appropriate for your operating system.
- SHOW-ALREADY-OWNER "true"|"false" (default true) to hide feedback for files already set correctly
