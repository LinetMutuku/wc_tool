import os

from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def word_count(file_path, keyword=''):
    lines = 0
    words = 0
    bytes_count = 0
    keyword_count = 0

    try:
        with open(file_path, 'rb') as file:
            for line in file:
                lines += 1
                words += len(line.split())
                bytes_count += len(line)
                if keyword and keyword in line.decode('utf-8', 'ignore'):
                    keyword_count += 1
    except FileNotFoundError:
        return lines, words, bytes_count, keyword_count

    return lines, words, bytes_count, keyword_count


@csrf_exempt
def wc_view(request):
    file_path = request.GET.get('file_path')
    keyword = request.GET.get('keyword', '')
    if not file_path or not os.path.exists(file_path):
        return JsonResponse({'error': 'File not found or path not provided'}, status=400)

    lines, words, bytes_count, keyword_count = word_count(file_path, keyword)
    response = {'lines': lines, 'words': words, 'bytes': bytes_count}
    if keyword:
        response['keyword_count'] = keyword_count
    return JsonResponse(response)


@csrf_exempt
def batch_wc_view(request):
    files = request.FILES.getlist('files')
    keyword = request.POST.get('keyword', '')
    if not files:
        return JsonResponse({'error': 'No files uploaded'}, status=400)

    results = []
    for file in files:
        file_path = default_storage.save(file.name, file)
        lines, words, bytes_count, keyword_count = word_count(file_path, keyword)
        results.append({
            'file_name': file.name,
            'lines': lines,
            'words': words,
            'bytes': bytes_count,
            'keyword_count': keyword_count
        })
        default_storage.delete(file_path)  # Clean up after processing

    return JsonResponse(results, safe=False)
