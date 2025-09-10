# A.R.I.S.E. Backend Tests

This folder contains all test files for the A.R.I.S.E. AI backend modules.

## Running Tests

### Individual Test Files
```bash
# Run application scanner test
python tests/test_app_scanner.py

# Run from backend directory
cd backend
python tests/test_app_scanner.py
```

### Using pytest (recommended)
```bash
# Install pytest first
pip install pytest

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_app_scanner.py -v
```

## Test Files

- `test_app_scanner.py` - Tests for the application scanner module
- `__init__.py` - Makes this directory a Python package

## Adding New Tests

When adding new modules to the backend, create corresponding test files here:

1. Name test files with `test_` prefix (e.g., `test_speech_recognition.py`)
2. Import modules using the correct path:
   ```python
   import sys
   import os
   sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   from modules.your_module import YourClass
   ```
3. Follow the existing test structure and patterns

## Cleanup

After project completion, you can safely delete this entire `tests/` folder to remove all test files from your production deployment.

```bash
# Remove all test files
rm -rf tests/
```

## Test Coverage

The tests verify:
- ✅ Application detection functionality
- ✅ Popular applications scanning
- ✅ Windows built-in applications
- ✅ Microsoft Office detection
- ✅ Application launching capabilities
- ✅ JSON export/import functionality
