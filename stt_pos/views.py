from django.shortcuts import render

# stt_pos/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'stt_pos/index.html')