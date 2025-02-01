import requests
from resources.classes.page import Page
from urllib.parse import urlparse
import time
import logging

def download_page(url: str) -> Page:
    """
    Downloads the content of a web page given its URL and returns a Page object.

    This function simulates fetching a web page via HTTP request and constructs
    a Page object with the content and URL. It handles network-related errors,
    implements retries, and checks for valid HTTP(S) URLs.

    Args:
        url (str): The URL of the web page to download.

    Returns:
        Page: An instance of Page containing the HTML content and the URL.

    Raises:
        requests.RequestException: If there's an error during the HTTP request.
        ValueError: If the response status code is not 200 (OK) or if the URL scheme is not http/https.
    """
    # Parse the URL to check the scheme
    parsed_url = urlparse(url)
    
    # Check if the URL scheme is HTTP or HTTPS
    if parsed_url.scheme not in ('http', 'https'):
        raise ValueError(f"Unsupported URL scheme: {parsed_url.scheme}. Only HTTP and HTTPS are supported.")
    
    # Handle potential mailto links or other unsupported URL schemes
    if parsed_url.scheme == 'mailto':
        raise ValueError(f"Unsupported URL scheme: {parsed_url.scheme}. Mailto links are not supported.")
    
    # Set up the headers with a User-Agent to avoid being blocked by simple anti-bot protections
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Retry logic
    retries = 3
    for attempt in range(retries):
        try:
            # Send a GET request to the provided URL with a timeout of 10 seconds
            response = requests.get(url, timeout=10, headers=headers, verify=False)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Create and return a Page object with the content and URL
                return Page(content=response.text, url=url)
            else:
                raise ValueError(f"Failed to download page. Status code: {response.status_code}")
        
        except requests.Timeout:
            # Handle timeouts specifically and retry if the connection times out
            logging.warning(f"Timeout occurred while trying to download {url}. Retrying ({attempt + 1}/{retries})...")
            if attempt < retries - 1:
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                raise requests.RequestException(f"Max retries reached for {url} due to timeout.")
        
        except requests.RequestException as e:
            # Catch other request-related exceptions (e.g., connection issues)
            logging.error(f"An error occurred while downloading {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                raise requests.RequestException(f"An error occurred while downloading {url} after {retries} retries: {e}")