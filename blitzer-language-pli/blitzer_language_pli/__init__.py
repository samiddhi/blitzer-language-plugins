"""Pali language plugin for blitzer.

Copyright (C) 2025 Samiddhi

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/.
"""

import os
from pathlib import Path
import requests


def normalizer_func(text: str) -> str:
    """
    Normalize pali notation to ensure exclusion list and text are not mismatched.
    DPD database handles all compounds without (') chars
    """
    return text.replace("ṁ", "ṃ").replace("'", "").replace("”", "").replace("’", "")


def _get_db_path():
    """Get the path to the database file, downloading if necessary."""
    # Check if we're in a development environment (editable install)
    # by looking for the source file in the same directory
    local_db_path = Path(__file__).parent / "lemmas.db"
    if local_db_path.exists():
        return str(local_db_path)
    
    # Use a cache directory in the user's home directory for production
    cache_dir = Path.home() / ".blitzer_language_pli"
    cache_dir.mkdir(exist_ok=True)
    
    db_path = cache_dir / "lemmas.db"
    
    # If database doesn't exist, download it
    if not db_path.exists():
        print(f"Downloading Pali language database to {db_path}...")
        url = "https://github.com/samiddhi/blitzer-language-plugins/releases/download/v1-pli-db/lemmas.db"
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
        "normalizer": normalizer_func,
        "tokenizer": None,  # Use core tokenizer
        "custom_lemmatizer": None  # Use core lemmatizer
    }