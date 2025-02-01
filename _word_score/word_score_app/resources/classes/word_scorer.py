from resources.functions.build_pages_set import build_pages_set
from resources.functions.word_total_occurencies import word_total_occurrences


# My application’s implementation: ### Anas Zughayyar ###

# WordScorer class is used to carry word and url information for each user input
from resources.functions.build_pages_set import build_pages_set
from resources.functions.word_total_occurencies import word_total_occurrences

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