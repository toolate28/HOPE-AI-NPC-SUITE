# NPC Trace Dataset Module

## Overview

The `NpcTraceDataset` module provides a robust dataset loader for NPC trace examples stored in JSON format. It includes comprehensive error handling for missing or invalid data, preventing unhandled `KeyError` exceptions.

## Features

- ✅ **Robust Error Handling**: Prevents crashes from missing required fields
- ✅ **Flexible Loading Modes**: Strict mode (raises exceptions) or non-strict mode (logs errors)
- ✅ **Clear Error Messages**: Informative messages that include field names and example indices
- ✅ **Validation**: Checks for required fields, None values, and proper data structure
- ✅ **Easy to Use**: Simple API for loading and accessing trace data

## Installation

No additional dependencies required beyond Python 3.6+. The module uses only standard library imports.

## Usage

### Basic Usage

```python
from npc_trace_dataset import NpcTraceDataset

# Load trace data (strict mode by default)
dataset = NpcTraceDataset.load('path/to/trace_data.json')

# Access examples
print(f"Loaded {len(dataset)} examples")
for example in dataset.get_examples():
    print(f"State: {example['state']}")
    print(f"Input: {example['input']}")
    print(f"Expected: {example['expected_output']}")
```

### Non-Strict Mode

```python
# Load with non-strict mode (skips invalid examples)
dataset = NpcTraceDataset.load('path/to/trace_data.json', strict=False)

# Check validation errors
errors = dataset.get_validation_errors()
if errors:
    print(f"Found {len(errors)} validation errors:")
    for error in errors:
        print(f"  - {error}")
```

### Error Handling

```python
try:
    dataset = NpcTraceDataset.load('trace_data.json', strict=True)
except FileNotFoundError as e:
    print(f"File not found: {e}")
except KeyError as e:
    print(f"Missing required field: {e}")
except ValueError as e:
    print(f"Invalid data format: {e}")
```

## JSON Format

Each trace data file should contain a JSON array of examples. Each example must have the following required fields:

```json
[
  {
    "state": "idle",
    "input": "Hello, NPC!",
    "expected_output": "Greetings, traveler!"
  },
  {
    "state": "quest_active",
    "input": "Help with quest",
    "expected_output": "Check the eastern ruins"
  }
]
```

### Required Fields

- **`state`**: The current state of the NPC (string)
- **`input`**: The input to the NPC (string)
- **`expected_output`**: The expected output from the NPC (string)

## API Reference

### `NpcTraceDataset`

Main class for loading and managing NPC trace data.

#### Methods

##### `load(file_path: str, strict: bool = True) -> NpcTraceDataset`

Load trace examples from a JSON file.

**Parameters:**
- `file_path` (str): Path to the JSON file
- `strict` (bool): If True, raises exceptions for missing fields. If False, logs errors and skips invalid examples.

**Returns:** 
- `NpcTraceDataset`: Instance with loaded examples

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `ValueError`: If JSON is invalid or data structure is wrong
- `KeyError`: If required fields are missing (strict mode only)

##### `get_examples() -> List[Dict[str, Any]]`

Get all loaded examples.

**Returns:** List of example dictionaries

##### `get_validation_errors() -> List[str]`

Get validation errors from loading (non-strict mode only).

**Returns:** List of error messages

##### `__len__() -> int`

Get the number of examples in the dataset.

##### `__getitem__(idx: int) -> Dict[str, Any]`

Access an example by index.

**Parameters:**
- `idx` (int): Index of the example

**Returns:** Example dictionary

**Raises:**
- `IndexError`: If index is out of range

## Testing

Run the test suite:

```bash
cd python-scripts
python3 test_npc_trace_dataset.py
```

Run the demo script:

```bash
cd python-scripts
python3 demo_npc_trace_dataset.py
```

## Example Test Data

The module includes several test data files in `python-scripts/test_data/`:

- `valid_trace_data.json`: Valid examples
- `missing_state.json`: Missing 'state' field
- `missing_input.json`: Missing 'input' field
- `missing_expected_output.json`: Missing 'expected_output' field
- `multiple_missing_fields.json`: Multiple examples with various missing fields
- `invalid_json.json`: Malformed JSON
- `none_values.json`: Examples with None values
- `not_a_list.json`: Invalid structure (not a list)

## Error Messages

The module provides clear, informative error messages:

- **Missing fields**: `"Example 0 missing required fields: state, input"`
- **None values**: `"Example 1 has None values for required fields: state"`
- **Invalid structure**: `"Expected a list of examples in file.json, got dict"`
- **Invalid JSON**: `"Invalid JSON in file.json: Expecting ',' delimiter: line 3 column 5 (char 50)"`

## Integration with HOPE NPCs

This module is designed to support training and testing of AI-powered NPCs in the HOPE NPCs (Human-Operated Personality Engines) ecosystem. It can be used to:

1. Load training examples for NPC behavior
2. Test NPC responses against expected outputs
3. Validate conversation traces
4. Build datasets for fine-tuning NPC models

## Contributing

When adding new functionality:

1. Ensure all required fields are validated
2. Provide clear error messages with context
3. Add tests for new features
4. Update this README with examples

## License

Part of the HOPE NPCs / SpiralSafe ecosystem. See main repository LICENSE.

---

*Built with ❤️ by Hope&&Sauced*
