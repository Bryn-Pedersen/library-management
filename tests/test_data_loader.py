"""Tests for CSV data loader."""

import csv
import pytest
import tempfile
from pathlib import Path

from library_management import load_books_from_csv, Book


class TestDataLoader:
    """Test CSV data loading functionality."""

    def test_load_books_basic(self):
        """Test loading books from a basic CSV."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=["title", "author", "genre", "available"])
            writer.writeheader()
            writer.writerow({"title": "Book 1", "author": "Author 1", "genre": "Fiction", "available": "true"})
            writer.writerow({"title": "Book 2", "author": "Author 2", "genre": "Non-Fiction", "available": "false"})
            csv_path = f.name

        try:
            books = load_books_from_csv(csv_path)
            assert len(books) == 2
            assert books[0].title == "Book 1"
            assert books[0].author == "Author 1"
            assert books[0].genre == "Fiction"
            assert books[0].available is True
            assert books[1].title == "Book 2"
            assert books[1].available is False
        finally:
            Path(csv_path).unlink()

    def test_load_books_with_all_fields(self):
        """Test loading books with all optional fields."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "book_id",
                    "title",
                    "author",
                    "genre",
                    "average_rating",
                    "isbn",
                    "language_code",
                    "rating_count",
                    "available",
                ],
            )
            writer.writeheader()
            writer.writerow(
                {
                    "book_id": "1",
                    "title": "The Hobbit",
                    "author": "Tolkien",
                    "genre": "Fantasy",
                    "average_rating": "4.5",
                    "isbn": "978-0547928227",
                    "language_code": "en",
                    "rating_count": "1000",
                    "available": "true",
                }
            )
            csv_path = f.name

        try:
            books = load_books_from_csv(csv_path)
            assert len(books) == 1
            book = books[0]
            assert book.book_id == 1
            assert book.title == "The Hobbit"
            assert book.author == "Tolkien"
            assert book.genre == "Fantasy"
            assert book.average_rating == 4.5
            assert book.isbn == "978-0547928227"
            assert book.language_code == "en"
            assert book.rating_count == 1000
            assert book.available is True
        finally:
            Path(csv_path).unlink()

    def test_load_books_flexible_isbn(self):
        """Test loading books with different ISBN column names."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=["title", "author", "ISBN"])
            writer.writeheader()
            writer.writerow({"title": "Book 1", "author": "Author 1", "ISBN": "1234567890"})
            csv_path = f.name

        try:
            books = load_books_from_csv(csv_path)
            assert len(books) == 1
            assert books[0].isbn == "1234567890"
        finally:
            Path(csv_path).unlink()

    def test_load_books_skips_invalid_rows(self):
        """Test that rows without title or author are skipped."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=["title", "author", "genre"])
            writer.writeheader()
            writer.writerow({"title": "Book 1", "author": "Author 1", "genre": "Fiction"})
            writer.writerow({"title": "", "author": "Author 2", "genre": "Non-Fiction"})
            writer.writerow({"title": "Book 3", "author": "", "genre": "Fiction"})
            writer.writerow({"title": "Book 4", "author": "Author 4", "genre": "Fiction"})
            csv_path = f.name

        try:
            books = load_books_from_csv(csv_path)
            assert len(books) == 2  # Only valid rows
            assert books[0].title == "Book 1"
            assert books[1].title == "Book 4"
        finally:
            Path(csv_path).unlink()

    def test_load_books_auto_increment_id(self):
        """Test that book IDs are auto-incremented when not provided."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=["title", "author"])
            writer.writeheader()
            writer.writerow({"title": "Book 1", "author": "Author 1"})
            writer.writerow({"title": "Book 2", "author": "Author 2"})
            csv_path = f.name

        try:
            books = load_books_from_csv(csv_path, starting_id=10)
            assert len(books) == 2
            assert books[0].book_id == 10
            assert books[1].book_id == 11
        finally:
            Path(csv_path).unlink()

    def test_load_books_bool_parsing(self):
        """Test parsing of boolean values in various formats."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=["title", "author", "available"])
            writer.writeheader()
            writer.writerow({"title": "Book 1", "author": "Author 1", "available": "True"})
            writer.writerow({"title": "Book 2", "author": "Author 2", "available": "yes"})
            writer.writerow({"title": "Book 3", "author": "Author 3", "available": "1"})
            writer.writerow({"title": "Book 4", "author": "Author 4", "available": "false"})
            writer.writerow({"title": "Book 5", "author": "Author 5", "available": "no"})
            writer.writerow({"title": "Book 6", "author": "Author 6", "available": "0"})
            csv_path = f.name

        try:
            books = load_books_from_csv(csv_path)
            assert len(books) == 6
            assert books[0].available is True
            assert books[1].available is True
            assert books[2].available is True
            assert books[3].available is False
            assert books[4].available is False
            assert books[5].available is False
        finally:
            Path(csv_path).unlink()

