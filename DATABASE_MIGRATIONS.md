# Database Migrations Guide

This guide explains how to use Alembic for database migrations in the AI Chatbot application.

## Overview

Alembic is a database migration tool for SQLAlchemy. It tracks changes to your database schema over time, allowing you to:

- Create versioned database schema changes
- Apply migrations to upgrade your database
- Rollback migrations if needed
- Maintain consistency across development, staging, and production environments

## Prerequisites

Alembic is already installed as part of the project dependencies (see `backend/requirements.txt`).

Ensure you have:
- PostgreSQL running (default: `localhost:5432`)
- Database configured in `.env` file or using the default `DATABASE_URL` from `backend/app/utils/config.py`

## Directory Structure

```
backend/
├── alembic/
│   ├── versions/          # Migration files
│   │   └── 001_initial_schema.py
│   ├── env.py            # Alembic environment configuration
│   ├── script.py.mako    # Template for new migrations
│   └── README
├── alembic.ini           # Alembic configuration file
└── app/
    └── models/
        └── database.py   # SQLAlchemy models
```

## Configuration

### alembic.ini

The main configuration file (`backend/alembic.ini`) controls Alembic's behavior. Key settings:

- `script_location`: Points to the `alembic/` directory containing migrations
- `sqlalchemy.url`: Database connection string (automatically set from `settings.DATABASE_URL`)

### env.py

The environment file (`backend/alembic/env.py`) configures how migrations run:

- Imports `Base` from `app.models.database`
- Imports all model classes to ensure they're registered
- Uses `settings.DATABASE_URL` from application config
- Sets `target_metadata = Base.metadata` for autogeneration

## Common Migration Commands

All commands should be run from the `backend/` directory:

```bash
cd backend
```

### Check Current Migration Status

```bash
alembic current
```

Shows which migration version is currently applied to the database.

### View Migration History

```bash
alembic history --verbose
```

Lists all available migrations with details.

### Apply Migrations (Upgrade)

```bash
# Upgrade to the latest version
alembic upgrade head

# Upgrade by one version
alembic upgrade +1

# Upgrade to a specific revision
alembic upgrade 001
```

### Rollback Migrations (Downgrade)

```bash
# Downgrade by one version
alembic downgrade -1

# Downgrade to a specific revision
alembic downgrade 001

# Downgrade all migrations (back to empty database)
alembic downgrade base
```

### Create New Migration

#### Auto-generate migration from model changes

```bash
alembic revision --autogenerate -m "Description of changes"
```

Alembic will compare the current database state with your SQLAlchemy models and generate migration code automatically.

**Important:** Always review auto-generated migrations before applying them!

#### Create empty migration file

```bash
alembic revision -m "Description of changes"
```

Creates a blank migration template for manual changes.

### View SQL Without Applying

```bash
# See SQL for next upgrade
alembic upgrade head --sql

# See SQL for downgrade
alembic downgrade -1 --sql
```

## Initial Setup (First Time)

If setting up the database for the first time:

1. **Ensure PostgreSQL is running:**
   ```bash
   # Check if PostgreSQL is running
   psql -U chatbot -d chatbot_db -c "SELECT version();"
   ```

2. **Create database if it doesn't exist:**
   ```bash
   createdb chatbot_db -U chatbot
   ```

3. **Apply initial migration:**
   ```bash
   cd backend
   alembic upgrade head
   ```

4. **Verify tables were created:**
   ```bash
   psql -U chatbot -d chatbot_db -c "\dt"
   ```

   You should see tables: `users`, `documents`, `chat_sessions`, `chat_messages`, `authors`, `posts`, and `alembic_version`.

## Migration File Structure

Each migration file contains:

### Metadata
```python
revision = '001'           # Unique identifier
down_revision = None       # Previous migration (None for first)
branch_labels = None       # For branching (rarely used)
depends_on = None          # Dependencies on other migrations
```

### upgrade() function
Defines how to apply the migration (create tables, add columns, etc.)

### downgrade() function
Defines how to reverse the migration (drop tables, remove columns, etc.)

## Current Migrations

### 001_initial_schema.py

Creates the complete initial database schema including:

**User Management:**
- `users` table - User accounts with authentication
- `documents` table - Uploaded documents with processing status

**Chat System:**
- `chat_sessions` table - Conversation sessions
- `chat_messages` table - Individual messages in sessions

**Blog System:**
- `authors` table - Blog post authors with profiles
- `posts` table - Blog posts with metadata (status, tags, category)

**Relationships:**
- Users own documents and chat sessions
- Chat sessions contain messages
- Authors create posts

**Indexes:**
- Unique constraints on usernames and emails
- Foreign key indexes for efficient joins
- Status and timestamp indexes for queries

## Best Practices

### 1. Always Review Auto-generated Migrations

