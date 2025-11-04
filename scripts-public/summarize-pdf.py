import sys
import google.generativeai as genai
import os

def read_prompt(prompt_file):
    try:
       with open(prompt_file, 'r', encoding='utf-8') as file:
          file_content = file.read()
       return(file_content)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    quit()
# --- Configuration ---
# Configure your API key. It's best practice to use an environment variable.
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

# PASTE THE SAVED NAME from the first program here
SAVED_FILE_NAME = sys.argv[1] # <--- Replace with your actual file name

# 1. Retrieve the file reference using its unique name
print(f"Retrieving file: {SAVED_FILE_NAME}")
existing_file = genai.get_file(name=SAVED_FILE_NAME)


# 2. Use the file in a new prompt
print("File retrieved. Asking a new question...")

# --- 2. Initialize the Model ---
# You must use a Gemini 1.5 model that supports file inputs.
#model = genai.GenerativeModel('gemini-1.5-flash-latest')
model = genai.GenerativeModel('gemini-2.5-pro')

# --- 3. Generate Content ---
# Create the prompt. You must include the uploaded file object.
#prompt = "Please provide a concise, one-paragraph summary of this document."
prompt = read_prompt(sys.argv[2])

print("\nApplying prompt...", prompt)
# Pass both the text prompt and the file to the model.
response = model.generate_content([existing_file, prompt])

# --- 4. Print the Response ---
print("\n--- Summary ---")
print(response.text)
print("---------------")

for i in [3, 4, 5]:
   prompt = read_prompt(sys.argv[i])
   response = model.generate_content([existing_file, prompt])
   # --- 5. Print the Response ---
   print("\n--- Summary ---")
   print(response.text)
   print("---------------")
