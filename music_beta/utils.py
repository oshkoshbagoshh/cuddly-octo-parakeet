"""
Utility functions for the music_beta app.
"""
import os
import numpy as np
from datetime import timedelta

# Try to import mutagen, but provide a fallback if it's not available
try:
    from mutagen import File
    from mutagen.id3 import ID3
    from mutagen.mp3 import MP3
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

# Try to import librosa for audio analysis, but provide a fallback if it's not available
try:
    import librosa
    import librosa.display
    LIBROSA_AVAILABLE = True

    # Define key mapping for librosa key detection
    KEY_MAPPING = {
        0: 'C major',
        1: 'C# major',
        2: 'D major',
        3: 'D# major',
        4: 'E major',
        5: 'F major',
        6: 'F# major',
        7: 'G major',
        8: 'G# major',
        9: 'A major',
        10: 'A# major',
        11: 'B major',
        12: 'C minor',
        13: 'C# minor',
        14: 'D minor',
        15: 'D# minor',
        16: 'E minor',
        17: 'F minor',
        18: 'F# minor',
        19: 'G minor',
        20: 'G# minor',
        21: 'A minor',
        22: 'A# minor',
        23: 'B minor',
    }
except ImportError:
    LIBROSA_AVAILABLE = False

def extract_bpm(file_path):
    """
    Extract beats per minute (BPM) from an audio file using librosa.

    Args:
        file_path (str): Path to the audio file

    Returns:
        float: BPM value or None if extraction fails
    """
    if not LIBROSA_AVAILABLE or not os.path.exists(file_path):
        return None

    try:
        # Load audio file with librosa
        y, sr = librosa.load(file_path)

        # Extract tempo (BPM)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]

        return round(tempo, 2)  # Round to 2 decimal places
    except Exception as e:
        print(f"Error extracting BPM: {e}")
        return None


def extract_key(file_path):
    """
    Extract musical key from an audio file using librosa.

    Args:
        file_path (str): Path to the audio file

    Returns:
        str: Musical key or None if extraction fails
    """
    if not LIBROSA_AVAILABLE or not os.path.exists(file_path):
        return None

    try:
        # Load audio file with librosa
        y, sr = librosa.load(file_path)

        # Extract chroma features
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

        # Compute key using Krumhansl-Schmuckler key-finding algorithm
        key = librosa.feature.tonnetz(y=y, sr=sr)
        chroma_sum = np.sum(chroma, axis=1)
        key_index = np.argmax(chroma_sum)

        # Convert to major/minor key
        if key_index < 12:
            # Use the KEY_MAPPING dictionary to get the key name
            return KEY_MAPPING.get(key_index)
        else:
            # If key_index is out of range, default to C major
            return KEY_MAPPING.get(0)
    except Exception as e:
        print(f"Error extracting key: {e}")
        return None


def extract_audio_metadata(file_path):
    """
    Extract metadata from an audio file using mutagen and librosa.

    Args:
        file_path (str): Path to the audio file

    Returns:
        dict: Dictionary containing metadata
    """
    if not os.path.exists(file_path):
        return {}

    metadata = {}

    # Extract metadata using mutagen if available
    if MUTAGEN_AVAILABLE:
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
            # If there's an error with mutagen, log it but continue
            print(f"Error extracting metadata with mutagen: {e}")

    # Extract BPM and key using librosa if available
    if LIBROSA_AVAILABLE:
        try:
            # Extract BPM
            bpm = extract_bpm(file_path)
            if bpm:
                metadata['bpm'] = bpm

            # Extract key
            key = extract_key(file_path)
            if key:
                metadata['key'] = key

            # TODO: Extract mood from DEAM dataset
            # This would require implementing a model trained on the DEAM dataset
            # For now, we'll leave this as a placeholder

        except Exception as e:
            # If there's an error with librosa, log it
            print(f"Error extracting audio features with librosa: {e}")

    return metadata
