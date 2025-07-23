from playwright.sync_api import sync_playwright
import newspaper
import time

def scrape_with_playwright(url):
    # Using Playwright to render JavaScript
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        time.sleep(1) # Allow the javascript to render
        content = page.content()
        browser.close()

    # Using Newspaper4k to parse the page content
    article = newspaper.article(url, input_html=content, language='en')

    return article

# Example URL
url = 'https://www.reuters.com/legal/litigation/us-funded-contraceptives-poor-nations-be-burned-france-sources-say-2025-07-23'  # Replace with the URL of your choice

# Scrape and process the article
article = scrape_with_playwright(url)
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(f"Keywords: {article.keywords}")