import sys
import google.generativeai as genai
import os
import time

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



def review_paper(filename, outdir, orig_prompts, realrun = 0):
    # PASTE THE SAVED NAME from the first program here
    SAVED_FILE_NAME = filename

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
    prompts = list(orig_prompts)
    prompt = read_prompt(prompts[0])
    prompts.pop(0)
    print("\nApplying prompt...", prompt)
    # Pass both the text prompt and the file to the model.
    if realrun == 1:
        response = model.generate_content([existing_file, prompt])

        # --- 4. Print the Response ---
        print("\n--- Summary ---")
        print(response.text)
        print("---------------")

    for i, prompt_file in enumerate(prompts):
       prompt = read_prompt(prompt_file)
       txt = 'empty'
       if realrun == 1:
           response = model.generate_content([existing_file, prompt])
           txt = response.text
           # --- 5. Print the Response ---
           print("\n--- Summary ---")
           print(response.text)
           print("---------------")
       else:
           txt = 'some response'
       j=i+1
       filename = f'review-{j}.txt'
       filename = os.path.join(outdir, filename)
       with open(filename, 'w') as file:
            file.write(txt)
       print("Write to -> ", filename)

def process_file(filename):
    """
    Reads a file line by line, parses it, and extracts the directory name.
    
    Args:
        filename (str): The name of the file to process.
    """
    list_of_files = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Strip leading/trailing whitespace and split the line by comma
                fields = line.strip().split(',')
                entry = dict()
                # Ensure there are at least two fields to avoid errors
                if len(fields) >= 1:
                    first_field = fields[0]
                    
                    # Extract the directory name using os.path.dirname
                    directory_name = os.path.dirname(first_field)
                    entry['dirname'] = directory_name
                    entry['fileptr'] = fields[1]
                    list_of_files.append(entry)
#                    print(f"Directory: {directory_name}")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return list_of_files

def setup_key():
    # --- Configuration ---
    # Configure your API key. It's best practice to use an environment variable.
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        exit()

def upload_file(file_path):
    print(f"Uploading file: {file_path}...")
    # The File API uploads the file and makes it available for the model.
    uploaded_file = genai.upload_file(path=file_path, display_name=file_path)
    print(f"Completed upload: {uploaded_file.uri}")


    # CRITICAL STEP: Get and save the unique file name
    file_name = uploaded_file.name
    return file_name


if __name__ == "__main__":
    prompts_dir = sys.argv[1]
    prompts = [ os.path.join(prompts_dir, 'prompt-setup.txt'),os.path.join(prompts_dir, 'prompt1.txt'),os.path.join(prompts_dir, 'prompt2.txt'),os.path.join(prompts_dir, 'prompt3.txt') ]
    papers_dir = sys.argv[2]
    print(prompts)

    for dirpath, _, filenames in os.walk(papers_dir):
        # Check if the target file exists in the current directory
        pdfexists = False
        pdf_filename = ''
        for filename in filenames:
            if filename.endswith(".pdf"):
                pdfexists = True
                pdf_filename=os.path.join(dirpath, filename)
                break
        if pdfexists == False:
            print(dirpath, "PDF does not exist")
            continue
        if os.path.exists( os.path.join(dirpath, 'review-3.txt')):
            r1 = os.path.join(dirpath, 'review-1.txt')
            r2 = os.path.join(dirpath, 'review-2.txt')
            r3 = os.path.join(dirpath, 'review-3.txt')
            print("Reviews already exist...", dirpath, os.path.getsize(r1), os.path.getsize(r2), os.path.getsize(r3) )
            continue
        print("Reviewing PDF ", pdf_filename)
        print("Title ", read_prompt(os.path.join(dirpath, 'title.txt')))
        cloud_file_name = upload_file(pdf_filename)
        review_paper(cloud_file_name, dirpath, prompts, 1)
        print("Sleeping...")
        time.sleep(10)
