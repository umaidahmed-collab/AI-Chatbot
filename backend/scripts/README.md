# Database Scripts

This directory contains utility scripts for database management.

## Seed Blog Data

The `seed_blog_data.py` script populates the database with sample blog posts and authors for testing.

### Usage

```bash
# From the backend directory
cd backend
python scripts/seed_blog_data.py
```

Or run from the scripts directory:

```bash
cd backend/scripts
python seed_blog_data.py
```

### What it creates

- **3 Authors**: Jane Smith, John Doe, and Sarah Johnson
- **5 Blog Posts**: Various technical articles about FastAPI, RAG, Docker, Asyncio, and Microservices

### Note

The script will skip seeding if authors already exist in the database to prevent duplicates.
