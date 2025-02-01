from queue import Queue
from typing import Set
from resources.classes.page import Page
from resources.functions.download_page import download_page
from resources.functions.get_links_in_page import get_links_in_page
import logging
from urllib.parse import urlparse, urljoin

def build_pages_set(start_url: str, depth: int = 2, max_pages: int = 100) -> Set[Page]:
    """
    This function performs a breadth-first search (BFS) starting from a URL to gather all reachable pages
    up to a specified depth. It returns a set of `Page` objects for each page visited.

    Args:
        start_url (str): The URL to start the crawling process from.
        depth (int): The depth to which the crawling should go (default is 2).
        max_pages (int): Maximum number of pages to be crawled (default is 100).

    Returns:
        Set[Page]: A set of `Page` objects containing the crawled pages.
    """
    visited = set()  # Track visited URLs to avoid redundant processing
    queue = Queue()  # Queue for breadth-first traversal
    queue.put((start_url, 0))  # Tuple with URL and current depth
    pages = set()

    while not queue.empty() and len(pages) < max_pages:
        url, current_depth = queue.get()

        # Skip if URL is already visited or exceeds depth limit
        if url in visited or current_depth > depth:
            continue
        
        # Check if the URL is a valid HTTP/HTTPS URL
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            logging.warning(f"Skipping unsupported URL scheme: {parsed_url.scheme} for {url}")
            continue

        try:
            # Download the page and create a Page object
            page = download_page(url)
        except Exception as e:
            logging.error(f"Failed to download {url}: {e}")
            continue

        visited.add(url)
        pages.add(page)

        if current_depth < depth:
            links = get_links_in_page(page)  # Extract links from the page
            for link in links:
                # Normalize relative links to absolute URLs
                absolute_link = urljoin(url, link)
                parsed_link = urlparse(absolute_link)

                # Ensure the link is valid and hasn't been visited before
                if parsed_link.scheme in ('http', 'https') and absolute_link not in visited:
                    queue.put((absolute_link, current_depth + 1))

    logging.info(f"Crawling finished: {len(pages)} pages visited.")
    return pages