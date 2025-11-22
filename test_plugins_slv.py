import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the plugin directory so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "blitzer-language-slv"))

class TestSlvPluginDownload(unittest.TestCase):
    
    def test_register_function_exists(self):
        """Test that the register function exists and returns expected structure."""
        import blitzer_language_slv
        config = blitzer_language_slv.register()
        
        self.assertIn("db_path", config)
        self.assertIn("normalizer", config)
        self.assertIn("tokenizer", config)
        self.assertIn("custom_lemmatizer", config)
        
        # Normalizer should be None for SLV
        self.assertIsNone(config["normalizer"])
    
    def test_db_download_mechanism(self):
        """Test that the download mechanism works without actually downloading."""
        import blitzer_language_slv
        
        # We need to patch the import and call at the function level
        # We'll patch both Path.exists (to simulate missing DB) and requests
        from unittest.mock import patch
        with patch('pathlib.Path.exists', return_value=False), \
             patch('blitzer_language_slv.requests.get') as mock_get:
            
            # Mock the response
            mock_response = MagicMock()
            mock_response.iter_content.return_value = [b"test_chunk"]
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            import tempfile
            import os
            with tempfile.TemporaryDirectory() as temp_dir:
                # We'll need to patch the Path.home call to use our temp directory
                with patch('pathlib.Path.home', return_value=Path(temp_dir)):
                    # Call the register function which should trigger download
                    config = blitzer_language_slv.register()
                    
                    # Verify that requests.get was called with the correct URL
                    mock_get.assert_called_once()
                    args, kwargs = mock_get.call_args
                    self.assertEqual(args[0], "https://github.com/samiddhi/blitzer-language-plugins/releases/download/v1-slv-db/lemmas.db")
                    
                    # Verify that the returned path is correct
                    self.assertTrue(config["db_path"].endswith("lemmas.db"))
    
    def test_db_path_structure(self):
        """Test that the DB path has the expected structure."""
        import blitzer_language_slv
        
        with patch('pathlib.Path.exists', return_value=True):  # Pretend DB exists
            config = blitzer_language_slv.register()
            
            db_path = Path(config["db_path"])
            self.assertTrue(db_path.name == "lemmas.db")
            self.assertTrue(".blitzer_language_slv" in str(db_path.parent))

if __name__ == '__main__':
    unittest.main()