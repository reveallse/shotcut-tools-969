import os
import re
import datetime
from pathlib import Path
import mutagen  # For handling media file metadata

def get_video_metadata(file_path):
    """
    Get metadata from a video file.
    Returns a dictionary with relevant metadata or None if not found.
    """
    try:
        video = mutagen.File(file_path)
        if video is not None and video.tags:
            metadata = {}
            
            # Try to get title from various tag formats
            if hasattr(video.tags, 'get'):
                metadata['title'] = (video.tags.get('TIT2') or 
                                   video.tags.get('\xa9nam') or 
                                   video.tags.get('TITLE'))
            
            # Get duration from info
            if hasattr(video, 'info') and hasattr(video.info, 'length'):
                metadata['duration'] = video.info.length
            
            # Try to get creation date from various tag formats
            if hasattr(video.tags, 'get'):
                metadata['creation_date'] = (video.tags.get('TDRC') or 
                                            video.tags.get('\xa9day') or 
                                            video.tags.get('DATE'))
            
            return {k: v for k, v in metadata.items() if v is not None}
        else:
            print(f"No metadata found for {file_path}")
            return None
    except Exception as e:
        print(f"Error reading metadata for {file_path}: {e}")
        return None

def rename_file(file_path, new_name):
    """
    Rename a file to a new name.
    Handles potential errors when renaming.
    """
    try:
        directory = os.path.dirname(file_path)
        new_file_path = os.path.join(directory, new_name)
        os.rename(file_path, new_file_path)
        print(f"Renamed '{file_path}' to '{new_file_path}'")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except PermissionError:
        print(f"Permission denied when trying to rename: {file_path}")
    except Exception as e:
        print(f"Error renaming file {file_path}: {e}")

def generate_new_filename(metadata, pattern="{title}_{date}.mp4"):
    """
    Generate a new filename based on the provided metadata and a pattern.
    Supports placeholders: {title}, {date}.
    """
    try:
        title = metadata.get('title', 'Untitled')
        if hasattr(title, '__iter__') and not isinstance(title, str):
            title = str(title[0]) if title else 'Untitled'
        
        creation_date = metadata.get('creation_date', datetime.datetime.now().isoformat())
        
        # Handle different date formats
        if isinstance(creation_date, str):
            try:
                formatted_date = datetime.datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S").strftime("%Y%m%d")
            except ValueError:
                try:
                    # Try YYYY format common in metadata
                    formatted_date = datetime.datetime.strptime(creation_date[:4], "%Y").strftime("%Y%m%d")
                except ValueError:
                    # Fallback to current date if parsing fails
                    formatted_date = datetime.datetime.now().strftime("%Y%m%d")
        else:
            formatted_date = datetime.datetime.now().strftime("%Y%m%d")

        new_name = pattern.format(title=title, date=formatted_date)
        # Clean up the filename to avoid illegal characters
        new_name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', new_name)
        return new_name
    except Exception as e:
        print(f"Error generating filename: {e}")
        return None

def validate_file_extension(file_path):
    """
    Validate if the file has a video extension.
    Returns True if valid, False otherwise.
    """
    valid_extensions = {'.mp4', '.mov', '.avi', '.mkv'}
    return Path(file_path).suffix.lower() in valid_extensions

# TODO: Add more metadata extraction options (e.g. from different file types)
# TODO: Implement logging instead of print statements for better debugging
# TODO: Create unit tests for utility functions to ensure reliability
