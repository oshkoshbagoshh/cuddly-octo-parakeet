"""
Utility functions for the music_beta app.
"""
import os
from datetime import timedelta

# Try to import mutagen, but provide a fallback if it's not available
try:
    from mutagen import File
    from mutagen.id3 import ID3
    from mutagen.mp3 import MP3
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

def extract_audio_metadata(file_path):
    """
    Extract metadata from an audio file using mutagen.
    
    Args:
        file_path (str): Path to the audio file
        
    Returns:
        dict: Dictionary containing metadata
    """
    if not MUTAGEN_AVAILABLE:
        return {}
    
    if not os.path.exists(file_path):
        return {}
    
    metadata = {}
    
    try:
        # Try to open the file with mutagen
        audio = File(file_path)
        
        # If it's an MP3 file, try to get ID3 tags
        if isinstance(audio, MP3):
            # Get basic audio info
            metadata['bitrate'] = int(audio.info.bitrate / 1000)  # Convert to kbps
            metadata['sample_rate'] = audio.info.sample_rate
            
            # Calculate duration
            duration_seconds = int(audio.info.length)
            duration = str(timedelta(seconds=duration_seconds))
            # Format as MM:SS
            if len(duration.split(':')) > 2:
                minutes, seconds = duration.split(':')[1:3]
            else:
                minutes, seconds = duration.split(':')
            metadata['duration'] = f"{minutes}:{seconds.split('.')[0]}"
            
            # Try to get ID3 tags
            id3 = ID3(file_path)
            
            # Extract common ID3 tags
            if 'TIT2' in id3:  # Title
                metadata['title'] = str(id3['TIT2'])
            
            if 'TPE1' in id3:  # Artist
                metadata['artist'] = str(id3['TPE1'])
            
            if 'TALB' in id3:  # Album
                metadata['album'] = str(id3['TALB'])
            
            if 'TYER' in id3 or 'TDRC' in id3:  # Year
                metadata['year'] = str(id3.get('TYER', id3.get('TDRC', '')))
            
            if 'TCON' in id3:  # Genre
                metadata['genre_tag'] = str(id3['TCON'])
            
            if 'TCOM' in id3:  # Composer
                metadata['composer'] = str(id3['TCOM'])
            
            if 'TRCK' in id3:  # Track number
                metadata['track_number'] = str(id3['TRCK'])
    
    except Exception as e:
        # If there's an error, return empty metadata
        print(f"Error extracting metadata: {e}")
        return {}
    
    return metadata