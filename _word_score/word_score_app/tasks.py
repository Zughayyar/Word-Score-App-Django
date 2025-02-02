from celery import shared_task
from queue import Queue
from typing import Set
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup
import requests
import time
import logging
import concurrent.futures

# Page Class to carry the page attributes for reusability
class Page:
    """A simple Page class to represent the downloaded HTML page."""
    def __init__(self, content: str, url: str):
        self.content = content
        self.url = url

    def get_content(self) -> str:
        return self.content

    def get_url(self) -> str:
        return self.url

# WordScorer class is used to carry word and url information for each user input
class WordScorer:
    def __init__(self, page_url: str, word: str):
        self.page_url = page_url
        self.word = word
        self.pages_set = None
        self._word_occurrences = 0  # Use a private variable to avoid confusion

    def build_pages_set(self):
        if self.pages_set is None:
            self.pages_set = build_pages_set(self.page_url)
        return self.pages_set

    def calculate_word_occurrences(self):
        if self._word_occurrences == 0:
            self._word_occurrences = word_total_occurrences(self.page_url, self.word)
        return self._word_occurrences  # Return the count if already calculated

def get_links_in_page(p: Page) -> Set[str]:
    """
    Extracts all the links from the given Page object's content.
    """
    try:
        soup = BeautifulSoup(p.content, 'html.parser')
        links = soup.find_all('a', href=True)
        extracted_links = set()
        for link in links:
            absolute_link = urljoin(p.url, link['href'])
            if absolute_link and absolute_link.startswith(('http', 'https')):
                extracted_links.add(absolute_link)

        logging.info(f"Extracted {len(extracted_links)} links from {p.url}")
        return extracted_links

    except ImportError:
        raise ImportError("BeautifulSoup is required for parsing HTML. Please install bs4: uv add bs4")
    except Exception as e:
        logging.error(f"Error occurred while extracting links from {p.url}: {e}")
        raise Exception(f"An error occurred while extracting links from {p.url}.")

def build_pages_set(start_url: str, depth: int = 2, max_pages: int = 100) -> Set[Page]:
    """
    Performs a breadth-first search (BFS) starting from a URL to gather all reachable pages.
    """
    visited = set()
    queue = Queue()
    queue.put((start_url, 0))
    pages = set()

    while not queue.empty() and len(pages) < max_pages:
        url, current_depth = queue.get()

        if url in visited or current_depth > depth:
            continue

        parsed_url = urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            logging.warning(f"Skipping unsupported URL scheme: {parsed_url.scheme} for {url}")
            continue

        try:
            page = download_page(url)
        except Exception as e:
            logging.error(f"Failed to download {url}: {e}")
            continue

        visited.add(url)
        pages.add(page)

        if current_depth < depth:
            links = get_links_in_page(page)
            for link in links:
                absolute_link = urljoin(url, link)
                parsed_link = urlparse(absolute_link)
                if parsed_link.scheme in ('http', 'https') and absolute_link not in visited:
                    queue.put((absolute_link, current_depth + 1))

    logging.info(f"Crawling finished: {len(pages)} pages visited.")
    return pages

def count_word_occurrences(p: Page, word: str) -> int:
    """
    Counts the occurrences of a specific word in the content of the given Page.
    """
    if not word:
        raise ValueError("The word to search for cannot be empty or None.")

    soup = BeautifulSoup(p.content, 'html.parser')
    text_content = soup.get_text(separator=' ', strip=True)
    text_content_lower = text_content.lower()
    word_lower = word.lower()
    pattern = r'\b' + re.escape(word_lower) + r'\b'
    occurrences = len(re.findall(pattern, text_content_lower))

    return occurrences

def word_total_occurrences(start_url: str, word: str, depth: int = 1) -> int:
    """
    Calculate the total occurrences of a specific word across pages starting from a given URL.
    """
    try:
        pages = build_pages_set(start_url, depth)
        logging.info(f"Found {len(pages)} pages to visit.")

        total_occurrences = 0

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(count_word_occurrences, page, word) for page in pages]

            for future in concurrent.futures.as_completed(futures):
                try:
                    total_occurrences += future.result()
                except Exception as e:
                    logging.error(f"Error in counting word occurrences: {e}")

        logging.info(f"Total occurrences of the word '{word}': {total_occurrences}")
        return total_occurrences

    except Exception as e:
        logging.error(f"Error in word_total_occurrences: {e}")
        raise

def download_page(url: str) -> Page:
    """
    Downloads the content of a web page given its URL and returns a Page object.
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ('http', 'https'):
        raise ValueError(f"Unsupported URL scheme: {parsed_url.scheme}. Only HTTP and HTTPS are supported.")

    if parsed_url.scheme == 'mailto':
        raise ValueError(f"Unsupported URL scheme: {parsed_url.scheme}. Mailto links are not supported.")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10, headers=headers, verify=True)
            if response.status_code == 200:
                return Page(content=response.text, url=url)
            else:
                raise ValueError(f"Failed to download page. Status code: {response.status_code}")

        except requests.Timeout:
            logging.warning(f"Timeout occurred while trying to download {url}. Retrying ({attempt + 1}/{retries})...")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise requests.RequestException(f"Max retries reached for {url} due to timeout.")

        except requests.RequestException as e:
            logging.error(f"An error occurred while downloading {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise requests.RequestException(f"An error occurred while downloading {url} after {retries} retries: {e}")


@shared_task
def word_score_task(page_url, word):
    try:
        word_score_1 = WordScorer(page_url, word)
        all_pages = [page.get_url() for page in word_score_1.build_pages_set()] # Extract URLs
        total_occurrences = word_score_1.calculate_word_occurrences()

        return {
            'status': 'success',
            'total_occurrences': total_occurrences,
            'all_pages': all_pages
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}