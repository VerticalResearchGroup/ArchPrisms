# First, install the library if you haven't already
# pip install google-generativeai

import google.generativeai as genai
import os

# --- Configuration ---
# It's a best practice to store your API key in an environment variable.
# If your institutional access uses a different method (like ADC),
# you might not need this explicit configuration.
# To set an environment variable:
# In Linux/macOS: export GOOGLE_API_KEY="YOUR_API_KEY"
# In Windows CMD: set GOOGLE_API_KEY="YOUR_API_KEY"
# In PowerShell: $env:GOOGLE_API_KEY="YOUR_API_KEY"

try:
    # Attempt to configure using an environment variable
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    # If the environment variable is not set, you can manually insert your key.
    # However, avoid hardcoding keys in production code.
    print('key didn not work')
    api_key = "YOUR_API_KEY_HERE"
    genai.configure(api_key=api_key)


# --- Model Initialization ---
# For text-only prompts, use 'gemini-pro'
model = genai.GenerativeModel('gemini-1.5-flash-latest')


# --- Prompt and Generation ---
# Create your prompt
prompt = "As a UW-Madison student, what are three must-do activities on campus?"

# Send the prompt to the model
response = model.generate_content(prompt)


# --- Output ---
# Print the generated text
print("--- Gemini Pro Response ---")
print(response.text)
