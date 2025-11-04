import requests
from bs4 import BeautifulSoup

def get_abstract_text(url):
    """
    Fetches a URL and extracts the text content from the <section id="abstract"> element.

    Args:
        url: The URL of the webpage to scrape.

    Returns:
        The text content of the abstract section, or None if the section
        isn't found or an error occurs.
    """
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful (status code 200)
        response.raise_for_status() 

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <section> element with the id "abstract"
        abstract_section = soup.find('section', id='abstract')

        # Check if the element was found
        if abstract_section:
            # Return the inner text content of the element
            return abstract_section.get_text(strip=True)
        else:
            # Return None if the section with id="abstract" was not found
            print(f"Warning: <section id=\"abstract\"> not found at {url}")
            return None

    except requests.exceptions.RequestException as e:
        # Handle exceptions for the web request (e.g., connection error, timeout)
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        # Handle other potential errors (e.g., parsing errors)
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example Usage:
    # Note: This example URL is a placeholder and may not work.
    # You will need to provide a URL that actually has a <section id="abstract">.
    
    # A simple HTML string for demonstration purposes
    import sys
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
        print(f"Attempting to fetch abstract from: {test_url}\n")
        abstract = get_abstract_text(test_url)
        if abstract:
            print("--- Abstract Found ---")
            print(abstract)
            print("------------------------")
        else:
            print("Could not retrieve the abstract.")
    else:
        print("--- Running a self-test with mock HTML ---")
        # To run a simple test without a live URL, we can mock the request
        # This part is just for showing the function works.
        try:
            import responses # This requires `pip install responses`
            
            mock_url = "http://example.com/article"
            mock_html = """
            <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>An Article</h1>
                <section id="intro">
                    <p>This is the introduction.</p>
                </section>
                <section id="abstract">
                    <h2>Abstract</h2>
                    <p>This is the abstract text we want to extract.</p>
                    <p>It has multiple paragraphs.</p>
                </section>
                <section id="conclusion">
                    <p>This is the conclusion.</p>
                </section>
            </body>
            </html>
            """
            
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, mock_url,
                         body=mock_html, status=200,
                         content_type='text/html')
                
                print(f"Fetching mock abstract from: {mock_url}\n")
                abstract = get_abstract_text(mock_url)
                if abstract:
                    print("--- Abstract Found ---")
                    print(abstract)
                    print("------------------------")
                else:
                    print("Could not retrieve the abstract.")

        except ImportError:
            print("\n(To run the example usage, you would need a real URL")
            print("or install the 'responses' library for mocking: pip install responses)")
            print("Usage: python extract_abstract.py <your-url>")