```bash
# After generating a migration
alembic revision --autogenerate -m "Add user preferences"

# Review the file before applying
cat alembic/versions/*_add_user_preferences.py
```

Alembic's autogenerate is helpful but not perfect. It may miss:
- Renamed columns (appears as drop + add)
- Changed constraints
- Custom SQL or data migrations

### 2. Test Migrations Locally First

```bash
# Apply migration
alembic upgrade head

# Test application functionality
pytest

# Test rollback
alembic downgrade -1
alembic upgrade head
```

### 3. Use Descriptive Migration Messages

```bash
# Good
alembic revision -m "Add user_preferences table with theme and language"

# Bad
alembic revision -m "Update database"
```

### 4. Keep Migrations Small and Focused

Create separate migrations for different features:
```bash
alembic revision -m "Add user email verification fields"
alembic revision -m "Add post comments table"
```

Rather than one large migration:
```bash
alembic revision -m "Add lots of stuff"
```

### 5. Never Modify Applied Migrations

Once a migration has been applied to production, create a new migration instead of modifying the old one.

### 6. Backup Before Major Migrations

```bash
# PostgreSQL backup
pg_dump chatbot_db > backup_$(date +%Y%m%d).sql

# Apply migration
alembic upgrade head
```

## Workflow Examples

### Adding a New Model

1. **Add model to `app/models/database.py`:**
   ```python
   class Comment(Base):
       __tablename__ = "comments"
       id = Column(Integer, primary_key=True)
       content = Column(Text, nullable=False)
       post_id = Column(Integer, ForeignKey("posts.id"))
   ```

2. **Generate migration:**
   ```bash
   cd backend
   alembic revision --autogenerate -m "Add comments table"
   ```

3. **Review migration file:**
   ```bash
   cat alembic/versions/*_add_comments_table.py
   ```

4. **Apply migration:**
   ```bash
   alembic upgrade head
   ```

### Modifying an Existing Column

1. **Update model:**
   ```python
   # Change in database.py
   bio = Column(Text)  # was Column(String(500))
   ```

2. **Generate migration:**
   ```bash
   alembic revision --autogenerate -m "Increase author bio length"
   ```

3. **Review and apply:**
   ```bash
   cat alembic/versions/*_increase_author_bio_length.py
   alembic upgrade head
   ```

### Data Migration

For migrations that modify data (not just schema):

1. **Create empty migration:**
   ```bash
   alembic revision -m "Migrate old post format to new format"
   ```

2. **Edit migration to include data changes:**
   ```python
   def upgrade() -> None:
       # Schema change
       op.add_column('posts', sa.Column('excerpt', sa.String(500)))

       # Data migration
       connection = op.get_bind()
       connection.execute(
           text("UPDATE posts SET excerpt = LEFT(content, 200)")
       )
   ```

3. **Apply migration:**
   ```bash
   alembic upgrade head
   ```

## Troubleshooting

### "Target database is not up to date"

Your database is behind the latest migration.

**Solution:**
```bash
alembic upgrade head
```

### "Can't locate revision identified by '...'"

Migration file is missing or corrupted.

**Solution:**
```bash
# Check what's in the database
alembic current

# Check available migrations
alembic history

# If mismatch, may need to stamp the current version
alembic stamp head
```

### Autogenerate Doesn't Detect Changes

Ensure models are imported in `env.py`:

**Solution:**
Check `backend/alembic/env.py` imports all models:
```python
from app.models.database import (
    User, Document, ChatSession, ChatMessage, Author, Post
)
```

### PostgreSQL Connection Error

Database URL may be incorrect.

**Solution:**
```bash
# Check DATABASE_URL in .env or config
cd backend
python -c "from app.utils.config import settings; print(settings.DATABASE_URL)"
```

### Migration Conflicts

Multiple developers creating migrations simultaneously.

**Solution:**
```bash
# Merge migrations using Alembic merge
alembic merge -m "Merge migrations" revision1 revision2
```

## Integration with Application

### Current Approach

The application currently uses `init_db()` in `backend/app/services/database.py` which calls `Base.metadata.create_all()`. This creates tables directly from models.

### Migrating to Alembic-Only Approach

To fully adopt Alembic migrations:

1. **Remove or deprecate `init_db()` usage**
2. **Update application startup to check migrations:**

```python
# In main.py or startup script
from alembic.config import Config
from alembic import command

def check_migrations():
    alembic_cfg = Config("alembic.ini")
    command.current(alembic_cfg)
    # Optionally auto-upgrade
    # command.upgrade(alembic_cfg, "head")
```

3. **Document that developers should run migrations manually**

## CI/CD Integration

### Running Migrations in Docker

Update `docker-compose.yml` or startup scripts:

```yaml
services:
  backend:
    command: sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0"
```

### GitHub Actions Example

