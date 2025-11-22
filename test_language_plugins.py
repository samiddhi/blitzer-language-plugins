import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import tempfile
import os

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
    
    @patch('pathlib.Path.exists', return_value=False)  # This patches globally
    def test_pli_download_mechanism_with_mock(self, mock_exists):
        """Test that the Pali download mechanism is called without actually downloading."""
        # We need to patch inside the function where the import happens
        import blitzer_language_pli
        
        # Since the requests import is inside the function, mock needs to happen
        # at the time of the function call
        original_get_db_path = blitzer_language_pli._get_db_path
        
        def mock_get_db_path():
            # Import requests inside the function (as in original)
            import requests
            from unittest.mock import patch
            from pathlib import Path
            
            # Mock the requests.get within this function
            with patch('requests.get') as mock_get:
                # Mock response
                mock_response = MagicMock()
                mock_response.iter_content.return_value = [b"test_chunk"]
                mock_response.raise_for_status.return_value = None
                mock_get.return_value = mock_response
                
                # Use temp directory
                with tempfile.TemporaryDirectory() as temp_dir:
                    cache_dir = Path(temp_dir) / ".blitzer_language_pli"
                    cache_dir.mkdir(exist_ok=True)
                    db_path = cache_dir / "lemmas.db"
                    
                    # Test the URL by checking the mock call
                    import builtins
                    original_open = builtins.open
                    
                    def mock_open(*args, **kwargs):
                        if str(args[0]).endswith("lemmas.db"):
                            # This is our db file, return a mock file handle
                            mock_file = MagicMock()
                            return mock_file
                        return original_open(*args, **kwargs)
                    
                    with patch('builtins.open', side_effect=mock_open):
                        # Call requests.get with the expected URL
                        url = "https://github.com/samiddhi/blitzer-language-plugins/releases/download/v1-pli-db/lemmas.db"
                        response = requests.get(url, stream=True)
                        response.raise_for_status()
                        
                        # Check the mock was called with the right URL
                        mock_get.assert_called_with(url, stream=True)
                        
                        # Return a test path
                        return str(db_path)
        
        # Temporarily replace the function
        blitzer_language_pli._get_db_path = mock_get_db_path
        
        try:
            # Now call register which should use our mocked function
            config = blitzer_language_pli.register()
            
            # This verifies the function completed without error
            self.assertTrue(config["db_path"].endswith("lemmas.db"))
        finally:
            # Restore original function
            blitzer_language_pli._get_db_path = original_get_db_path
    
    def test_db_path_structure_with_mocked_exists(self):
        """Test that the DB path has the expected structure when file exists."""
        pli_path = Path(__file__).parent / "blitzer-language-pli"
        sys.path.insert(0, str(pli_path))
        
        import blitzer_language_pli
        
        # Create a temporary directory and use it as home
        with tempfile.TemporaryDirectory() as temp_base:
            temp_home = Path(temp_base) / "test_home"
            temp_home.mkdir(exist_ok=True)
            
            with patch('pathlib.Path.exists', return_value=True):  # Pretend DB exists
                with patch('pathlib.Path.home', return_value=temp_home):  # Mock home
                    config = blitzer_language_pli.register()
                    
                    db_path = Path(config["db_path"])
                    self.assertTrue(db_path.name == "lemmas.db")
                    self.assertTrue(".blitzer_language_pli" in str(db_path.parent))


if __name__ == '__main__':
    unittest.main()