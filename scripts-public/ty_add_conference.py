import os
import sys
import ty_add_page as ty_add_page

def local_add_paper(paper_id, paper_path):
    """
    Placeholder function to process a paper.
    
    Args:
        paper_id (str): A unique identifier for the paper (dir_name + "_" + subdir_name).
        paper_path (str): The full absolute path to the paper's directory.
    """
   # In a real application, you would add your paper processing logic here.
    # For example:
    # database.add_entry(paper_id, paper_path)
    # results = analyze_reviews(paper_path)
    print(f"Processing paper with ID: {paper_id}")
    print(f"Found review files in: {paper_path}")
    print("-" * 30)
    # summary.save(paper_id, results)
    pass

def find_review_dirs(root_directory, category):
    """
    Searches for subdirectories named 'paper_<number>' containing specific 
    review files (review-1.txt, review-2.txt, review-3.txt) and calls 
    add_paper if found. Processes subdirectories in numerical order.

    Args:
        root_directory (str): The path to the main directory to start searching from.
    """
    
    # Ensure the root directory exists
    if not os.path.isdir(root_directory):
        print(f"Error: Directory not found at {root_directory}")
        return

    # Get the name of the root directory itself for constructing the ID
    root_dir_name = os.path.basename(os.path.normpath(root_directory))

    try:
        paper_dirs = []
        # First, scan all entries and collect valid paper directories
        for entry in os.scandir(root_directory):
            # Check if it's a directory and starts with "paper_"
            if entry.is_dir() and entry.name.startswith("paper-"):
                try:
                    # Extract the number part after "paper_"
                    number_str = entry.name[len("paper-"):]
                    paper_number = int(number_str)
                    # Store the number, path, and name for sorting
                    paper_dirs.append((paper_number, entry.path, entry.name))
                except ValueError:
                    # The part after "paper_" was not a number, skip it
                    print(f"Skipping directory (non-numeric name): {entry.name}")
                    pass
        
        # Sort the list based on the paper number (the first element of the tuple)
        paper_dirs.sort(key=lambda x: x[0])
        
        # Now, iterate through the sorted list and process the directories
        for paper_number, subdir_path, subdir_name in paper_dirs:
            
            # Define the paths for the three required files
            file1 = os.path.join(subdir_path, "review-1.txt")
            file2 = os.path.join(subdir_path, "review-2.txt")
            file3 = os.path.join(subdir_path, "review-3.txt")
            
            # Check if all three files exist
            if (os.path.exists(file1) and 
                os.path.exists(file2) and 
                os.path.exists(file3)):
                
                # All files exist, construct the arguments and call add_paper
                
                # 1. First argument: directory name + "_" + subdirectory name
                paper_id = f"01_{root_dir_name}_{subdir_name}"
                
                # 2. Second argument: full path of the subdirectory
                # os.path.abspath ensures it's the full path
                full_subdir_path = os.path.abspath(subdir_path)
                
                # Call the subroutine
                print(full_subdir_path)
                ty_add_page.add_paper(category, paper_id, full_subdir_path)
            else:
                # Optional: Log which sorted papers are skipped due to missing files
                print(f"Skipping directory (missing files): {subdir_name}")


    except OSError as e:
        print(f"Error scanning directory {root_directory}: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    d = sys.argv[1]
    category = sys.argv[2]
    find_review_dirs(d, category)
