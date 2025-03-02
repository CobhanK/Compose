#main/views.py
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

# Create your views here.
@require_http_methods(["GET"])
def index(request):
    #return HttpResponse("Hello world!") 
    return render(request, 'index.html')

@require_http_methods(["GET"])
def record(request):
    return render(request, 'record.html')

# views.py
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def upload_wav(request):
    if request.method == 'POST':
        try:
            # Check if request contains a file
            if 'audio_file' not in request.FILES:
                return JsonResponse({'error': 'No audio file found in request'}, status=400)
            
            audio_file = request.FILES['audio_file']
            
            # Validate that it's a WAV file
            if not audio_file.name.endswith('.wav'):
                return JsonResponse({'error': 'File must be a WAV file'}, status=400)
            
            # Create media directory if it doesn't exist
            media_dir = os.path.join(settings.BASE_DIR, 'media')
            os.makedirs(media_dir, exist_ok=True)
            
            # Generate a unique filename to prevent overwriting
            # You could also use a UUID or timestamp
            filename = audio_file.name
            file_path = os.path.join(media_dir, filename)
            
            # Handle filename conflicts
            counter = 1
            while os.path.exists(file_path):
                name_parts = os.path.splitext(audio_file.name)
                filename = f"{name_parts[0]}_{counter}{name_parts[1]}"
                file_path = os.path.join(media_dir, filename)
                counter += 1
            
            # Save the file
            with open(file_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)
            
            return JsonResponse({
                'success': True,
                'filename': filename,
                'path': f'/media/{filename}'
            }, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

