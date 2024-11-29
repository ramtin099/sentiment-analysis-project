from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import os
import sentiment_analysis_model


def save_results_to_json(file_name, data):
    if os.path.exists(file_name):
        with open(file_name, 'r+', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []

            existing_data.append(data)

            file.seek(0)
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
    else:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump([data], file, ensure_ascii=False, indent=4)

async def scrape_tansimnews(page):
    html_content = await page.content()
    soup = BeautifulSoup(html_content, "html.parser")
    target_classes = ["col-md-8 col-xs-8 text-container vcenter"]
    articles = []

    for target_class in target_classes:
        articles.extend(soup.find_all("div", class_=target_class))

    results = []

    for article in articles:
        title_tag = article.find("h2")
        title = title_tag.get_text(strip=True) if title_tag else "no_title"

        paragraph_tag = article.find("h4")
        paragraph = paragraph_tag.get_text(strip=True) if paragraph_tag else "no_paragraph"

        time_tag = article.find("time")
        time = time_tag.get_text(strip=True) if time_tag else "no_time"

        results.append({
            "title": title,
            "paragraph": paragraph,
            "time": time,
        })

    return results


async def scrape_mehrnews(page):
    html_content = await page.content()
    soup = BeautifulSoup(html_content, "html.parser")

    target_classes = ["news", "audio", "photo"]
    articles = []

    for target_class in target_classes:
        articles.extend(soup.find_all("li", class_=target_class))

    results = []

    for article in articles:
        title_tag = article.find("h3")
        title = title_tag.get_text(strip=True) if title_tag else "no_title"

        paragraph_tag = article.find("p")
        paragraph = paragraph_tag.get_text(strip=True) if paragraph_tag else "no_paragraph"

        time_tag = article.find("time")
        time = time_tag.get_text(strip=True) if time_tag else "no_time"

        results.append({
            "title": title,
            "paragraph": paragraph,
            "time": time,
        })

    return results


async def scrape_irna(page):
    html_content = await page.content()
    soup = BeautifulSoup(html_content, "html.parser")

    target_classes = ["news", "audio", "photo"]
    articles = []

    for target_class in target_classes:
        articles.extend(soup.find_all("li", class_=target_class))

    results = []

    for article in articles:
        title_tag = article.find("h3")
        title = title_tag.get_text(strip=True) if title_tag else "no_title"

        paragraph_tag = article.find("p")
        paragraph = paragraph_tag.get_text(strip=True) if paragraph_tag else "no_paragraph"

        time_tag = article.find("time")
        time = time_tag.get_text(strip=True) if time_tag else "no_time"

        results.append({
            "title": title,
            "paragraph": paragraph,
            "time": time
        })

    return results


async def scrape_isna(page):
    html_content = await page.content()
    soup = BeautifulSoup(html_content, "html.parser")

    target_classes = ["trans", "desc", "coverage"]
    articles = []

    for target_class in target_classes:
        articles.extend(soup.find_all("li", class_=target_class))

    results = []

    for article in articles:
        title_tag = article.find("h3")
        title = title_tag.get_text(strip=True) if title_tag else "no_title"

        paragraph_tag = article.find("p")
        paragraph = paragraph_tag.get_text(strip=True) if paragraph_tag else "no_paragraph"

        time_tag = article.find("time")
        time = time_tag.get_text(strip=True) if time_tag else "no_time"

        results.append({
            "title": title,
            "paragraph": paragraph,
            "time": time
        })

    return results


async def scrape_generic(page):
    html_content = await page.content()
    soup = BeautifulSoup(html_content, "html.parser")
    tags_to_extract = ["p", "div", "span", "article"]
    main_content = " ".join(
        [tag.get_text(strip=True) for t in tags_to_extract for tag in soup.find_all(t)]
    )
    return {"title": soup.title.string, "content": main_content}


SCRAPERS = {
    'en.isna.ir/archive': scrape_isna,
    'en.irna.ir/archive': scrape_irna,
    'en.mehrnews.com/archive': scrape_mehrnews,
    'tasnimnews.com/en/archive': scrape_tansimnews,
}

sentiment = sentiment_analysis_model.SentimentAnalyzer()

async def scrape_page(url, retries=3):
    for attempt in range(retries):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await page.set_extra_http_headers({
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                })

                await page.goto(f"https://{url}", timeout=60000)

                if url in SCRAPERS:
                    results = await SCRAPERS[url](page)
                else:
                    results = await scrape_generic(page)

                for result in results:
                    text = result.get("paragraph", "") or result.get("title", "")
                    if text:
                        print(f"Analyzing text: {text}")
                        try:
                            result_text = sentiment.analyze(text)
                            print(f"Sentiment result: {result_text}")
                        except Exception as e:
                            print(f"Sentiment analysis failed: {e}")
                            result_text = {"label": "UNKNOWN", "score": 0.0}
                        result["sentiment"] = result_text
                    else:
                        result["sentiment"] = {"label": "NO_TEXT", "score": 0.0}

                file_name = 'scraped_data.json'
                save_results_to_json(file_name, results)
                await browser.close()
                return results

        except Exception as e:
            print(f"Error occurred during scraping: {e}")
            if attempt < retries - 1:
                print("Retrying...")
            else:
                print("Max retries reached.")