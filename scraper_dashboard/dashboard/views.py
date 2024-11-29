from django.shortcuts import render
from django.core.paginator import Paginator
import subprocess
import json
import os
import threading

def run_consuming_process():
    script_path = "/home/ramtin/Desktop/projects/sentiment_analysis/publisher-consumer.py"
    try:
        subprocess.run(["python3", script_path], check=True)
        print("Script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error in running consumer: {e}")

def home_view(request):
    threading.Thread(target=run_consuming_process, daemon=True).start()
    return render(request, 'dashboard/home.html')

def news_view(request):
    file_path = os.path.join(os.path.dirname(__file__), '../scraped_data.json')

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print("Data read successfully:", data)
    except FileNotFoundError:
        data = []
        print("File not found")

    if not data:
        print("No data found in JSON file")

    all_news = [item for sublist in data for item in sublist]

    print("Total news items:", len(all_news))

    paginator = Paginator(all_news, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/news.html', {'page_obj': page_obj})


def dashboard_view(request):
    file_path = os.path.join(os.path.dirname(__file__), '../scraped_data.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    positive_count = sum(1 for sublist in data for item in sublist if item.get('sentiment', {}).get('label') == 'POSITIVE')
    negative_count = sum(1 for sublist in data for item in sublist if item.get('sentiment', {}).get('label') == 'NEGATIVE')
    neutral_count = sum(1 for sublist in data for item in sublist if item.get('sentiment', {}).get('label') == 'NEUTRAL')

    total_count = sum(len(sublist) for sublist in data)

    context = {
        'total_count': total_count,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
    }
    return render(request, 'dashboard/dashboard.html', context)
