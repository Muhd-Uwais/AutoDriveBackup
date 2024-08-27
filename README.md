# AutoDriveBackup: Automated File Backup and Google Drive Uploader

AutoDriveBackup is a Python-based project that automatically monitors a directory for newly created files or directories. When a new file is created, it is instantly uploaded to Google Drive. If a directory is created, it is compressed into a ZIP file, uploaded to Google Drive, and then deleted locally. This project is ideal for automating backup tasks, ensuring that your important files are safely stored in the cloud.

## Features

- **Real-time Monitoring**: Automatically detects and responds to file and directory creation within the specified directory.
- **Automated Backup**: Compresses newly created directories into ZIP files and uploads them to Google Drive.
- **Local Cleanup**: Deletes local files and directories after successful upload to Google Drive to save disk space.
- **Google Drive Integration**: Seamlessly integrates with Google Drive for secure cloud storage.

## Requirements

- Python 3.6 or later
- Google API Client Libraries
- Watchdog library for directory monitoring

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Muhd-Uwais/AutoDriveBackup.git
    cd AutoDriveBackup
    ```

2. **Install the required Python libraries:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Setup Google API credentials:**

    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project and enable the Google Drive API.
    - Create OAuth 2.0 credentials and download the `client_secret.json` file.
    - Save the `client_secret.json` file in the project directory.

4. **Configure the script:**

    - Update the `CLIENT_SECRET` and `SCOPES` variables in the script with your Google API credentials and desired API scopes.

5. **Run the script:**

    ```bash
    python autobackup.py
    ```

## Usage

- The script will monitor the specified directory for any new files or directories.
- Files are uploaded directly to Google Drive.
- Directories are compressed into ZIP files before being uploaded.
- After successful upload, local files are deleted to free up space.

## Customization

- **Change the monitored directory**: Update the `path` variable in the `if __name__ == "__main__"` section to the directory you want to monitor.
- **Specify Google Drive folder**: Update the `parents` field in the `meta_file` dictionary to the desired Google Drive folder ID where backups should be stored.

## Contributing

AutoDriveBackup is still in its early stages and may have some flaws and issues. If you're interested in improving the project, please feel free to contribute! We welcome pull requests and suggestions for enhancements. Thank you for your support.

## Contact

For any questions or feedback, please reach out to [nox0389@gmail.com](mailto:nox0389@gmail.com).
