import google.generativeai as genai
import os

# --- Important: Configure your API Key ---
# It's best to use an environment variable.
# If you don't have one set, replace os.environ["GOOGLE_API_KEY"]
# with your actual API key string: "YOUR_API_KEY_HERE"
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Please set the GOOGLE_API_KEY environment variable or paste your key in the code.")
    exit()


print("--- Models Supporting 'generateContent' ---\n")

# The correct way to list models
for m in genai.list_models():
  # Check if the model supports the 'generateContent' method
  if 'generateContent' in m.supported_generation_methods:
    # m.name gives the full path, like 'models/gemini-1.5-pro-latest'
    # We can print just the part after 'models/'
    print(m.name.split('/')[-1])
