from flask import Flask, request, jsonify
from newspaper import Article, Config
import os
from functools import wraps
import logging
import nltk

nltk.download('punkt_tab')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Fixed token for API security
API_TOKEN = os.getenv('API_TOKEN', 'your-secure-token-here')

# Validate that we have a proper token
if API_TOKEN == 'your-secure-token-here':
    logger.warning("Using default API token - please set a proper API_TOKEN environment variable")

def require_token(f):
    """Decorator to require API token authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error': 'Authorization header missing'}), 401

        # Check if token is provided in format: Bearer <token>
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = auth_header

        if token != API_TOKEN:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated_function

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.info(f"Health check passed with API token: {API_TOKEN[:8]}...")
    if API_TOKEN == 'your-secure-token-here':
        logger.error("Health check failed: API token not configured")
        return jsonify({'status': 'error', 'message': 'API token not configured'}), 500
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

@app.route('/parse', methods=['POST'])
@require_token
def parse_article():
    """Parse article from URL using newspaper4k"""
    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400

        url = data['url']

        if not url or not isinstance(url, str):
            return jsonify({'error': 'Valid URL string is required'}), 400

        logger.info(f"Parsing article from URL: {url}")

        c =  Config()
        c.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        c.keep_article_html = True
        c.remove_unknown_tags = False
        c.allow_tags = ['a', 'span', 'p', 'br', 'strong', 'b',
            'em', 'i', 'tt', 'code', 'pre', 'blockquote', 'img', 'h1',
            'h2', 'h3', 'h4', 'h5', 'h6', 'figure', 'img', 'picture', 'ul', 'li', 'div', 'section', 'article']
        c.browser_html_parser = 'lxml'
        c.fetch_images = True
        c.request_timeout = 60

        # Download and parse the article
        article = Article(url, config=c)
        article.download()
        article.parse()
        article.nlp()

        # Extract article information
        article_data = {
            'raw_html': article.html,
            'html': article.article_html,
            'title': article.title,
            'text': article.text,
            'summary': article.summary,
            'keywords': article.keywords,
            'authors': article.authors,
            'publish_date': article.publish_date.isoformat() if article.publish_date else None,
            'top_image': article.top_image,
            'images': article.images,
            'movies': article.movies,
            'meta_description': article.meta_description,
            'meta_keywords': article.meta_keywords,
            'meta_lang': article.meta_lang,
            'meta_favicon': article.meta_favicon,
            'meta_img': article.meta_img,
            'canonical_link': article.canonical_link,
            'url': url
        }

        logger.info(f"Successfully parsed article: {article.title}")

        return jsonify({
            'success': True,
            'article': article_data
        })

    except Exception as e:
        logger.error(f"Error parsing article: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to parse article: {str(e)}'
        }), 500

@app.route('/parse/batch', methods=['POST'])
@require_token
def parse_articles_batch():
    """Parse multiple articles from URLs"""
    try:
        data = request.get_json()

        if not data or 'urls' not in data:
            return jsonify({'error': 'URLs list is required'}), 400

        urls = data['urls']

        if not isinstance(urls, list):
            return jsonify({'error': 'URLs must be a list'}), 400

        if len(urls) > 10:  # Limit batch size
            return jsonify({'error': 'Maximum 10 URLs allowed per batch'}), 400

        results = []

        for url in urls:
            try:
                article = Article(url)
                article.download()
                article.parse()

                article_data = {
                    'url': url,
                    'title': article.title,
                    'text': article.text,
                    'summary': article.summary,
                    'keywords': article.keywords,
                    'authors': article.authors,
                    'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                    'top_image': article.top_image,
                    'success': True
                }

                results.append(article_data)

            except Exception as e:
                results.append({
                    'url': url,
                    'success': False,
                    'error': str(e)
                })

        return jsonify({
            'success': True,
            'results': results
        })

    except Exception as e:
        logger.error(f"Error in batch parsing: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to process batch: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3002))
    app.run(host='0.0.0.0', port=port, debug=False)