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

from pathlib import Path


def _get_db_path():
    """Get the path to the lemmas.db file, downloading it if necessary."""
    # Import requests here to ensure it's available
    import requests
    
    # Use a cache directory in user's home folder
    cache_dir = Path.home() / ".blitzer_language_slv"
    cache_dir.mkdir(exist_ok=True)
    db_path = cache_dir / "lemmas.db"
    
    if not db_path.exists():
        print(f"Downloading Slovenian lemmas database to {db_path}...")
        url = "https://github.com/samiddhi/blitzer-language-plugins/releases/download/v1-slv-db/lemmas.db"
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(db_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("Download completed successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to download Slovenian lemmas database: {e}")
    
    return str(db_path)


def register():
    """Register function that returns language configuration."""
    db_path = _get_db_path()
    
    return {
        "db_path": db_path,
        "normalizer": None,  # No special normalization needed
        "tokenizer": None,  # Use core tokenizer
        "custom_lemmatizer": None  # Use core lemmatizer
    }