import requests
import json
import sys
import time
import os

username = "karu"

def prepare(server_origin, secret_b64):

    # --- Prepare the request ---
    url = f"{server_origin}/-/v0/do"

    headers = {
        "Authorization": f"Basic {secret_b64}",
        "Content-Type": "application/json"
    }
    return url, headers

def send_req(url, headers, payload):

    # --- Send the request ---
    try:
        # The `json` parameter automatically converts the dict to a JSON string
        print(url)
        print(headers)
        print(payload)
        response = requests.post(url, headers=headers, json=payload)

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        print("✅ Success!")
        print(f"Status Code: {response.status_code}")
        # Print the JSON response from the server
        print("Response JSON:", response.json())

    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")


def add_comment(server_origin, secret_b64, page_ref_id, comment_ref_id, body_contents):
    url, headers = prepare(server_origin, secret_b64)
    # The payload is a Python dictionary, which is easy to construct.
    payload = {
        "doActions": [{
            "asWho": f"username:{username}",
            "doWhat": "CreateComment",
            "doHow": {
                "refId": comment_ref_id,
                "parentNr": 1,
                "whatPage": page_ref_id,
                "bodySrc": body_contents, # Your multiline string is inserted here
                "bodyFmt": "CommonMark"
            }
        }]
    }
    send_req(url, headers, payload)

def add_page(server_origin, secret_b64, page_ref_id, cat_ref_id, title, body_content):

    url, headers = prepare(server_origin, secret_b64)

    # The payload is a Python dictionary, which is easy to construct.
    payload = {
        "doActions": [{
            "asWho": f"username:{username}",
            "doWhat": "CreatePage",
            "doHow": {
                "refId": page_ref_id,
                "pageType": "Discussion",
                "inCategory": cat_ref_id,
                "title": title,
                "bodySrc": body_content, # Your multiline string is inserted here
                "bodyFmt": "CommonMark"
            }
        }]
    }
    send_req(url, headers, payload)


def read_and_truncate_file(filepath, max_bytes=1950):
    """
    Reads the content of a file into a string and truncates it to a specified byte length.

    Args:
        filepath (str): The path to the file to read.
        max_bytes (int): The maximum number of bytes to keep in the string.

    Returns:
        str: The truncated content of the file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Encode the string to bytes to get its byte length and truncate
        encoded_content = content.encode('utf-8')
        if len(encoded_content) > max_bytes:
            truncated_bytes = encoded_content[:max_bytes]
            # Decode back to a string, handling potential incomplete multi-byte characters
            # 'ignore' will drop incomplete characters at the end
            truncated_string = truncated_bytes.decode('utf-8', errors='ignore')
        else:
            truncated_string = content
        
        return truncated_string

    except FileNotFoundError:
        return f"Error: File not found at {filepath}"
    except Exception as e:
        return f"An error occurred: {e}"


def add_paper(cat_ref_id, page_ref_id, dirname):

    # --- Configuration ---
    #server_origin = "https://________.talkyard.net"  # e.g., "https://example.com"
    #secret_b64 = "SECRET KEY HERE"

    title = read_and_truncate_file(os.path.join(dirname, 'title.txt'))
    acm_page_url = read_and_truncate_file(os.path.join(dirname, 'url.txt'))
    body_contents = read_and_truncate_file(os.path.join(dirname,'abstract.txt')) + f"[ACM DL Link]({acm_page_url})"
    add_page(server_origin, secret_b64, page_ref_id, cat_ref_id, title, body_contents)


    body_contents = read_and_truncate_file(os.path.join(dirname, 'review-1.txt'), 10000) 
    comment_ref_id = page_ref_id+"_review_1"
    print("Adding review 1")
    add_comment(server_origin, secret_b64, 'rid:'+page_ref_id, comment_ref_id, body_contents)
    time.sleep(10)

    body_contents = read_and_truncate_file(os.path.join(dirname, 'review-2.txt'), 10000) 
    comment_ref_id = page_ref_id+"_review_2"
    print("Adding review 2")
    add_comment(server_origin, secret_b64, 'rid:'+page_ref_id, comment_ref_id, body_contents)
    time.sleep(10)


    body_contents = read_and_truncate_file(os.path.join(dirname, 'review-3.txt'), 10000) 
    comment_ref_id = page_ref_id+"_review_3"
    print("Adding review 3")
    add_comment(server_origin, secret_b64, 'rid:'+page_ref_id, comment_ref_id, body_contents)
    time.sleep(10)



if __name__ == '__main__':


    # --- Configuration ---
    #server_origin = "https://________.talkyard.net"  # e.g., "https://example.com"
    #secret_b64 = "SECRET KEY HERE"
    
    cat_ref_id = "rid:category_questions"
    page_ref_id = sys.argv[1]
    dirname = sys.argv[2]
    add_paper(cat_ref_id, page_ref_id, dirname)
