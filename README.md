Google Drive Recursive Ownership Tool
==

Setup
--

    git clone https://github.com/davidstrauss/google-drive-recursive-ownership
    pip install --upgrade google-api-python-client

Usage
--

    python transfer.py PATH-PREFIX NEW-OWNER-EMAIL SHOW-ALREADY-OWNER
    NOTE: PATH-PREFIX assumed use of "\". SHOW-ALREADY-OWNER "true"|"false" (default true) to hide feedback for files already set correctly