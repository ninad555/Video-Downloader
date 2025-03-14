# Video Downloader Application

A Streamlit application that allows users to download videos from YouTube and Instagram, save them with custom filenames to a specified path, and export a list of downloaded files to Excel.

## Features

- **Download Videos**: Download videos from YouTube and Instagram with custom filenames
- **Batch Downloads**: Process multiple URLs at once by entering each URL and filename on a separate line
- **File Management**: View downloaded files and download history
- **Export to Excel**: Export the list of downloaded files or download history to an Excel file

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

3. Make sure you have Python 3.7 or higher installed

## Usage

1. Run the application:

2. The application will open in your default web browser

### Downloading Videos

1. Select the platform (YouTube or Instagram)
2. Enter one URL and filename per line in the text area
   - Format: `URL filename` or `URL, filename`
   - Example: `https://youtube.com/watch?v=abcdef MyVideo`
   - Example: `https://instagram.com/p/abcdef, Beach Video`
3. Specify the download path
4. Click "Download Videos"

### Viewing Downloaded Files

1. Navigate to "View Downloaded Files" in the sidebar
2. Enter the path to scan for files
3. Click "Scan Directory" to view all files in that directory
4. Your download history will be displayed below (for the current session)

### Exporting to Excel

1. Navigate to "Export to Excel" in the sidebar
2. Choose what to export: Download History or Files in Directory
3. Specify the export path
4. Preview the data before exporting
5. Click "Export to Excel"

## Requirements

- Python 3.7+
- Streamlit
- yt-dlp
- instaloader
- pandas
- openpyxl

## Troubleshooting

### YouTube Download Issues

If you encounter issues downloading YouTube videos:

1. Make sure yt-dlp is up to date:


2. Check your internet connection and firewall settings
3. Some videos may be restricted and not available for download

### Instagram Download Issues

For Instagram downloads:

1. Some private content may require authentication
2. Instagram's API changes frequently, so updates may be needed

## Notes

- The application maintains download history only for the current session
- All filenames are sanitized to remove invalid characters
- The YouTube downloader gets the highest resolution available for each video

## Legal Disclaimer

This tool is intended for downloading videos for personal use only. 
Please respect copyright laws and terms of service of the platforms.
Do not download or distribute copyrighted content without permission.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
