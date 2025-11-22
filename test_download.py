#!/usr/bin/env python3
"""
Test script to verify the download functionality works properly.
"""

import sys
import os
from pathlib import Path

def test_pli():
    """Test Pali plugin download functionality."""
    print("Testing Pali plugin download functionality...")
    
    # Add the plugin directory to the path so we can import it
    pli_path = Path(__file__).parent / "blitzer-language-pli"
    sys.path.insert(0, str(pli_path))
    
    try:
        import blitzer_language_pli
        config = blitzer_language_pli.register()
        db_path = config["db_path"]
        print(f"Pali plugin DB path: {db_path}")
        print(f"Pali plugin normalizer function available: {config['normalizer'] is not None}")
        
        # Test the normalizer function
        test_text = "saṁyuttaṁ"
        normalized = config["normalizer"](test_text)
        print(f"Normalizer test - Input: {test_text}, Output: {normalized}")
        
        print("Pali plugin test completed successfully.")
    except Exception as e:
        print(f"Error testing Pali plugin: {e}")
        import traceback
        traceback.print_exc()


def test_slv():
    """Test Slovenian plugin download functionality."""
    print("\nTesting Slovenian plugin download functionality...")
    
    # Reset sys.path and add the SLV plugin directory
    slv_path = Path(__file__).parent / "blitzer-language-slv"
    # Remove any previous plugin paths to avoid conflicts
    sys.path = [p for p in sys.path if "blitzer-language" not in p]
    sys.path.insert(0, str(slv_path))
    
    try:
        import blitzer_language_slv
        config = blitzer_language_slv.register()
        db_path = config["db_path"]
        print(f"Slovenian plugin DB path: {db_path}")
        print(f"Slovenian plugin normalizer function available: {config['normalizer'] is None}")
        
        print("Slovenian plugin test completed successfully.")
    except Exception as e:
        print(f"Error testing Slovenian plugin: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_pli()
    test_slv()
    print("\nAll tests completed.")