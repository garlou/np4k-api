# Article Parser API

A secure Python API that uses newspaper4k to parse and extract information from news articles and web pages.

## Features

- 🔐 **Secure**: Token-based authentication
- 📰 **Article Parsing**: Extract title, text, summary, keywords, authors, and more
- 🚀 **Fast**: Built with Flask and Gunicorn
- 🐳 **Dockerized**: Easy deployment with Docker
- 📊 **Batch Processing**: Parse multiple URLs at once
- 🏥 **Health Checks**: Built-in health monitoring

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd qiosq-np4k
   ```

2. **Set your API token:**

   **Option A: Using secrets file (recommended)**
   ```bash
   # Generate a secure token
   python generate_token.py

   # Copy the template and update with your token
   cp secrets.env.template secrets.env
   # Edit secrets.env and replace 'your-secure-token-here' with your generated token
   ```

   **Option B: Direct environment variable**
   Edit `docker-compose.yml` and change the `API_TOKEN` value:
   ```yaml
   environment:
     - API_TOKEN=your-actual-secure-token-here
   ```

3. **Build and run:**
   ```bash
   docker-compose up --build
   ```

4. **Test the API:**
   ```bash
   curl http://localhost:3002/health
   ```

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t article-parser-api .
   ```

2. **Run the container:**
   ```bash
   docker run -p 3002:3002 -e API_TOKEN=your-secure-token-here article-parser-api
   ```

## API Endpoints

### Authentication

All endpoints (except `/health`) require authentication using a Bearer token in the Authorization header:

```
Authorization: Bearer your-secure-token-here
```

### Endpoints

#### `GET /health`
Health check endpoint (no authentication required)

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### `POST /parse`
Parse a single article from a URL

**Request:**
```json
{
  "url": "https://example.com/article"
}
```

**Response:**
```json
{
  "success": true,
  "article": {
    "title": "Article Title",
    "text": "Full article text...",
    "summary": "Article summary...",
    "keywords": ["keyword1", "keyword2"],
    "authors": ["Author Name"],
    "publish_date": "2023-01-01T00:00:00",
    "top_image": "https://example.com/image.jpg",
    "images": ["https://example.com/image1.jpg"],
    "movies": ["https://example.com/video.mp4"],
    "meta_description": "Meta description",
    "meta_keywords": "meta, keywords",
    "meta_lang": "en",
    "meta_favicon": "https://example.com/favicon.ico",
    "meta_img": "https://example.com/meta-image.jpg",
    "canonical_link": "https://example.com/canonical",
    "url": "https://example.com/article"
  }
}
```

#### `POST /parse/batch`
Parse multiple articles from URLs (max 10 URLs per request)

**Request:**
```json
{
  "urls": [
    "https://example.com/article1",
    "https://example.com/article2"
  ]
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "url": "https://example.com/article1",
      "title": "Article 1 Title",
      "text": "Article 1 text...",
      "summary": "Article 1 summary...",
      "keywords": ["keyword1"],
      "authors": ["Author 1"],
      "publish_date": "2023-01-01T00:00:00",
      "top_image": "https://example.com/image1.jpg",
      "success": true
    },
    {
      "url": "https://example.com/article2",
      "title": "Article 2 Title",
      "text": "Article 2 text...",
      "summary": "Article 2 summary...",
      "keywords": ["keyword2"],
      "authors": ["Author 2"],
      "publish_date": "2023-01-02T00:00:00",
      "top_image": "https://example.com/image2.jpg",
      "success": true
    }
  ]
}
```

## Usage Examples

### Using curl

**Parse a single article:**
```bash
curl -X POST http://localhost:3002/parse \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secure-token-here" \
  -d '{"url": "https://example.com/article"}'
```

**Parse multiple articles:**
```bash
curl -X POST http://localhost:3002/parse/batch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secure-token-here" \
  -d '{"urls": ["https://example.com/article1", "https://example.com/article2"]}'
```

### Using Python

```python
import requests

API_BASE = "http://localhost:3002"
TOKEN = "your-secure-token-here"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# Parse single article
response = requests.post(
    f"{API_BASE}/parse",
    headers=HEADERS,
    json={"url": "https://example.com/article"}
)
article_data = response.json()

# Parse multiple articles
response = requests.post(
    f"{API_BASE}/parse/batch",
    headers=HEADERS,
    json={"urls": ["https://example.com/article1", "https://example.com/article2"]}
)
batch_results = response.json()
```

## Configuration

### Environment Variables

- `API_TOKEN`: Your secure token for API authentication (default: "your-secure-token-here")
- `PORT`: Port to run the API on (default: 3002)

### Security

⚠️ **Important**: Always change the default API token in production!

#### Using Secrets File (Recommended)

1. Generate a secure token:
   ```bash
   python generate_token.py
   ```

2. Create and configure your secrets file:
   ```bash
   cp secrets.env.template secrets.env
   # Edit secrets.env and replace 'your-secure-token-here' with your generated token
   ```

3. The `secrets.env` file is automatically excluded from Docker builds and should never be committed to version control.

#### Security Best Practices

- ✅ Use the `secrets.env` file for storing sensitive configuration
- ✅ Generate strong, random tokens using the provided script
- ✅ Never commit `secrets.env` to version control
- ✅ Use different tokens for different environments (dev, staging, prod)
- ✅ Rotate tokens regularly in production
- ❌ Never hardcode tokens in source code
- ❌ Never use default tokens in production

## Development

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export API_TOKEN=your-secure-token-here
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

### Testing

Test the API with a sample URL:

```bash
curl -X POST http://localhost:3002/parse \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secure-token-here" \
  -d '{"url": "https://www.bbc.com/news/world-us-canada-12345678"}'
```

## Troubleshooting

### Common Issues

1. **Permission denied errors**: Make sure the API token is correct
2. **Article parsing fails**: Some websites may block automated requests
3. **Docker build fails**: Ensure you have Docker and Docker Compose installed

### Logs

View container logs:
```bash
docker-compose logs -f article-parser-api
```

## License

This project is open source and available under the MIT License.