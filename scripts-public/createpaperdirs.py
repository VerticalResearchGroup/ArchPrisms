import parsemainhtml as p
import sys
import os

html_file = sys.argv[1]
extracted_papers = p.parse_acm_html(html_file)


# Define the top-level directory where all paper folders will be stored.
topdir = sys.argv[2]

# Create the top-level directory if it doesn't already exist.
# The 'exist_ok=True' argument prevents an error if the directory is already there.
os.makedirs(topdir, exist_ok=True)
print(f"Top-level directory '{topdir}' is ready.")

# Loop through each paper in the list with its index.
for i, paper in enumerate(extracted_papers):

    # 1. Get the data for the current paper.
    # Using .get() is a good practice as it returns None if a key is missing,
    # preventing errors. We'll provide a default empty string '' just in case.
    title = paper.get('paper-title', '')
    url = paper.get('paper-URL', '')
    abstract = paper.get('paper-truncated-abstract', '')
    pdf_link = paper.get('paper-pdf-link', '')
    if pdf_link == None:
        print("Skipping....", i)
        continue
    # 2. Create a specific directory for the current paper.
    paper_dir = os.path.join(topdir, f"paper-{i}")
    os.makedirs(paper_dir, exist_ok=True)
    print(f"\nCreated directory: {paper_dir}")
    # 3. Define the file paths and write the content to each file.
    file_mappings = {
        "title.txt": title,
        "url.txt": url,
        "abstract.txt": abstract,
        "pdf_link.txt": pdf_link
    }

    for filename, content in file_mappings.items():
        file_path = os.path.join(paper_dir, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  - Wrote {filename}")
        except IOError as e:
            print(f"  - Error writing to {filename}: {e}")

print("\nProcessing complete.")
