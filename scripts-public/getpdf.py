import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sys

def setup_chrome(download_dir):

   # Define the download directory
   if not os.path.exists(download_dir):
      os.makedirs(download_dir)

   # Configure ChromeOptions for downloading PDFs
   chrome_options = webdriver.ChromeOptions()
   prefs = {
     "plugins.plugins_disabled": ["Chrome PDF Viewer"],  # Disable built-in PDF viewer
     "plugins.always_open_pdf_externally": True,  # Always download PDFs instead of opening
     "download.default_directory": download_dir,  # Set the download directory
   }
   chrome_options.add_experimental_option("prefs", prefs)
   chrome_options.add_argument("--remote-allow-origins=*") # Required for some environments

   # Initialize the WebDriver
   service = Service(ChromeDriverManager().install())
   driver = webdriver.Chrome(service=service, options=chrome_options)
   return service, driver

def get_pdf(driver, pdfurl, download_dir):

   try:
      # Navigate to a webpage containing a PDF link
      print(pdfurl)
      driver.get(pdfurl) # Example PDF URL


      # In this specific example, the URL directly points to a PDF, so it will download automatically.
      # If the PDF is linked from a page, you would find and click the link:
      #  pdf_link = driver.find_element(By.LINK_TEXT, "Download PDF") # Or By.XPATH, By.ID etc.
      # pdf_link.click()

      #  Wait for the download to complete (adjust time as needed)
      time.sleep(30)

      # Verify the file download (optional)
      downloaded_files = os.listdir(download_dir)
      if any(".pdf" in f for f in downloaded_files):
         print("PDF downloaded successfully!")
      else:
         print("PDF download failed.")
   finally:
      pass

def close_browser(driver):
   # Close the browser
   driver.quit()

if __name__ == '__main__':
   service, driver = setup_chrome(sys.argv[1])
   get_pdf(driver, sys.argv[2], sys.argv[1])
   get_pdf(driver, sys.argv[3], sys.argv[1])
   close_browser(driver)
