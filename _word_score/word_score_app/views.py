from django.shortcuts import render, redirect
from celery.result import AsyncResult
from .tasks import word_score_task
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html', {'csrf_token': request.COOKIES['csrftoken']})

@csrf_exempt
def word_score_view(request):
    if request.method == "POST":
        page_url = request.POST.get("page_url")
        word = request.POST.get("word")
        
        if not page_url or not word:
            return JsonResponse({"error": "Missing parameters"}, status=400)
        
        try:
            task = word_score_task.delay(page_url, word)
            return JsonResponse({"task_id": task.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def task_status_view(request, task_id):
    task_result = AsyncResult(task_id)
    if task_result.state == 'PENDING':
        response = {"status": "pending"}
    elif task_result.state == 'SUCCESS':
        response = task_result.result
    else:
        response = {"status": "error", "message": str(task_result.info)}
    return JsonResponse(response)