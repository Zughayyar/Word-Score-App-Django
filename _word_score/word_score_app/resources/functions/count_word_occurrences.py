from resources.classes.page import Page
import re
from bs4 import BeautifulSoup

def count_word_occurrences(p: Page, word: str) -> int:
    """
    Counts the occurrences of a specific word in the content of the given Page.

    This function performs a case-insensitive count of the word, considering
    word boundaries to avoid counting parts of larger words.

    Args:
        p (Page): An instance of Page containing the HTML content to search.
        word (str): The word to count occurrences of.

    Returns:
        int: The number of times the word appears in the page content.

    Raises:
        ValueError: If the word provided is empty or None.
    """
    # Check if the word is valid
    if not word:
        raise ValueError("The word to search for cannot be empty or None.")

    # Extract text content by removing HTML tags using BeautifulSoup
    soup = BeautifulSoup(p.content, 'html.parser')
    text_content = soup.get_text(separator=' ', strip=True)  # Extract clean text
    
    # Convert the page content and the word to lowercase for case-insensitive matching
    text_content_lower = text_content.lower()
    word_lower = word.lower()

    # Use regex to find whole word occurrences, considering word boundaries
    pattern = r'\b' + re.escape(word_lower) + r'\b'

    # Count the occurrences using regex
    occurrences = len(re.findall(pattern, text_content_lower))

    return occurrences