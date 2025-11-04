import sys
import google.generativeai as genai
import os

def read_prompt(prompt_file):
    try:
       with open(file_path, 'r', encoding='utf-8') as file:
          file_content = file.read()
       print(file_content)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Configuration ---
# Configure your API key. It's best practice to use an environment variable.
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

# --- 1. Upload the File ---
# Provide the path to your local PDF file.
# Make sure this file exists in the same directory as your script,
# or provide the full path to it.
file_path = sys.argv[1]

print(f"Uploading file: {file_path}...")
# The File API uploads the file and makes it available for the model.
uploaded_file = genai.upload_file(path=file_path, display_name="Sample Document")
print(f"Completed upload: {uploaded_file.uri}")

# CRITICAL STEP: Get and save the unique file name
file_name = uploaded_file.name
print(f"File uploaded successfully!")
print("SAVE THIS NAME for future use:")
print(f"{sys.argv[1]} -> {file_name}")

