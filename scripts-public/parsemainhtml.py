from bs4 import BeautifulSoup
import csv
import sys

def parse_acm_html(file_path):
    """
    Parses an HTML file from the ACM Digital Library to extract paper details.

    Args:
        file_path (str): The path to the HTML file to parse.

    Returns:
        list: A list of dictionaries, where each dictionary contains the
              details of a single paper (URL, title, abstract, PDF link).
    """
    papers = []
    # Base URL to prepend to relative links if necessary
    base_url = "https://dl.acm.org"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the main containers for each paper listing
        issue_items = soup.find_all('div', class_='issue-item clearfix')

        if not issue_items:
            print("Warning: No elements with class 'issue-item clearfix' found.")
            return []

        for item in issue_items:
            paper_data = {
                'paper-URL': None,
                'paper-title': None,
                'paper-truncated-abstract': None,
                'paper-pdf-link': None
            }

            # a) Find the title and link
            title_tag = item.find('h3', class_='issue-item__title')
            if title_tag and title_tag.a:
                # Ensure the URL is absolute
                href = title_tag.a.get('href', '')
                paper_data['paper-URL'] = f"{base_url}{href}" if href.startswith('/') else href
                paper_data['paper-title'] = title_tag.a.get_text(strip=True)

            # b) Find the abstract
            # The class name in the file is slightly different
            abstract_tag = item.find('div', class_='issue-item__abstract')
            if abstract_tag:
                 paper_data['paper-truncated-abstract'] = abstract_tag.get_text(strip=True)


            # c) Find the PDF link
            pdf_tag = item.find('a', attrs={"aria-label": "PDF", "data-title": "PDF"})
            if pdf_tag:
                href = pdf_tag.get('href', '')
                paper_data['paper-pdf-link'] = f"{base_url}{href}" if href.startswith('/') else href

            papers.append(paper_data)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return papers

def save_to_csv(data, filename="papers.csv"):
    """
    Saves the extracted paper data to a CSV file.

    Args:
        data (list): A list of paper data dictionaries.
        filename (str): The name of the CSV file to create.
    """
    if not data:
        print("No data to save.")
        return

    # The headers are the keys of the first dictionary
    headers = data[0].keys()

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Successfully saved data to {filename}")
    except Exception as e:
        print(f"Failed to save CSV file: {e}")


if __name__ == '__main__':
    # The name of the file you uploaded
    html_file = sys.argv[1]
    
    extracted_papers = parse_acm_html(html_file)

    if extracted_papers:
        # Print the results to the console for a quick view
        for i, paper in enumerate(extracted_papers, 1):
            print(f"--- Paper {i} ---")
            print(f"Title: {paper.get('paper-title')}")
            print(f"URL: {paper.get('paper-URL')}")
            print(f"Abstract: {paper.get('paper-truncated-abstract')}")
            print(f"PDF Link: {paper.get('paper-pdf-link')}\n")
        
        # Save the extracted data to a CSV file
        save_to_csv(extracted_papers, "extracted_papers.csv")

