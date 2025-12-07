# Financial Data Analyzer

A comprehensive microservices-based system for scraping, analyzing, and searching financial news articles. The system extracts structured information from articles including spokespersons, sources, people, comments, and metadata using AI-powered analysis.

## 🏗️ Architecture Overview

This system follows a microservices architecture with message-driven communication using RabbitMQ. The workflow processes articles through multiple stages: configuration dispatch → content scraping → AI analysis → database storage → search and retrieval.

```
┌─────────────────┐
│ Dispatcher      │
│ Service         │
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │RabbitMQ │
    └────┬────┘
         │
         ├──────────────┐
         │              │
         ▼              ▼
┌──────────────┐  ┌──────────────┐
│ Article      │  │ Article      │
│ Content      │  │ Analyzer     │
│ Scraper      │  │ Consumer     │
└──────┬───────┘  └──────┬───────┘
       │                  │
       │                  ▼
       │            ┌──────────┐
       │            │PostgreSQL│
       │            └────┬─────┘
       │                 │
       └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │  Search API     │
    │  Analyzer API   │
    └────────┬────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌──────────┐
│ Admin UI │  │Search UI │
└──────────┘  └──────────┘
```

## 📦 Components

### Backend Services

#### 1. **Dispatcher Service** (`dispatcher-service/`)
- **Purpose**: Initiates the article processing pipeline by fetching article configurations from the database and publishing them to RabbitMQ
- **Technology**: Python
- **Key Features**:
  - Reads article configurations from PostgreSQL
  - Publishes messages to RabbitMQ with priority support
  - Configurable via `application.ini`

#### 2. **Article Content Scraper** (`article-content-scrapper/`)
- **Purpose**: Scrapes article content from various news websites
- **Technology**: Python, FastAPI, Selenium, Playwright, BeautifulSoup
- **Key Features**:
  - Supports multiple automation frameworks (Selenium, Playwright)
  - Configurable browser settings (headless, proxy, user agent)
  - Batch article extraction
  - Failed article retry mechanism
  - Email notifications for errors
  - Publishes scraped content to RabbitMQ for analysis
- **Port**: 9005

#### 3. **Article Analyzer Consumer** (`article-analyzer-consumer/`)
- **Purpose**: Consumes article content from RabbitMQ, analyzes it using AI, and stores structured data in the database
- **Technology**: Python, Google Gemini AI, Pika (RabbitMQ client)
- **Key Features**:
  - AI-powered extraction of:
    - Spokesperson details (name, designation, organization, location, past roles)
    - Source information
    - People mentioned in articles
    - Comments and quotes
    - Article metadata (keywords, summary, author info)
  - Validation scoring for extracted data
  - Automatic retry and error handling
  - Database persistence

#### 4. **Analyzer API** (`analyzer-api/`)
- **Purpose**: REST API for managing article configurations and metadata
- **Technology**: Python, FastAPI, PostgreSQL
- **Key Features**:
  - Azure AD authentication
  - API key management
  - Rate limiting
  - Newspaper configuration management
  - Article metadata configuration retrieval
  - CORS support
- **Port**: 8001
- **Endpoints**:
  - `GET /articles/v1/news` - Fetch all newspapers
  - `GET /articles/v1/config/article-content/{newspaper_id}` - Get article content config
  - `GET /articles/v1/config/article-meta/{newspaper_id}` - Get article metadata config

#### 5. **Article Search API** (`article-search-api/`)
- **Purpose**: Natural language search API for querying analyzed articles
- **Technology**: Python, FastAPI, PostgreSQL, Google Gemini
- **Key Features**:
  - Natural language query processing
  - Semantic search across articles, spokespersons, sources, and people
  - Full article details retrieval
  - CORS support
- **Port**: 8000
- **Endpoints**:
  - `POST /query` - Search articles by natural language query
  - `POST /article` - Fetch complete article details by ID

### Frontend Applications

#### 6. **Admin UI** (`anazlyzer-admin-ui/`)
- **Purpose**: Administrative interface for managing article configurations
- **Technology**: React, TypeScript, Vite, Ant Design, Azure MSAL
- **Key Features**:
  - Azure AD authentication
  - Configuration management
  - Article metadata configuration
  - Redux state management

#### 7. **Article Search UI** (`article-search-ui/`)
- **Purpose**: User-facing interface for searching and viewing articles
- **Technology**: Next.js, React, TypeScript, Tailwind CSS, Radix UI
- **Key Features**:
  - Natural language search interface
  - Article detail views
  - Spokesperson, source, and people information display
  - Modern, responsive design

## 🗄️ Database Schema

The system uses PostgreSQL with two main schemas:

### Configuration Schema (`conf`)
- `newspapers` - Newspaper/source information
- `articlesearchconf` - Article search configurations
- `articlebrowserconf` - Browser automation configurations
- `api_keys` - API key management
- `languages` - Supported languages
- `regions` - Geographic regions

