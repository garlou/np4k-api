from playwright.sync_api import sync_playwright
import newspaper
import time
import nltk
nltk.download('punkt_tab')

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
url = 'https://www.reuters.com/legal/litigation/us-funded-contraceptives-poor-nations-be-burned-france-sources-say-2025-07-23/'
print(url)
# Scrape and process the article
article = scrape_with_playwright(url)
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(f"Keywords: {article.keywords}")

# Example URL
url = 'https://www.crowdfunder.co.uk/p/streatham-common-paddling-pool'
print(url)
# Scrape and process the article
article = scrape_with_playwright(url)
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(f"Keywords: {article.keywords}")

# Example URL
url = 'https://edition.cnn.com/2025/07/22/politics/doj-ghislaine-maxwell-epstein'
print(url)
# Scrape and process the article
article = scrape_with_playwright(url)
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(f"Keywords: {article.keywords}")

# Example URL
url = 'https://www.publico.pt/2025/07/18/politica/noticia/portugal-oposse-inclusao-direito-palestinianos-comer-declaracao-cplp-2140693'
print(url)
# Scrape and process the article
article = scrape_with_playwright(url)
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(f"Keywords: {article.keywords}")

# Example URL
url = 'https://newsletter.pragmaticengineer.com/p/project-management-in-tech'
print(url)
# Scrape and process the article
article = scrape_with_playwright(url)
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(f"Keywords: {article.keywords}")

# Example URL
url = 'https://londonist.com/london/things-to-do/streatham-common-kite-day-festival'
print(url)
# Scrape and process the article
article = scrape_with_playwright(url)
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(f"Keywords: {article.keywords}")

# Example URL
url = 'https://www.bloomberg.com/news/articles/2025-07-23/eu-readies-100-billion-no-deal-plan-to-match-us-30-tariff?srnd=homepage-europe'
print(url)
# Scrape and process the article
article = scrape_with_playwright(url)
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(f"Keywords: {article.keywords}")

# Example URL
url = 'https://garnix.io/blog/garn-v0_0_18'
print(url)
# Scrape and process the article
article = scrape_with_playwright(url)
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(f"Keywords: {article.keywords}")