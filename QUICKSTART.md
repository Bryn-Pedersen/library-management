# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd library-management

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e ".[dev]"
```

## Basic Usage

### Using the CLI

```bash
# Initialize a database
library init-db library.db

# Load books from CSV
library load-csv books.csv --db library.db

# List books
library list-books --db library.db

# Reserve a book
library reserve "The Hobbit" --db library.db

# Return a book
library return "The Hobbit" --db library.db

# Add a user
library add-user --first "John" --last "Doe" --email "john@example.com" --db library.db

# List users
library list-users --db library.db
```

### Using the Python API

```python
from library_management import LibrarySystem, Book, User

# Create library (in-memory or with database)
library = LibrarySystem()  # In-memory
# or
library = LibrarySystem(db_path="library.db")  # With database

# Add a book
book = Book(
    book_id=1,
    title="The Hobbit",
    author="J.R.R. Tolkien",
    genre="Fantasy",
    available=True
)
library.add_book(book)

# Add a user
user = User(first_name="John", last_name="Doe", email="john@example.com")
library.add_user(user)

# Find and reserve a book
book = library.find_book_by_title("The Hobbit")
if book:
    book.reserve()
    library.update_book(book)
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=library_management --cov-report=html

# Run specific test file
pytest tests/test_models.py
```

## Development

```bash
# Format code
black library_management tests

# Lint code
ruff check library_management tests

# Type check
mypy library_management
```

## Verify Setup

```bash
python scripts/verify_setup.py
```

This will verify that all imports work and basic functionality is operational.

