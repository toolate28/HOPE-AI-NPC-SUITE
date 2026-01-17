"""
NpcTraceDataset - A dataset loader for NPC trace data

This module provides a dataset class for loading and managing NPC trace examples
from JSON files. Each example should contain state, input, and expected_output fields.
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path


class NpcTraceDataset:
    """
    Dataset class for loading NPC trace examples from JSON files.
    
    Each example in the dataset should have the following required fields:
    - state: The current state of the NPC
    - input: The input to the NPC
    - expected_output: The expected output from the NPC
    """
    
    def __init__(self):
        """Initialize an empty NpcTraceDataset."""
        self.examples: List[Dict[str, Any]] = []
        self.validation_errors: List[str] = []
    
    @staticmethod
    def load(file_path: str, strict: bool = True) -> 'NpcTraceDataset':
        """
        Load NPC trace examples from a JSON file.
        
        Args:
            file_path: Path to the JSON file containing trace examples
            strict: If True, raises an exception when required fields are missing.
                   If False, logs errors and skips invalid examples.
        
        Returns:
            NpcTraceDataset instance with loaded examples
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
            ValueError: If the file is not valid JSON or required fields are missing (when strict=True)
            KeyError: If required fields are missing (when strict=True)
        """
        dataset = NpcTraceDataset()
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(f"Trace data file not found: {file_path}")
        
        # Load JSON data
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {file_path}: {e}")
        
        # Ensure data is a list of examples
        if not isinstance(data, list):
            raise ValueError(f"Expected a list of examples in {file_path}, got {type(data).__name__}")
        
        # Required fields for each example
        required_fields = ['state', 'input', 'expected_output']
        
        # Validate and load each example
        for idx, example in enumerate(data):
            if not isinstance(example, dict):
                error_msg = f"Example {idx} is not a dictionary, got {type(example).__name__}"
                if strict:
                    raise ValueError(error_msg)
                else:
                    dataset.validation_errors.append(error_msg)
                    continue
            
            # Check for missing required fields
            missing_fields = [field for field in required_fields if field not in example]
            
            if missing_fields:
                error_msg = f"Example {idx} missing required fields: {', '.join(missing_fields)}"
                if strict:
                    raise KeyError(error_msg)
                else:
                    dataset.validation_errors.append(error_msg)
                    continue
            
            # Validate that fields are not None
            none_fields = [field for field in required_fields if example.get(field) is None]
            if none_fields:
                error_msg = f"Example {idx} has None values for required fields: {', '.join(none_fields)}"
                if strict:
                    raise ValueError(error_msg)
                else:
                    dataset.validation_errors.append(error_msg)
                    continue
            
            # Add valid example
            dataset.examples.append(example)
        
        return dataset
    
    def get_examples(self) -> List[Dict[str, Any]]:
        """
        Get all loaded examples.
        
        Returns:
            List of example dictionaries
        """
        return self.examples
    
    def get_validation_errors(self) -> List[str]:
        """
        Get validation errors that occurred during loading (in non-strict mode).
        
        Returns:
            List of error messages
        """
        return self.validation_errors
    
    def __len__(self) -> int:
        """Return the number of examples in the dataset."""
        return len(self.examples)
    
    def __getitem__(self, idx: int) -> Dict[str, Any]:
        """
        Get an example by index.
        
        Args:
            idx: Index of the example
            
        Returns:
            Example dictionary
            
        Raises:
            IndexError: If index is out of range
        """
        return self.examples[idx]
    
    def __repr__(self) -> str:
        """Return string representation of the dataset."""
        return f"NpcTraceDataset(examples={len(self.examples)}, errors={len(self.validation_errors)})"
