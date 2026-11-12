# AlbumBot API Specification

## 1. Project Overview
**Name:** AlbumBot API
**Purpose:** A semantic music discovery assistant that processes album metadata. It uses Retrieval-Augmented Generation (RAG) to find albums based on natural-language queries and provides conversational listening recommendations.
**Target Role:** AI Data Product Engineer (Megamedia)

## 2. Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **Database:** PostgreSQL with `pgvector` extension
* **Data Engineering:** Apache Airflow, dbt (Data Build Tool)
* **AI/LLM:** Google Gemini API (for text generation and embeddings)
* **Containerization:** Docker, Docker Compose

## 3. Database Schema (PostgreSQL)

### Table: `album_catalog`
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `UUID` | Primary Key |
| `title` | `VARCHAR` | Album title |
| `artist` | `VARCHAR` | Primary recording artist |
| `description` | `TEXT` | Cleaned description of the album |
| `genre` | `VARCHAR` | Primary musical genre |
| `embedding` | `VECTOR(768)` | Vector representation of the album description |

## 4. API Endpoints

### 4.1. Health Check
* **Endpoint:** `GET /health`
* **Description:** Verifies API and Database connectivity.
* **Response:** `{ "status": "ok", "db_connection": true }`

### 4.2. Semantic Search
* **Endpoint:** `POST /search`
* **Description:** Vectorizes the user query and performs a nearest-neighbor search using cosine distance (`<=>`) in pgvector.
* **Payload:**
  ```json
  {
    "query": "A warm, acoustic folk album for a quiet evening",
    "top_k": 3
  }
  ```
* **Response:** Array of matched content objects with their similarity scores.

### 4.3. Chat / RAG
* **Endpoint:** `POST /chat`
* **Description:** Retrieves semantic matches and injects them into an LLM prompt to return a conversational recommendation.
* **Payload:**
  ```json
  {
    "message": "I'm looking for an energetic electronic album to work out to."
  }
  ```
* **Response:**
  ```json
  {
    "response": "I recommend checking out 'Discovery' by Daft Punk. Its upbeat electronic production makes it a great choice for a workout..."
  }
  ```

## 5. Data Pipeline (Airflow & dbt)
1. **Extract:** Airflow DAG downloads raw album catalog data weekly.
2. **Transform (dbt):** Cleans null values, standardizes text casing, and outputs to an analytics-ready schema.
3. **Load (Vectorize):** Airflow triggers a Python task to chunk the album `description` text, fetch embeddings from the LLM provider, and UPSERT into the `album_catalog` table.

## 6. Environment Variables (`.env`)
```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/albumbot

# AI Provider
GEMINI_API_KEY=your_api_key_here

# App Config
ENVIRONMENT=development
LOG_LEVEL=info
```