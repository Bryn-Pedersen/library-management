# Library Management System

A professional library management system with book and user tracking, CSV import/export, and SQLite database persistence.

## Features

- 📚 **Book Management**: Add, search, reserve, and return books
- 👥 **User Management**: Track library users with contact information
- 💾 **Database Persistence**: SQLite database for data storage
- 📊 **CSV Import**: Load books from CSV files
- 🎨 **Modern CLI**: Beautiful Typer-based command-line interface with Rich formatting
- 🧪 **Tested**: Comprehensive unit tests with pytest
- 🔄 **CI/CD**: GitHub Actions workflow for automated testing

## Installation

### From Source

1. Clone the repository:
```bash
git clone <your-repo-url>
cd library-management
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

Or install with dev dependencies:
```bash
pip install -e ".[dev]"
```

## Usage

### Command-Line Interface

After installation, you can use the `library` command:

```bash
# Initialize a database
library init-db library.db

# Load books from CSV
library load-csv books.csv --db library.db

# List all books
library list-books --db library.db

# List only available books
library list-books --available --db library.db

# Reserve a book
library reserve "The Hobbit" --db library.db

# Return a book
library return "The Hobbit" --db library.db

# Add a user
library add-user --first "John" --last "Doe" --email "john@example.com" --db library.db

# List users
library list-users --db library.db
```

### Python API

```python
from library_management import LibrarySystem, Book, User, load_books_from_csv

# In-memory mode (no database)
library = LibrarySystem()

# With database
library = LibrarySystem(db_path="library.db")

# Add a book
book = Book(
    book_id=1,
    title="The Hobbit",
    author="J.R.R. Tolkien",
    genre="Fantasy",
    average_rating=4.5,
    isbn="978-0547928227",
    available=True
)
library.add_book(book)

# Add a user
user = User(
    first_name="John",
    last_name="Doe",
    email="john@example.com"
)
library.add_user(user)

# Load books from CSV
books = load_books_from_csv("books.csv")
for book in books:
    library.add_book(book)

# Find and reserve a book
book = library.find_book_by_title("The Hobbit")
if book and book.available:
    book.reserve()
    library.update_book(book)

# List books
for book in library.list_books():
    print(book)
```

## CSV Format

The CSV loader is flexible and supports various column names. Required columns:
- `title`
- `author`

Optional columns:
- `book_id`
- `genre`
- `average_rating`
- `isbn` or `ISBN`
- `language_code`
- `rating_count`
- `available` (true/false, yes/no, 1/0)

Example CSV:
```csv
title,author,genre,available
The Hobbit,J.R.R. Tolkien,Fantasy,true
1984,George Orwell,Dystopian,true
```

## Database Schema

The SQLite database includes three tables:

1. **books**: Stores book information
2. **users**: Stores user information
3. **borrowings**: Tracks book borrowings and returns

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=library_management --cov-report=html

# Run specific test file
pytest tests/test_models.py
```

### Code Formatting

```bash
# Format code with black
black library_management tests

# Check with ruff
ruff check library_management tests

# Type checking with mypy
mypy library_management
```

### Installing Dev Dependencies

```bash
pip install -e ".[dev]"
```

## Project Structure

```
library-management/
├── library_management/     # Main package
│   ├── __init__.py
│   ├── models.py           # Book and User models
│   ├── library.py          # LibrarySystem class
│   ├── database.py         # SQLite database layer
│   ├── data_loader.py      # CSV loading functionality
│   └── cli.py              # Typer CLI interface
├── tests/                  # Unit tests
│   ├── test_models.py
│   ├── test_library.py
│   ├── test_database.py
│   └── test_data_loader.py
├── scripts/                # Utility scripts
│   └── generate_book_data.py
├── pyproject.toml          # Project configuration
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md
```

## CI/CD

The project includes GitHub Actions workflows that:
- Run tests on multiple Python versions (3.8-3.12)
- Run tests on multiple operating systems (Linux, macOS, Windows)
- Check code formatting and linting
- Generate coverage reports

## License

MIT License

## Author

Bryn Pedersen (brp@gmail.com)
