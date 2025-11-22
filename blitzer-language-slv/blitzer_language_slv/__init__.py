"""Slovenian language plugin for blitzer.

Copyright (C) 2025 Samiddhi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
from pathlib import Path
import requests


def _get_db_path():
    """Get the path to the database file, downloading if necessary."""
    # Check if we're in a development environment (editable install)
    # by looking for the source file in the same directory
    local_db_path = Path(__file__).parent / "lemmas.db"
    if local_db_path.exists():
        return str(local_db_path)
    
    # Use a cache directory in the user's home directory for production
    cache_dir = Path.home() / ".blitzer_language_slv"
    cache_dir.mkdir(exist_ok=True)
    
    db_path = cache_dir / "lemmas.db"
    
    # If database doesn't exist, download it
    if not db_path.exists():
        print(f"Downloading Slovenian language database to {db_path}...")
        url = "https://github.com/samiddhi/blitzer-language-plugins/releases/download/v1-slv-db/lemmas.db"
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(db_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("Download completed.")
    
    return str(db_path)


def register():
    """Register function that returns language configuration."""
    # Get the path to your bundled database file (download if needed)
    db_path = _get_db_path()
    
    return {
        "db_path": db_path,
        "normalizer": None,  # No special normalization needed
        "tokenizer": None,  # Use core tokenizer
        "custom_lemmatizer": None  # Use core lemmatizer
    }