### Analysis Schema (`ai_new`)
- `article_details` - Article metadata (header, summary, keywords, author)
- `spokesperson_details` - Extracted spokesperson information
- `source_details` - Source information
- `people_information` - People mentioned in articles
- `comment_details` - Comments and quotes linked to spokespersons/sources

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL 12+
- RabbitMQ 3.8+
- Docker (optional, for RabbitMQ)

### Environment Setup

Each service requires its own `.env` file. Key environment variables:

#### Analyzer API
```env
DB_HOST=localhost
DB_NAME=your_database
DB_USER=postgres
DB_PASSWORD=your_password
DB_MIN_CONNECTION=1
DB_MAX_CONNECTION=10
AZURE_CLIENT_ID=your_azure_client_id
AZURE_CLIENT_SECRET=your_azure_secret
AZURE_TENANT_ID=your_tenant_id
REDIRECT_URI=http://localhost:5173
FRONTEND_URL=http://localhost:5173
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SENDER_EMAIL=noreply@example.com
RECIPIENT_EMAILS=admin@example.com
EMAIL_ALERT_LEVEL=ERROR
```

#### Article Content Scraper
```env
DB_HOST=localhost
DB_NAME=your_database
DB_USER=postgres
DB_PASSWORD=your_password
MQ_HOST=localhost
MQ_PORT=5672
MQ_USER=admin
MQ_PASSWORD=admin
MQ_VIRTUAL_HOST=/
SPOKESPERSON_ARTICLE_METADATA_QUEUE=article_metadata_queue
SPOKESPERSON_ARTICLE_CONTENT_QUEUE=article_content_queue
SPOKESPERSON_ARTICLE_EXCHANGE=article_exchange
HEADLESS=true
BROWSER=chrome
# ... additional browser and SMTP settings
```

#### Article Analyzer Consumer
```env
DB_HOST=localhost
DB_NAME=your_database
DB_USER=postgres
DB_PASSWORD=your_password
MQ_HOST=localhost
MQ_PORT=5672
MQ_USER=admin
MQ_PASSWORD=admin
SPOKESPERSON_ARTICLE_ANALYZER_QUEUE=article_analyzer_queue

# IMPORTANT: Add your personal Google Gemini API key(s) before running
# You can get your API key from: https://makersuite.google.com/app/apikey
# For multiple keys (quota management), use comma-separated list:
# API_KEYS=["your_key_1", "your_key_2", "your_key_3"]
API_KEYS=["your_gemini_api_key_here"]
API_KEY=your_gemini_api_key_here

# Model configuration
PARSING_MODEL_NAME=gemini-2.0-flash-exp
PARSING_MAX_OUTPUT_TOKENS=8192
PARSING_TEMPERATURE=0.1
PARSING_TOP_P=0.95
PARSING_TOP_K=40
PARSING_CANDIDATE_COUNT=1

VALIDATION_MODEL_NAME=gemini-2.0-flash-exp
VALIDATION_TEMPERATURE=0.1
VALIDATION_TOP_P=0.95
VALIDATION_TOP_K=40
```

#### Article Search API
```env
DB_HOST=localhost
DB_NAME=your_database
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# IMPORTANT: Add your personal Google Gemini API key before running
# You can get your API key from: https://makersuite.google.com/app/apikey
API_KEY=your_gemini_api_key_here
```

### Installation

> **⚠️ IMPORTANT: Before running any services, you must add your personal Google Gemini API key(s) to the respective `.env` files.**
> 
> - Get your API key from: https://makersuite.google.com/app/apikey
> - Add `API_KEY=your_gemini_api_key_here` to:
>   - `article-analyzer-consumer/.env`
>   - `article-search-api/.env`
> - For `article-analyzer-consumer`, you can also set multiple keys for quota management: `API_KEYS=["key1", "key2", "key3"]`

#### 1. Database Setup

```bash
# Create database
createdb financial_analyzer

# Run database creation script
cd article-analyzer-consumer
python db_creation.py
```

#### 2. RabbitMQ Setup

Using Docker:
```bash
cd docker_rabbitmq_for_local_testing
docker-compose up -d
```

Or install RabbitMQ locally and configure accordingly.

#### 3. Backend Services

```bash
# Install dependencies for each service
cd analyzer-api
pip install -r requirements.txt

cd ../article-content-scrapper
pip install -r requirements.txt

cd ../article-analyzer-consumer
pip install -r requirements.txt

cd ../article-search-api
pip install -r requirements.txt

cd ../dispatcher-service
pip install -r requirements.txt  # if exists, or install manually
```

#### 4. Frontend Applications

```bash
# Admin UI
cd anazlyzer-admin-ui
npm install
npm run dev

# Search UI
cd article-search-ui
pnpm install  # or npm install
pnpm dev      # or npm run dev
```

### Running the System

1. **Start RabbitMQ** (if using Docker):
   ```bash
   cd docker_rabbitmq_for_local_testing
   docker-compose up -d
   ```

