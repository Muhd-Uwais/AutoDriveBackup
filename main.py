import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler  # For monitoring directory changes
from googleapiclient.discovery import build        # For interacting with Google Drive API
from googleapiclient.http import MediaFileUpload    # For uploading files to Google Drive
from google_auth_oauthlib.flow import InstalledAppFlow  # For handling OAuth 2.0 authorization flow

# Path to your Google API client secret file, Replace with yours.
CLIENT_SECRET = "D:\\Automate_ File_Backup\\client_secret.json"  

# Google Drive API scope for file operations, Don't change this
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Custom event handler class to respond to file system events
class Listener(FileSystemEventHandler):
    
    def __init__(self):
        # Initialize OAuth 2.0 flow using client secrets JSON file and requested scopes
        self.flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET, SCOPES)
        # Run the OAuth flow locally and retrieve credentials
        self.creds = self.flow.run_local_server(port=8080)            
        # Build the Google Drive API service object using the retrieved credentials
        self.service = build('drive', 'v3', credentials=self.creds)

    def on_created(self, event):
        # This method is called when a file or directory is created in the monitored directory
        item_path = event.src_path  # Get the path of the created item
        item_name = os.path.basename(item_path)  # Get the name of the created item

        # Check if the created item is a directory
        if os.path.isdir(item_path):  
            print("Directory created ...")
            print("Converting to ZIP....")
            
            try:
                time.sleep(1)  # Small delay before archiving
                # Convert the directory to a ZIP file
                shutil.make_archive(item_path, "zip", item_path)  
            except Exception as e:
                print(f"An exception occurred: {e}")    
            print("Successfully converted..")

            try:
                # Remove the original directory after zipping
                shutil.rmtree(item_path)   
                print(f"{item_name} directory successfully deleted..")
            except FileNotFoundError:
                print(f"Directory does not exist: {item_path}") 
            except Exception as e:
                print(f"An unexpected exception occurred: {e}")    

        else:
            # If the created item is a file, log its creation and upload it to Google Drive
            print(f"File created: {item_name}") 
            time.sleep(1)  # Small delay before upload
            self.upload(item_path)

    def upload(self, item_path):
        # Upload the specified file to Google Drive

        # Define metadata for the file to be uploaded
        meta_file = {
            'name': os.path.basename(item_path),  # Name of the file on Google Drive
            'parents': ['Replace']  # Replace with your folder last part url id in drive
        }
        
        try:
            # Create a media object for the file to be uploaded
            media = MediaFileUpload(item_path)  
        except PermissionError as e:
            print(f'Permission error: {e}. Retrying...')   

        try:
            # Upload the file to Google Drive using the service object
            file = self.service.files().create(
                body=meta_file,  # Metadata for the file
                media_body=media,  # File content
                fields='id'  # Request the file ID as the response
            ).execute()
            print(f"File uploaded successfully: {file.get('id')}")
        except Exception as e:
            print(f"An error occurred during upload: {e}")   
        finally:
            del media  # Delete the media object to free resources
            self.remove(item_path)  # Calling remove function for deleting local file after successful upload

    def remove(self, item_path): 
        # Delete the local file after it has been successfully uploaded
        for attempt in range(5):
            try:
                os.remove(item_path)  # Attempt to delete the file
                print(f'Local file {item_path} successfully deleted.')
                break  # Exit the loop if the file is deleted successfully
            except OSError as e:
                print(f'Attempt {attempt + 1} - Error: {e}')
                time.sleep(1)  # Wait before retrying in case of failure


if __name__ == "__main__":
    # Directory path to be monitored, Replace with yours.
    path = "D:\\Backup"        

    event_handler = Listener()  # Create an instance of the custom event handler
    observer = Observer()  # Create an observer object
    # Schedule the observer to monitor the specified directory path using the event handler
    observer.schedule(event_handler, path)

    observer.start()  # Start the observer to begin monitoring
    print(f"Monitoring directory: {os.path.basename(path)}")

    try:
        while True:
            time.sleep(1)  # Keep the script running to allow continuous monitoring
    except KeyboardInterrupt:  # Stop monitoring on user interruption (Ctrl+C)
        observer.stop()
    observer.join()  # Ensure the observer thread terminates properly
