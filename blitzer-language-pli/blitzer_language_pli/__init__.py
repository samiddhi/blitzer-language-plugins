"""Pali language plugin for blitzer.

Copyright (C) 2025 Samiddhi

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/.
"""

from pathlib import Path


def normalizer_func(text: str) -> str:
    """
    Normalize pali notation to ensure exclusion list and text are not mismatched.
    DPD database handles all compounds without (') chars
    """
    return text.replace("ṁ", "ṃ").replace("'", "").replace("”", "").replace("’", "")


def _get_db_path():
    """Get the path to the lemmas.db file, downloading it if necessary."""
    # Import requests here to ensure it's available
    import requests
    
    # Use a cache directory in user's home folder
    cache_dir = Path.home() / ".blitzer_language_pli"
    cache_dir.mkdir(exist_ok=True)
    db_path = cache_dir / "lemmas.db"
    
    if not db_path.exists():
        print(f"Downloading Pali lemmas database to {db_path}...")
        url = "https://github.com/samiddhi/blitzer-language-plugins/releases/download/v1-pli-db/lemmas.db"
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(db_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("Download completed successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to download Pali lemmas database: {e}")
    
    return str(db_path)


def register():
    """Register function that returns language configuration."""
    db_path = _get_db_path()
    
    return {
        "db_path": db_path,
        "normalizer": normalizer_func,
        "tokenizer": None,  # Use core tokenizer
        "custom_lemmatizer": None  # Use core lemmatizer
    }