2. **Start Dispatcher Service**:
   ```bash
   cd dispatcher-service
   python main.py
   ```

3. **Start Article Content Scraper**:
   ```bash
   cd article-content-scrapper
   python main.py
   ```

4. **Start Article Analyzer Consumer**:
   ```bash
   cd article-analyzer-consumer
   python main.py
   ```

5. **Start Analyzer API**:
   ```bash
   cd analyzer-api
   python -m app.main
   # or
   uvicorn app.main:app --host 127.0.0.1 --port 8001
   ```

6. **Start Article Search API**:
   ```bash
   cd article-search-api
   python main.py
   # or
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```

7. **Start Frontend Applications**:
   ```bash
   # Admin UI (port 5173)
   cd anazlyzer-admin-ui
   npm run dev

   # Search UI (port 3000)
   cd article-search-ui
   pnpm dev
   ```

## 🔧 Configuration

### Dispatcher Service Configuration

Edit `dispatcher-service/conf/application.ini`:
```ini
[DB]
host=localhost
database=your_database
user=postgres
password=your_password

[MQ]
article-url_exchange=article_url_exchange
article-url_queue=article_url_queue
article-url_key=article_url_key
connection_attempts=5
retry_delay=1
delivery_mode=2
```

### Browser Automation Settings

Configure in `article-content-scrapper/.env`:
- `HEADLESS`: Run browser in headless mode
- `BROWSER`: Browser type (chrome, firefox, etc.)
- `PROXY_ENABLED`: Enable proxy support
- `PAGE_LOAD_TIMEOUT`: Page load timeout in seconds
- `TAKE_SCREENSHOTS`: Capture screenshots on failure

## 📊 Data Flow

1. **Configuration Dispatch**: Dispatcher service reads article configurations from the database and publishes them to RabbitMQ
2. **Content Scraping**: Article Content Scraper consumes configuration messages, scrapes article content from websites, and publishes content to RabbitMQ
3. **AI Analysis**: Article Analyzer Consumer processes article content using Google Gemini AI to extract structured information
4. **Data Storage**: Analyzed data is stored in PostgreSQL with validation
5. **Search & Retrieval**: Search API provides natural language query capabilities over stored data
6. **UI Access**: Admin UI and Search UI provide interfaces for configuration and search

## 🔐 Authentication

- **Analyzer API**: Uses Azure AD authentication with JWT tokens
- **Admin UI**: Integrated with Azure MSAL for authentication
- **API Keys**: Supports API key-based authentication for programmatic access

## 🧪 Testing

### Local RabbitMQ Testing

Use the provided Docker Compose setup:
```bash
cd docker_rabbitmq_for_local_testing
docker-compose up -d
```

Access RabbitMQ Management UI at `http://localhost:15672` (default: admin/admin)

## 📝 API Documentation

### Analyzer API

Once running, access interactive API docs at:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

### Article Search API

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🛠️ Development

### Project Structure

```
Financial_data_ananalyzer/
├── analyzer-api/              # Configuration management API
├── anazlyzer-admin-ui/        # Admin React application
├── article-analyzer-consumer/ # AI analysis service
├── article-content-scrapper/  # Web scraping service
├── article-search-api/        # Search API
├── article-search-ui/         # Search Next.js application
├── dispatcher-service/        # Message dispatcher
└── docker_rabbitmq_for_local_testing/ # RabbitMQ setup
```

### Key Technologies

- **Backend**: FastAPI, Python, PostgreSQL, RabbitMQ, Pika
- **AI/ML**: Google Gemini (Generative AI)
- **Web Scraping**: Selenium, Playwright, BeautifulSoup
- **Frontend**: React, Next.js, TypeScript, Tailwind CSS
- **Authentication**: Azure AD, MSAL
- **State Management**: Redux Toolkit

## 🐛 Troubleshooting

### Common Issues

1. **RabbitMQ Connection Errors**
   - Verify RabbitMQ is running: `docker ps` or check service status
   - Check connection credentials in `.env` files
   - Ensure ports 5672 and 15672 are accessible

2. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check database credentials
   - Ensure database and schemas are created

3. **Browser Automation Failures**
   - Install browser drivers (ChromeDriver, GeckoDriver)
   - For Playwright: Run `playwright install`
   - Check headless mode settings
   - Verify proxy settings if enabled

4. **AI Analysis Failures**
   - **IMPORTANT**: Ensure you have added your personal Google Gemini API key to the `.env` file
   - Verify Google Gemini API key is correctly configured in environment variables
   - Check API quota and rate limits at https://makersuite.google.com/app/apikey
   - Review validation score thresholds
   - If using multiple keys, ensure `API_KEYS` is properly formatted as a list

## 📄 License

[Specify your license here]

## 👥 Contributors

[Add contributor information]

## 📧 Support

For issues and questions, please [create an issue](link-to-issues) or contact the development team.
