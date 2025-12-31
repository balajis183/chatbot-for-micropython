# CodeBot — What this chatbot does ✅

**Short summary**

CodeBot (the script `codebot_test.py`) is a CLI chatbot that generates executable MicroPython code for ESP32 devices. It accepts a hardware-related user question, constructs a targeted system prompt (with rules for sensors, motors, etc.), sends the prompt to an LLM API, and prints the returned MicroPython code (no explanations or markdown).

---

## Features 🔧

- Generates only executable MicroPython code for ESP32 (no extra commentary).
- Adds specialized rules automatically for things like ADC (temperature), ultrasonic sensors, and motors.
- Sends user questions to a remote LLM API and returns the code response.
- Minimal CLI: type a question, get MicroPython code, or type `exit` to quit.

## How it works 🧭

1. User enters a question in the CLI.
2. `build_system_prompt()` inspects the question and appends device-specific rules to the base system prompt.
3. The script calls the LLM API (`API_URL`) with the assembled system prompt and the user's question.
4. The returned message content is cleaned and printed to the terminal.

## Quick usage example ▶️

- Run:

```bash
python codebot_test.py
```

- Example interactions:

```
Ask: How do I read a temperature sensor?
# → (prints MicroPython code using ADC on GPIO32)

Ask: How to get distance from ultrasonic sensor?
# → (prints MicroPython code with TRIG=GPIO33, ECHO=GPIO32, get_distance())
```

## Dependencies

- Python 3
- `requests` library (pip install requests)

## Security & privacy ⚠️

> **Important:** `codebot_test.py` currently contains a hard-coded `API_KEY`. Remove the key from the source and use environment variables (e.g., `os.environ`) or a secure secrets manager before sharing or committing the code.

Example change:

```python
API_KEY = os.getenv("CODEBOT_API_KEY")
```

## Notes & limitations ✳️

- The LLM model and the `API_URL` in the script are external services — behavior depends on that provider.
- The script enforces a strict system prompt that instructs the model to return *only* runnable MicroPython code — do not expect explanations.

---

If you want, I can:
- Add a short README section with instructions to store the API key in an `.env` file and load it with `python-dotenv`.
- Add a simple test script that validates sample prompts and checks returned code for syntax.

Let me know which you'd prefer and I’ll add it. ✨
