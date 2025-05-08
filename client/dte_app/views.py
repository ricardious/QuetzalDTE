from django.shortcuts import render, redirect
from django.contrib import messages
import os
import tempfile
from datetime import date

GLOBAL_CONTEXT = {"file_content": None, "binary_file": None, "file_name": None}
ENDPOINT = "http://localhost:4000/"

def home(request):
    return render(request, 'pages/home.html', {
        'today': date.today().strftime('%d/%m/%Y'),
    })

def dashboard(request):
    return render(request, 'pages/dashboard.html')

def upload_file(request):
    return render(request, 'pages/upload_file.html')

def query_data(request):
    return render(request, 'pages/query_data.html')

def vat_summary(request):
    return render(request, 'pages/vat_summary.html')
