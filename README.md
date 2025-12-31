# CodeBot — Quick Start & Testing ✅

## Very short plain-language summary 🟢
CodeBot turns simple hardware questions into working MicroPython code you can run on an ESP32.

## Quick setup 🔧
1. Install Python 3.
2. Install dependencies:

```bash
pip install requests
```

3. Set your API key safely (do NOT keep it hard-coded). Example using an environment variable (Windows PowerShell):

```powershell
$env:CODEBOT_API_KEY = "YOUR_API_KEY_HERE"
```

Or use a `.env` file and load it with `python-dotenv` (optional):

```bash
pip install python-dotenv
```

Then in `codebot_test.py` replace the hard-coded key with:

```python
import os
API_KEY = os.getenv("CODEBOT_API_KEY")
```

## Run the program ▶️

```bash
python codebot_test.py
```

Type questions like:
```
Ask: How do I read a temperature sensor?
```
The script prints MicroPython code (no extra explanations).

## How to test 🔬

### Manual test (quick)
- Run `python codebot_test.py` and ask a sensor-related question such as "temperature" or "ultrasonic". Check the printed output contains sensible MicroPython code (e.g., ADC setup or TRIG/ECHO pins).

### Automated tests (unit tests)
A basic test file `test_codebot.py` is included that:
- Verifies rules are added to the system prompt
- Mocks the API and verifies unauthorized responses and output cleanup

Run the tests with:

```bash
python -m unittest test_codebot.py
```

