
---

# Sentiment Analysis News Scraper Project

## Project Overview
This project is a complete pipeline for scraping news articles from multiple sources, analyzing their sentiment, and displaying the results in a Django-based web application. The system uses Playwright for web scraping, a custom sentiment analysis model built with Hugging Face's Transformers, and Django for the frontend dashboard.

## Project Structure
```
sentiment_analysis/
├── distilbert/
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── tokenizer_config.json
│   └── vocab.txt
├── publisher-consumer.py
├── scraper.py
├── sentiment_analysis_model.py
└── scraper_dashboard/
    ├── dashboard/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── models.py
    │   ├── templates/
    │   │   └── dashboard/
    │   │       ├── dashboard.html  # Displays scraped data and sentiment analysis results
    │   │       └── home.html        # Homepage of the dashboard
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── manage.py  # Django project management file
    ├── settings.py  # Django project settings
    ├── scraped_data.json  # JSON file storing the scraped data
    └── requirements.txt  # List of project dependencies
```

## Detailed Explanation of Core Files

### 1. `publisher-consumer.py`
- **Purpose**: Responsible for connecting to a RabbitMQ message queue to send URLs to be scraped and consume the URLs for processing.
- **Key Libraries**:
  - `aio_pika`: For handling asynchronous messaging with RabbitMQ.
  - `scraper`: The module responsible for web scraping.
- **Functions**:
  - `send_to_queue(urls)`: Sends a list of URLs to the RabbitMQ queue.
  - `consume_from_queue()`: Consumes URLs from the queue and calls the `scrape_page()` function to process them.

### 2. `scraper.py`
- **Purpose**: Contains the scraping logic for each news source and saves the results to a JSON file.
- **Key Libraries**:
  - `playwright.async_api`: Used for web scraping in an asynchronous manner.
  - `BeautifulSoup`: Parses and extracts data from HTML content.
  - `sentiment_analysis_model`: For analyzing sentiment in the scraped text.
- **Functions**:
  - `scrape_tansimnews(page)`, `scrape_mehrnews(page)`, `scrape_irna(page)`, `scrape_isna(page)`: Functions that target specific news sites and extract relevant information like title, paragraph, and publication time.
  - `scrape_generic(page)`: A fallback function for generic scraping.
  - `scrape_page(url, retries=3)`: The main function to launch a browser instance, scrape data using the appropriate scraper, and analyze sentiment.
  - `save_results_to_json(file_name, data)`: Saves the collected data to a JSON file.

### 3. `sentiment_analysis_model.py`
- **Purpose**: Contains the class `SentimentAnalyzer` that loads and runs a sentiment analysis model.
- **Key Libraries**:
  - `transformers`: Used for loading and running sentiment analysis pipelines from Hugging Face.
- **Class**:
  - `SentimentAnalyzer`: Initializes a sentiment analysis model and has a method `analyze()` that takes text input and returns the sentiment.

### 4. Django App (`scraper_dashboard`)
- **Purpose**: Provides the frontend for displaying news articles and sentiment analysis results.
- **Files**:
  - **`urls.py`**: Maps the URLs to respective views.
  - **`views.py`**: Contains the view functions that handle HTTP requests and render templates.
  - **Templates**:
    - `dashboard.html`: Displays the data analysis results and metrics.
    - `home.html`: The homepage of the dashboard.

## How the Project Works
1. **URL Submission**:
   - The `publisher-consumer.py` script sends URLs of news articles to a RabbitMQ message queue using `send_to_queue()`.
2. **Data Scraping and Sentiment Analysis**:
   - The `consume_from_queue()` function reads URLs from the queue and invokes `scrape_page()` to fetch and parse data using Playwright and BeautifulSoup.
   - The content is analyzed for sentiment using the `SentimentAnalyzer` class, and the results are stored in `scraped_data.json`.
3. **Django Dashboard**:
   - The Django app provides a web interface that reads from `scraped_data.json` and displays:
     - All collected articles with pagination.
     - Sentiment analysis results in the dashboard view.
4. **Background Processing**:
   - When the `home_view()` function is called, a separate thread runs `run_consuming_process()` to start the `publisher-consumer.py` script, ensuring that data collection runs in the background.

## Installation and Setup

### Prerequisites
- **Python 3.x** (recommended: Python 3.8+)
- **Django** (Version 4.0 or higher)
- **Playwright** for browser automation
- **Transformers** library for sentiment analysis

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/sentiment_analysis.git
   cd sentiment_analysis
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Browsers**:
   ```bash
   python -m playwright install
   ```

5. **Run Django Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Web Application**:
   Visit `http://127.0.0.1:8000/` in your browser.

## How to Use the Project
1. **Navigate to the homepage** to start the background process that collects data from the specified news sources.
2. **View news articles** by going to the `/news/` path.
3. **Access sentiment analysis metrics** on the `/dashboard/` path, where insights on positive, negative, and neutral article counts are displayed.

## Project Dependencies
List of dependencies in `requirements.txt`:
- `Django>=4.0`
- `playwright>=1.0.0`
- `transformers>=4.0.0`
- `beautifulsoup4>=4.9.0`
- `aio-pika>=6.8.0`

---

