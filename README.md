# AlbumBot API

A semantic music discovery assistant for album catalogs. AlbumBot uses Retrieval-Augmented Generation (RAG) and vector similarity search to provide natural, conversational album recommendations.

## Architecture

This project implements a robust AI Data Engineering pipeline connecting modern databases with Large Language Models, demonstrating end-to-end product development.

*   **Backend Framework:** FastAPI for high-performance, low-latency API endpoints.
*   **Vector Database:** PostgreSQL equipped with the `pgvector` extension for efficient semantic search (L2, inner product, cosine distance).
*   **Data Orchestration & Transformation:** Apache Airflow handles the ETL workflows, while dbt manages modular SQL data transformations, preparing raw content metadata for vectorization.
*   **Containerization:** Docker and Docker Compose for reproducible infrastructure setup.
*   **AI Integration:** Integrates Gemini LLM for conversational responses and leverages Model Context Protocol (MCP) concepts for advanced model-to-tool connections.

## Project Structure

*   `docker-compose.yml`: Defines the PostgreSQL (`pgvector`) and FastAPI services.
*   `app/`: Contains the FastAPI application logic.
    *   `app_main.py`: The entry point for the API, defining the `/search` and `/chat` endpoints.
    *   `app_database.py`: Database connection and session management (SQLAlchemy/SQLModel).
*   `airflow/`: Contains the Airflow DAGs for data ingestion and orchestration.
*   `dbt/`: Contains the dbt project for album metadata transformations and data cleaning.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [repository-url]
    cd albumbot-api
    ```

2.  **Environment Variables:**
    Create a `.env` file in the root directory and configure the necessary variables (e.g., database credentials, API keys).

3.  **Start the Infrastructure:**
    ```bash
    docker-compose up -d
    ```

4.  **Initialize the Database:**
    (Instructions for running initial migrations or setup scripts).

## API Endpoints

*   `POST /search`: Receives a natural-language music query, vectorizes it, and returns the top matching albums from PostgreSQL.
*   `POST /chat`: Receives a listener request, retrieves relevant albums via internal search, and generates a conversational listening recommendation using the Gemini LLM.