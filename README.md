# Build a Banking Workflow App Using Django, MongoDB & Voyage AI (Datacamp)

A hands-on codealong project that demonstrates how to build a banking document workflow application with semantic search and retrieval augmented generation (RAG).

## Key Takeaways

- Build a functional web application with Django to serve as your workflow interface.
- Implement semantic search and retrieval augmented generation using MongoDB Atlas Vector Search and Voyage AI.
- Get hands-on with a practical banking workflow use case, from document retrieval to automated task handling.

## Prerequisites

- Python 3.12+
- A MongoDB Atlas cluster (free tier works)
- A [Voyage AI](https://www.voyageai.com/) API key

## Setup

1. Clone the repository and checkout the starter branch:
   ```bash
   git clone <repo-url>
   cd banking-workflow-codealong
   git checkout starter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key-here
   DB_ENGINE=django_mongodb_backend
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=bankflow
   DB_NAME=banking_workflow
   VOYAGE_API_KEY=your-voyage-ai-key
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit http://127.0.0.1:8000/ in your browser.

## Project Structure

```
banking/                  # Main application
├── models.py            # BankingDocument & WorkflowTask models
├── views.py             # View functions for all pages
├── forms.py             # Django forms
├── urls.py              # URL routing
├── admin.py             # Admin configuration
├── services/
│   ├── embedding_service.py      # Voyage AI embeddings
│   ├── vector_search_service.py  # MongoDB Atlas Vector Search
│   └── rag_service.py            # RAG pipeline
└── templates/banking/   # HTML templates
```

## Branches

- **`main`** — Complete solution with all features implemented
- **`starter`** — Skeleton with TODOs for the codealong

## Atlas Vector Search Index

Create this index on the `banking_bankingdocument` collection in your Atlas cluster.

**Index name:** `banking_embedding_index`

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1024,
      "similarity": "cosine"
    }
  ]
}
```


## UI Screenshot:

<img width="2547" height="1244" alt="image" src="https://github.com/user-attachments/assets/dc9abdd6-6ede-40e9-a406-6df7216d8f62" />
