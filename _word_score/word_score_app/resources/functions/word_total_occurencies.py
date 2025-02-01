import concurrent.futures
import logging
from resources.functions.build_pages_set import build_pages_set
from resources.functions.count_word_occurrences import count_word_occurrences

def word_total_occurrences(start_url: str, word: str, depth: int = 1) -> int:
    """
    Calculate the total occurrences of a specific word across pages starting from a given URL.

    Args:
        start_url (str): The URL to start the search from.
        word (str): The word to count occurrences of.
        depth (int, optional): The depth of links to follow. Defaults to 2.

    Returns:
        int: The total number of occurrences of the word in all visited pages.

    Raises:
        Various exceptions if there are issues with downloading pages or counting words.
    """
    try:
        # Build the set of pages to visit
        pages = build_pages_set(start_url, depth)
        logging.info(f"Found {len(pages)} pages to visit.")

        total_occurrences = 0

        # Use ThreadPoolExecutor to count word occurrences across pages concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(count_word_occurrences, page, word) for page in pages]

            # Process the results as the threads complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    total_occurrences += future.result()
                except Exception as e:
                    logging.error(f"Error in counting word occurrences: {e}")

        logging.info(f"Total occurrences of the word '{word}': {total_occurrences}")
        return total_occurrences

    except Exception as e:
        logging.error(f"Error in word_total_occurrences: {e}")
        raise  # Re-raise the exception after logging it