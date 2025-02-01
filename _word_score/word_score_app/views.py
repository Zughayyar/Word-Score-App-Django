from django.shortcuts import render, redirect
from celery.result import AsyncResult
from .tasks import process_word_score
import json
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def word_score(request):
    if request.method == 'POST':
        page_url = request.POST['page_url']
        word = request.POST['word']

        # Start Celery Task
        task = process_word_score.delay(page_url, word)

        # Return Task ID to the frontend
        return JsonResponse({'task_id': task.id})
    
def task_status(request, task_id):
    result = AsyncResult(task_id)
    if result.state == 'SUCCESS':
        return JsonResponse(result.result)  # Return the result
    elif result.state == 'FAILURE':
        return JsonResponse({'status': 'error', 'message': str(result.result)})
    else:
        return JsonResponse({'status': 'pending'})