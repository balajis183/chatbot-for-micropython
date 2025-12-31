import requests
import time

# ==============================
# CONFIGURATION (WORKING)
# ==============================

API_KEY = "9d06bc2c-7d40-42d4-9fac-8a1d3d3f9a54"
API_URL = "https://api.sambanova.ai/v1/chat/completions"
MODEL_NAME = "Llama-3.3-Swallow-70B-Instruct-v0.4"

# ==============================
# BASE SYSTEM PROMPT
# ==============================

BASE_SYSTEM_PROMPT = """
You generate ONLY executable MicroPython code for ESP32.
No explanations.
No markdown.
No triple backticks.
Use only valid MicroPython libraries.
Code must run directly on ESP32.
"""

# ==============================
# RULE BUILDER
# ==============================

def build_system_prompt(question: str) -> str:
    q = question.lower()
    rules = ""

    if "temperature" in q or "temp" in q or "analog" in q:
        rules += """
Use ADC on GPIO32.
Configure:
ADC.ATTN_11DB
ADC.WIDTH_12BIT
Read continuously in a loop.
"""

    if "ultrasonic" in q or "distance" in q:
        rules += """
Ultrasonic sensor rules:
TRIG = GPIO33
ECHO = GPIO32
Import:
from machine import Pin, time_pulse_us
import time
Use get_distance() function.
Send 10us trigger pulse.
Use time_pulse_us(echo, 1, 30000).
Distance = (duration * 0.034) / 2
"""

    if "motor" in q:
        rules += """
Motor rules:
Use Pin.OUT
Use PWM for speed
Never set both direction pins HIGH
"""

    return BASE_SYSTEM_PROMPT + rules

# ==============================
# API CALL
# ==============================

def generate_code(user_question):
    system_prompt = build_system_prompt(user_question)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        "temperature": 0.2,
        "max_tokens": 600
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    if response.status_code == 401:
        return "ERROR: Unauthorized – check API key"

    response.raise_for_status()

    code = response.json()["choices"][0]["message"]["content"]

    # Clean output (important for editor integration)
    code = code.replace("```python", "").replace("```", "").strip()

    return code

# ==============================
# MAIN LOOP
# ==============================

print("🔥 ESP32 MicroPython CodeBot Ready")
print("👉 Ask a hardware question")
print("👉 Type 'exit' to quit\n")

while True:
    question = input("Ask: ")

    if question.lower() == "exit":
        print("👋 Exiting CodeBot")
        break

    result = generate_code(question)
    print("\n" + result + "\n")

    time.sleep(0.5)
