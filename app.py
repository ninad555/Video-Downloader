import streamlit as st
import os
import pandas as pd
from pytube import YouTube
import instaloader
import re
import datetime
import requests
from urllib.parse import urlparse

# Set page configuration
st.set_page_config(
    page_title="Video Downloader",
    page_icon="🎬",
    layout="wide"
)

# Create a session state to store download history
if 'download_history' not in st.session_state:
    st.session_state.download_history = []

def is_valid_path(path):
    """Check if the provided path is valid and exists."""
    return os.path.exists(path)

def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_youtube_video(url, output_path, filename):
    """Download a YouTube video."""
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        
        # Sanitize filename and add extension
        safe_filename = sanitize_filename(filename)
        if not safe_filename.endswith('.mp4'):
            safe_filename += '.mp4'
            
        # Download the video
        output_file = os.path.join(output_path, safe_filename)
        video.download(output_path=output_path, filename=safe_filename)
        
        # Add to download history
        st.session_state.download_history.append({
            'Filename': safe_filename,
            'Source': 'YouTube',
            'URL': url,
            'Path': output_file,
            'Date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        return True, f"Downloaded: {safe_filename}"
    except Exception as e:
        return False, f"Error downloading YouTube video: {str(e)}"

def download_instagram_video(url, output_path, filename):
    """Download an Instagram video."""
    try:
        # Extract post shortcode from URL
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 1:
            shortcode = path_parts[0]
        else:
            return False, "Invalid Instagram URL"
        
        # Initialize Instaloader
        L = instaloader.Instaloader(
            dirname_pattern=output_path,
            filename_pattern=filename,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False
        )
        
        # Download the post
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Sanitize filename and add extension
        safe_filename = sanitize_filename(filename)
        if not safe_filename.endswith('.mp4'):
            safe_filename += '.mp4'
            
        # Only download if it's a video
        if post.is_video:
            L.download_post(post, target=safe_filename)
            
            # Add to download history
            output_file = os.path.join(output_path, safe_filename)
            st.session_state.download_history.append({
                'Filename': safe_filename,
                'Source': 'Instagram',
                'URL': url,
                'Path': output_file,
                'Date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return True, f"Downloaded: {safe_filename}"
        else:
            return False, "The Instagram post is not a video."
    except Exception as e:
        return False, f"Error downloading Instagram video: {str(e)}"

def get_files_in_directory(directory):
    """Get a list of all files in the specified directory."""
    files = []
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                file_created = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                files.append({
                    'Filename': file,
                    'Path': file_path,
                    'Size (KB)': round(file_size / 1024, 2),
                    'Created': file_created.strftime("%Y-%m-%d %H:%M:%S")
                })
    return files

def export_to_excel(data, output_path):
    """Export data to Excel file."""
    if not data:
        return False, "No data to export"
    
    try:
        df = pd.DataFrame(data)
        excel_path = os.path.join(output_path, f"downloaded_files_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        df.to_excel(excel_path, index=False)
        return True, f"Exported to {excel_path}"
    except Exception as e:
        return False, f"Error exporting to Excel: {str(e)}"

# Main application UI
st.title("🎬 Video Downloader")
st.subheader("Download videos from YouTube and Instagram")

# Use radio buttons for navigation instead of tabs
page = st.sidebar.radio("Navigation", ["Download Videos", "View Downloaded Files", "Export to Excel"])

if page == "Download Videos":
    st.header("Download Videos")
    
    # Input fields
    url = st.text_input("Enter YouTube or Instagram video URL")
    filename = st.text_input("Enter desired filename (without extension)")
    output_path = st.text_input("Enter download path", value=os.path.expanduser("~/Downloads"))
    
    # Platform selection
    platform = st.radio("Select platform", ["YouTube", "Instagram", "Auto-detect"])
    
    # Download button
    if st.button("Download Video"):
        if not url:
            st.error("Please enter a URL")
        elif not filename:
            st.error("Please enter a filename")
        elif not is_valid_path(output_path):
            st.error("Invalid download path. Please enter a valid directory path.")
        else:
            with st.spinner("Downloading video..."):
                # Auto-detect platform or use selected platform
                if platform == "Auto-detect":
                    if "youtube" in url.lower() or "youtu.be" in url.lower():
                        success, message = download_youtube_video(url, output_path, filename)
                    elif "instagram" in url.lower() or "insta.gr" in url.lower():
                        success, message = download_instagram_video(url, output_path, filename)
                    else:
                        success, message = False, "Could not detect platform from URL"
                elif platform == "YouTube":
                    success, message = download_youtube_video(url, output_path, filename)
                else:  # Instagram
                    success, message = download_instagram_video(url, output_path, filename)
                
                if success:
                    st.success(message)
                else:
                    st.error(message)

elif page == "View Downloaded Files":
    st.header("View Downloaded Files")
    
    # Input for directory to scan
    scan_path = st.text_input("Enter path to scan for files", value=os.path.expanduser("~/Downloads"))
    
    if st.button("Scan Directory"):
        if not is_valid_path(scan_path):
            st.error("Invalid path. Please enter a valid directory path.")
        else:
            files = get_files_in_directory(scan_path)
            if files:
                st.dataframe(pd.DataFrame(files))
            else:
                st.info(f"No files found in {scan_path}")
    
    # Show download history
    st.subheader("Download History")
    if st.session_state.download_history:
        st.dataframe(pd.DataFrame(st.session_state.download_history))
    else:
        st.info("No download history yet")

elif page == "Export to Excel":
    st.header("Export to Excel")
    
    export_option = st.radio("What would you like to export?", 
                            ["Download History", "Files in Directory"])
    
    export_path = st.text_input("Enter path to save Excel file", value=os.path.expanduser("~/Downloads"))
    
    if export_option == "Files in Directory":
        directory_to_export = st.text_input("Enter directory to export files from", 
                                          value=os.path.expanduser("~/Downloads"))
    
    if st.button("Export to Excel"):
        if not is_valid_path(export_path):
            st.error("Invalid export path. Please enter a valid directory path.")
        else:
            if export_option == "Download History":
                if not st.session_state.download_history:
                    st.warning("No download history to export")
                else:
                    success, message = export_to_excel(st.session_state.download_history, export_path)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            else:  # Files in Directory
                if not is_valid_path(directory_to_export):
                    st.error("Invalid directory path")
                else:
                    files = get_files_in_directory(directory_to_export)
                    if not files:
                        st.warning(f"No files found in {directory_to_export}")
                    else:
                        success, message = export_to_excel(files, export_path)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)

# Footer
st.markdown("---")
st.markdown("### How to use this app")
st.markdown("""
1. Enter the URL of a YouTube or Instagram video
2. Provide a desired filename
3. Specify the download path
4. Click 'Download Video'
5. View your downloaded files in the 'View Downloaded Files' section
6. Export file lists to Excel in the 'Export to Excel' section
""")