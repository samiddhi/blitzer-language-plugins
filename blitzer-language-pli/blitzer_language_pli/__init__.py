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


def register():
    """Register function that returns language configuration."""
    # Get the path to your bundled database file
    db_path = str(Path(__file__).parent / "lemmas.db")
    
    return {
        "db_path": db_path,
        "normalizer": normalizer_func,
        "tokenizer": None,  # Use core tokenizer
        "custom_lemmatizer": None  # Use core lemmatizer
    }