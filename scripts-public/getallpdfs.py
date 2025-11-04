# read a main directory
# go through all its sub-directories
# if there is a file called pdf_link.txt in a sub-directory, read the contents of that file into a variable called pdfurl. call the function get_pdf(pdf_url)

import os
import shutil
import sys
import getpdf as getpdf
from urllib.parse import urlparse

def find_and_process_pdfs(main_directory, service, driver, download_dir):
    """
    Walks through a main directory and its sub-directories to find
    and process 'pdf_link.txt' files.

    Args:
        main_directory (str): The absolute or relative path to the main directory.
    """
    print(f"Starting scan in: '{main_directory}'...")

    # os.walk() recursively goes through every directory and file
    # For each directory, it yields the path, a list of sub-directories, and a list of files
    for dirpath, _, filenames in os.walk(main_directory):
        # Check if the target file exists in the current directory
        pdfexists = False
        for filename in filenames:
            if filename.endswith(".pdf"):
                pdfexists = True
                break
        if pdfexists == True:
            print(dirpath, "PDF exists")
            continue
        else:
            print(dirpath, "Need to download PDF")
        if 'pdf_link.txt' in filenames:
            file_path = os.path.join(dirpath, 'pdf_link.txt')
            print(f"\nFound 'pdf_link.txt' at: {file_path}")
            try:
                # Open the file and read its content
                with open(file_path, 'r') as f:
                    # .strip() removes any leading/trailing whitespace or newlines
                    pdfurl = f.read().strip()

                    # Call the function with the extracted URL
                    getpdf.get_pdf(driver, pdfurl, download_dir)
                    path = urlparse(pdfurl).path
                    filename = os.path.basename(path)+".pdf"
                    shutil.copy2(os.path.join(download_dir,filename), os.path.join(dirpath,filename))
                    os.remove(os.path.join(download_dir,filename))

            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    print("\nScan complete.")

download_dir = sys.argv[1]
papers_dir = sys.argv[2]
if not os.listdir(download_dir):
    print(f"✅ The directory '{download_dir}' is empty.")
else:
    print(f"❌ The directory '{download_dir}' is not empty.")
    quit()

service, driver = getpdf.setup_chrome(download_dir)
find_and_process_pdfs(papers_dir, service, driver, download_dir)
getpdf.close_browser(driver)

