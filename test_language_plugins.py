import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import tempfile

class TestLanguagePlugins(unittest.TestCase):
    
    def test_pli_register_function_exists(self):
        """Test that the Pali register function exists and returns expected structure."""
        # Add the plugin directory so we can import the module
        pli_path = Path(__file__).parent / "blitzer-language-pli"
        sys.path.insert(0, str(pli_path))
        
        import blitzer_language_pli
        config = blitzer_language_pli.register()
        
        self.assertIn("db_path", config)
        self.assertIn("normalizer", config)
        self.assertIn("tokenizer", config)
        self.assertIn("custom_lemmatizer", config)
        
        # Test that normalizer function works
        normalizer = config["normalizer"]
        self.assertIsNotNone(normalizer)
        result = normalizer("saṁyuttaṁ")
        self.assertEqual(result, "saṃyuttaṃ")
    
    def test_slv_register_function_exists(self):
        """Test that the Slovenian register function exists and returns expected structure."""
        # Reset sys.path and add the SLV plugin directory
        sys.path = [p for p in sys.path if "blitzer-language-pli" not in p]  # Remove old if any
        slv_path = Path(__file__).parent / "blitzer-language-slv"
        sys.path.insert(0, str(slv_path))
        
        import blitzer_language_slv
        config = blitzer_language_slv.register()
        
        self.assertIn("db_path", config)
        self.assertIn("normalizer", config)
        self.assertIn("tokenizer", config)
        self.assertIn("custom_lemmatizer", config)
        
        # Normalizer should be None for SLV
        self.assertIsNone(config["normalizer"])
    
    def test_pli_download_mechanism(self):
        """Test that the Pali download mechanism is called without actually downloading."""
        # Add the plugin directory so we can import the module
        pli_path = Path(__file__).parent / "blitzer-language-pli"
        sys.path.insert(0, str(pli_path))
        
        # Mock Path.exists to return False so we test the download functionality
        with patch.object(Path, 'exists', return_value=False), \
             patch('requests.get') as mock_get:
            
            # Mock the response
            mock_response = MagicMock()
            mock_response.iter_content.return_value = [b"test_chunk"]
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            # Use a temporary directory as home
            with tempfile.TemporaryDirectory() as temp_dir:
                with patch('pathlib.Path.home', return_value=Path(temp_dir)):
                    import blitzer_language_pli
                    config = blitzer_language_pli.register()
                    
                    # Verify that requests.get was called with the correct URL
                    mock_get.assert_called_once()
                    args, kwargs = mock_get.call_args
                    self.assertEqual(args[0], "https://github.com/samiddhi/blitzer-language-plugins/releases/download/v1-pli-db/lemmas.db")
                    
                    # Verify that the returned path is correct
                    self.assertTrue(config["db_path"].endswith("lemmas.db"))
    
    def test_pli_local_db_file_takes_precedence(self):
        """Test that a local database file is used in preference to downloading."""
        # Add the plugin directory so we can import the module
        pli_path = Path(__file__).parent / "blitzer-language-pli"
        sys.path.insert(0, str(pli_path))
        
        # Mock Path.exists to return True for local file
        with patch.object(Path, 'exists', return_value=True):
            import blitzer_language_pli
            config = blitzer_language_pli.register()
            
            # The path should point to the local file
            self.assertTrue(config["db_path"].endswith("lemmas.db"))
            self.assertIn("blitzer_language_pli", config["db_path"])

    def test_db_path_structure_with_local_file(self):
        """Test that the DB path has the expected structure when local file exists."""
        pli_path = Path(__file__).parent / "blitzer-language-pli"
        sys.path.insert(0, str(pli_path))
        
        # Create a temporary directory and use it as home
        with patch.object(Path, 'exists', return_value=True):  # Pretend local DB exists
            import blitzer_language_pli
            config = blitzer_language_pli.register()
            
            db_path = Path(config["db_path"])
            self.assertTrue(db_path.name == "lemmas.db")
            # When local DB exists, it should be in the same directory as __init__.py
            self.assertTrue("blitzer_language_pli" in str(db_path.parent))


if __name__ == '__main__':
    unittest.main()