```yaml
- name: Run migrations
  run: |
    cd backend
    alembic upgrade head
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Seeding Sample Data

After applying migrations, you can populate the database with sample blog data for development and testing.

### Blog System Seed Script

The `backend/app/scripts/seed_blog_data.py` script creates sample authors and blog posts.

**Features:**
- Creates 5 sample authors with realistic profiles
- Creates 10 sample blog posts across various categories
- Includes both published posts and drafts
- Safe to run multiple times (checks for existing data)
- Includes diverse content: tutorials, technical articles, and best practices

### Running the Seed Script

```bash
cd backend
python -m app.scripts.seed_blog_data
```

**Expected Output:**
```
============================================================
Blog System Seed Data Script
============================================================

Current database state:
  - Authors: 0
  - Posts: 0

Seeding authors...
------------------------------------------------------------
Created author: Sarah Chen
Created author: Marcus Rodriguez
Created author: Aisha Patel
Created author: James O'Connor
Created author: Luna Kim

Seeding posts...
------------------------------------------------------------
Created post: Building a Full-Stack AI Chatbot with FastAPI and React
Created post: Understanding Retrieval-Augmented Generation (RAG)
Created post: Containerizing Your FastAPI Application with Docker
Created post: Database Design for Chat Applications
Created post: Best Practices for JWT Authentication in FastAPI
Created post: Creating Accessible React Components
Created post: Optimizing Vector Search with ChromaDB
Created post: Database Migrations with Alembic
Created post: CI/CD Pipelines for Python Applications
Created post: TypeScript Best Practices for React Projects

============================================================
Seeding completed!
Final database state:
  - Authors: 5
  - Posts: 10
============================================================
```

### Sample Data Details

**Authors:**
- Sarah Chen - Full-stack developer
- Marcus Rodriguez - AI/ML engineer
- Aisha Patel - DevOps specialist
- James O'Connor - Database architect
- Luna Kim - UX engineer

**Posts:**
The seed data includes 10 posts covering:
- **Published Posts (7)**: Ready to display on the blog
  - FastAPI and React chatbot tutorial
  - RAG explanation
  - Docker containerization
  - Database design
  - JWT authentication
  - React accessibility
  - TypeScript best practices

- **Draft Posts (3)**: For testing draft functionality
  - ChromaDB optimization
  - Alembic migrations
  - CI/CD pipelines

**Categories:**
- Tutorials
- AI/ML
- DevOps
- Database
- Security
- Frontend

**Tags:**
Each post includes relevant tags (e.g., `python,fastapi,react,ai,chatbot`)

### Running Seed Script in Docker

Add to your Docker startup script or run manually:

```bash
# In docker-compose.yml or startup script
docker-compose exec backend python -m app.scripts.seed_blog_data
```

Or include in the backend service command:

```yaml
services:
  backend:
    command: sh -c "alembic upgrade head && python -m app.scripts.seed_blog_data && uvicorn app.main:app --host 0.0.0.0"
```

### Verifying Seed Data

Check the data was created:

```bash
# Using psql
psql -U chatbot -d chatbot_db -c "SELECT name, email FROM authors;"
psql -U chatbot -d chatbot_db -c "SELECT title, status, category FROM posts;"

# Using Python
cd backend
python -c "
from app.services.database import SessionLocal
from app.models.database import Author, Post

db = SessionLocal()
print(f'Authors: {db.query(Author).count()}')
print(f'Posts: {db.query(Post).count()}')
print(f'Published: {db.query(Post).filter(Post.status == \"published\").count()}')
print(f'Drafts: {db.query(Post).filter(Post.status == \"draft\").count()}')
"
```

### Resetting Seed Data

To remove seed data and reseed:

```bash
# Delete existing data
psql -U chatbot -d chatbot_db -c "TRUNCATE posts, authors RESTART IDENTITY CASCADE;"

# Reseed
python -m app.scripts.seed_blog_data
```

**Warning:** This will delete all blog data. Use with caution in development only.

### Customizing Seed Data

To modify the seed data:

1. Edit `backend/app/scripts/seed_blog_data.py`
2. Update the `authors_data` list to change author information
3. Update the `posts_data` list to change blog posts
4. Run the script to add your custom data

**Example:**
```python
# Add a new author
{
    "name": "Your Name",
    "email": "your.email@example.com",
    "bio": "Your bio here",
    "profile_picture_url": "https://i.pravatar.cc/150?img=10"
}
```

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- Project configuration: `backend/app/utils/config.py`
- Model definitions: `backend/app/models/database.py`
- Seed script: `backend/app/scripts/seed_blog_data.py`

## Support

For issues or questions:
1. Check this documentation
2. Review Alembic logs: `alembic.log` (if logging configured)
3. Examine migration files in `backend/alembic/versions/`
4. Check database state: `alembic current` and `alembic history`
