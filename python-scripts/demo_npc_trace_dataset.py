"""
Demo script showing how to use NpcTraceDataset

This script demonstrates both strict and non-strict loading modes
and proper error handling for missing fields.
"""

from pathlib import Path
from npc_trace_dataset import NpcTraceDataset


def demo_valid_loading():
    """Demonstrate loading valid trace data"""
    print("=" * 60)
    print("Demo 1: Loading valid trace data")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'test_data'
    file_path = test_data_dir / 'valid_trace_data.json'
    
    try:
        dataset = NpcTraceDataset.load(str(file_path))
        print(f"✓ Successfully loaded {len(dataset)} examples")
        print(f"  Dataset: {dataset}")
        
        print("\n  First example:")
        example = dataset[0]
        print(f"    State: {example['state']}")
        print(f"    Input: {example['input']}")
        print(f"    Expected output: {example['expected_output'][:50]}...")
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_strict_mode_error():
    """Demonstrate strict mode with missing fields"""
    print("\n" + "=" * 60)
    print("Demo 2: Strict mode with missing fields (raises KeyError)")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'test_data'
    file_path = test_data_dir / 'missing_state.json'
    
    try:
        dataset = NpcTraceDataset.load(str(file_path), strict=True)
        print(f"✓ Loaded {len(dataset)} examples")
    except KeyError as e:
        print(f"✓ Caught KeyError as expected: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


def demo_non_strict_mode():
    """Demonstrate non-strict mode with missing fields"""
    print("\n" + "=" * 60)
    print("Demo 3: Non-strict mode with missing fields (logs errors)")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'test_data'
    file_path = test_data_dir / 'multiple_missing_fields.json'
    
    try:
        dataset = NpcTraceDataset.load(str(file_path), strict=False)
        print(f"✓ Loaded {len(dataset)} valid examples")
        print(f"  Dataset: {dataset}")
        
        errors = dataset.get_validation_errors()
        if errors:
            print(f"\n  Validation errors encountered ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                print(f"    {i}. {error}")
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_file_not_found():
    """Demonstrate FileNotFoundError"""
    print("\n" + "=" * 60)
    print("Demo 4: Handling missing file")
    print("=" * 60)
    
    try:
        dataset = NpcTraceDataset.load('/nonexistent/path/data.json')
        print(f"✓ Loaded {len(dataset)} examples")
    except FileNotFoundError as e:
        print(f"✓ Caught FileNotFoundError as expected: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


def demo_invalid_json():
    """Demonstrate invalid JSON handling"""
    print("\n" + "=" * 60)
    print("Demo 5: Handling invalid JSON")
    print("=" * 60)
    
    test_data_dir = Path(__file__).parent / 'test_data'
    file_path = test_data_dir / 'invalid_json.json'
    
    try:
        dataset = NpcTraceDataset.load(str(file_path))
        print(f"✓ Loaded {len(dataset)} examples")
    except ValueError as e:
        print(f"✓ Caught ValueError as expected")
        print(f"  Error message: {str(e)[:80]}...")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == '__main__':
    print("\n" + "🎮 NpcTraceDataset Demo Script".center(60))
    print()
    
    demo_valid_loading()
    demo_strict_mode_error()
    demo_non_strict_mode()
    demo_file_not_found()
    demo_invalid_json()
    
    print("\n" + "=" * 60)
    print("Demo complete! All error handling working as expected.")
    print("=" * 60)
    print()
