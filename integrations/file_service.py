# integrations/file_service.py
# This module contains all functions for interacting with the Google Drive API.

import os
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
# Import our reusable authentication service
from integrations.auth_service import get_google_api_service

def upload_file_to_drive(file_path, folder_id=None):
    """
    Uploads a file to the user's Google Drive.

    Args:
        file_path (str): The path to the local file to upload.
        folder_id (str, optional): The ID of the Drive folder to upload into. 
                                   If None, uploads to the root "My Drive". Defaults to None.

    Returns:
        str: The ID of the uploaded file, or None if it fails.
    """
    try:
        service = get_google_api_service('drive', 'v3')
        if not service:
            print("Failed to get Drive service. Aborting.")
            return None

        if not os.path.exists(file_path):
            print(f"Error: The file at {file_path} does not exist.")
            return None

        # Get the filename from the path
        file_name = os.path.basename(file_path)
        
        # Prepare the file metadata
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        # Prepare the media to upload
        media = MediaFileUpload(file_path, resumable=True)

        print(f"Uploading '{file_name}' to Google Drive...")
        # Call the Drive v3 API
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        file_id = file.get('id')
        print(f"File uploaded successfully! File ID: {file_id}")
        return file_id

    except HttpError as error:
        print(f"An error occurred with the Drive API: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# This block allows you to run this file directly for testing.
if __name__ == '__main__':
    print("--- Running Google Drive File Upload Test ---")
    
    # 1. Create a dummy file to upload for the test
    test_file_name = "test_upload.txt"
    try:
        with open(test_file_name, "w") as f:
            f.write("This is a test file for the Intelligent Agent upload function.")
        print(f"Created a dummy file: '{test_file_name}'")
    
        # 2. Call the upload function
        upload_file_to_drive(test_file_name)

    except Exception as e:
        print(f"An error occurred during the test setup: {e}")
    finally:
        # 3. Clean up the dummy file
        if os.path.exists(test_file_name):
            os.remove(test_file_name)
            print(f"Cleaned up the dummy file: '{test_file_name}'")
