#!/bin/bash

# Loop over all directories starting with "paper-" in the current location
for dir in paper-*/; do
    
    # Check if 'dir' is actually a directory
    if [ -d "$dir" ]; then
        
        # Use 'find' to search for any file ending in .pdf (case-insensitive)
        # -maxdepth 1 limits the search to only the directory itself, not subdirectories
        # We pipe to 'grep' to see if any results are returned.
        # 'read' will set $found_pdf if grep finds anything
        found_pdf=$(find "$dir" -maxdepth 1 -type f -iname "*.pdf" | grep . -c)

        # Check if the count of found PDF files is 0
        if [ "$found_pdf" -eq 0 ]; then
            # No PDF files were found.
            # Now, check if 'url.txt' exists and is readable in this directory
            if [ -f "${dir}url.txt" ] && [ -r "${dir}url.txt" ]; then
                # echo "--- Contents of ${dir}url.txt ---"
                echo -n "${dir} "
                cat "${dir}url.txt"
                echo -n " " 
                cat "${dir}title.txt"
                echo " -----------------------------------"
            else
                echo "--- No PDF in $dir, but url.txt is missing or unreadable ---"
            fi
        # else
            # A PDF was found, so we skip this directory.
            # echo "Skipping $dir (contains PDF)"
        fi
    fi
done

echo "Script finished."
