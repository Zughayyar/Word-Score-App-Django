# word_score_app/tasks.py
from celery import shared_task
from resources.classes.word_scorer import WordScorer

@shared_task(bind=True)
def process_word_score(self, page_url, word):
    try:
        word_score_1 = WordScorer(page_url, word)
        all_pages = list(word_score_1.build_pages_set())  # Convert set to list for session storage
        total_occurrences = word_score_1.calculate_word_occurrences()

        return {
            'status': 'success',
            'total_occurrences': total_occurrences,
            'all_pages': all_pages
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}