"""
Unit tests for NpcTraceDataset class

Tests the dataset loader for proper error handling and validation
of NPC trace data from JSON files.
"""

import unittest
import os
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent))

from npc_trace_dataset import NpcTraceDataset


class TestNpcTraceDataset(unittest.TestCase):
    """Test cases for NpcTraceDataset class"""
    
    def setUp(self):
        """Set up test data directory path"""
        self.test_data_dir = Path(__file__).parent / 'test_data'
    
    def test_load_valid_data(self):
        """Test loading a valid trace data file"""
        file_path = self.test_data_dir / 'valid_trace_data.json'
        dataset = NpcTraceDataset.load(str(file_path))
        
        self.assertEqual(len(dataset), 3)
        self.assertEqual(len(dataset.get_validation_errors()), 0)
        
        # Check first example
        example = dataset[0]
        self.assertEqual(example['state'], 'idle')
        self.assertEqual(example['input'], 'Hello, NPC!')
        self.assertIn('Greetings', example['expected_output'])
    
    def test_load_missing_state_strict(self):
        """Test that missing 'state' field raises KeyError in strict mode"""
        file_path = self.test_data_dir / 'missing_state.json'
        
        with self.assertRaises(KeyError) as context:
            NpcTraceDataset.load(str(file_path), strict=True)
        
        self.assertIn('state', str(context.exception))
    
    def test_load_missing_input_strict(self):
        """Test that missing 'input' field raises KeyError in strict mode"""
        file_path = self.test_data_dir / 'missing_input.json'
        
        with self.assertRaises(KeyError) as context:
            NpcTraceDataset.load(str(file_path), strict=True)
        
        self.assertIn('input', str(context.exception))
    
    def test_load_missing_expected_output_strict(self):
        """Test that missing 'expected_output' field raises KeyError in strict mode"""
        file_path = self.test_data_dir / 'missing_expected_output.json'
        
        with self.assertRaises(KeyError) as context:
            NpcTraceDataset.load(str(file_path), strict=True)
        
        self.assertIn('expected_output', str(context.exception))
    
    def test_load_missing_fields_non_strict(self):
        """Test that missing fields are handled gracefully in non-strict mode"""
        file_path = self.test_data_dir / 'multiple_missing_fields.json'
        
        # Should not raise, but log errors
        dataset = NpcTraceDataset.load(str(file_path), strict=False)
        
        # Only the first example is valid
        self.assertEqual(len(dataset), 1)
        
        # Should have validation errors for the other two
        errors = dataset.get_validation_errors()
        self.assertEqual(len(errors), 2)
        
        # Verify the valid example was loaded
        example = dataset[0]
        self.assertEqual(example['state'], 'idle')
    
    def test_load_invalid_json(self):
        """Test that invalid JSON raises ValueError"""
        file_path = self.test_data_dir / 'invalid_json.json'
        
        with self.assertRaises(ValueError) as context:
            NpcTraceDataset.load(str(file_path))
        
        self.assertIn('Invalid JSON', str(context.exception))
    
    def test_load_none_values_strict(self):
        """Test that None values for required fields raise ValueError in strict mode"""
        file_path = self.test_data_dir / 'none_values.json'
        
        with self.assertRaises(ValueError) as context:
            NpcTraceDataset.load(str(file_path), strict=True)
        
        self.assertIn('None values', str(context.exception))
    
    def test_load_not_a_list(self):
        """Test that non-list JSON data raises ValueError"""
        file_path = self.test_data_dir / 'not_a_list.json'
        
        with self.assertRaises(ValueError) as context:
            NpcTraceDataset.load(str(file_path))
        
        self.assertIn('Expected a list', str(context.exception))
    
    def test_load_nonexistent_file(self):
        """Test that loading a nonexistent file raises FileNotFoundError"""
        file_path = self.test_data_dir / 'nonexistent_file.json'
        
        with self.assertRaises(FileNotFoundError):
            NpcTraceDataset.load(str(file_path))
    
    def test_get_examples(self):
        """Test get_examples method"""
        file_path = self.test_data_dir / 'valid_trace_data.json'
        dataset = NpcTraceDataset.load(str(file_path))
        
        examples = dataset.get_examples()
        self.assertIsInstance(examples, list)
        self.assertEqual(len(examples), 3)
    
    def test_indexing(self):
        """Test dataset indexing"""
        file_path = self.test_data_dir / 'valid_trace_data.json'
        dataset = NpcTraceDataset.load(str(file_path))
        
        # Test valid index
        example = dataset[1]
        self.assertEqual(example['state'], 'quest_active')
        
        # Test invalid index
        with self.assertRaises(IndexError):
            _ = dataset[99]
    
    def test_repr(self):
        """Test string representation"""
        file_path = self.test_data_dir / 'valid_trace_data.json'
        dataset = NpcTraceDataset.load(str(file_path))
        
        repr_str = repr(dataset)
        self.assertIn('NpcTraceDataset', repr_str)
        self.assertIn('examples=3', repr_str)
        self.assertIn('errors=0', repr_str)


class TestNpcTraceDatasetErrorMessages(unittest.TestCase):
    """Test that error messages are informative"""
    
    def setUp(self):
        """Set up test data directory path"""
        self.test_data_dir = Path(__file__).parent / 'test_data'
    
    def test_error_message_includes_field_name(self):
        """Test that error messages include the missing field name"""
        file_path = self.test_data_dir / 'missing_state.json'
        
        try:
            NpcTraceDataset.load(str(file_path), strict=True)
            self.fail("Expected KeyError to be raised")
        except KeyError as e:
            # Error message should mention 'state'
            self.assertIn('state', str(e).lower())
    
    def test_error_message_includes_example_index(self):
        """Test that error messages include the example index"""
        file_path = self.test_data_dir / 'missing_state.json'
        
        try:
            NpcTraceDataset.load(str(file_path), strict=True)
            self.fail("Expected KeyError to be raised")
        except KeyError as e:
            # Error message should mention the example number
            self.assertIn('0', str(e))


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
