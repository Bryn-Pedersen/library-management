"""Tests for database functionality."""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from library_management.database import LibraryDatabase
from library_management.models import Book, User


class TestLibraryDatabase:
    """Test LibraryDatabase functionality."""

    def test_init_database(self):
        """Test initializing a database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            assert db_path.exists()

    def test_add_book(self):
        """Test adding a book to the database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            book = Book(book_id=1, title="Test Book", author="Test Author")
            db.add_book(book)
            retrieved = db.get_book(1)
            assert retrieved is not None
            assert retrieved.title == "Test Book"
            assert retrieved.author == "Test Author"

    def test_get_book_by_title(self):
        """Test retrieving a book by title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            book = Book(book_id=1, title="The Hobbit", author="Tolkien")
            db.add_book(book)
            retrieved = db.get_book_by_title("The Hobbit")
            assert retrieved is not None
            assert retrieved.title == "The Hobbit"
            # Case insensitive
            retrieved2 = db.get_book_by_title("the hobbit")
            assert retrieved2 is not None

    def test_list_books(self):
        """Test listing all books."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            book1 = Book(book_id=1, title="Book 1", author="Author 1", available=True)
            book2 = Book(book_id=2, title="Book 2", author="Author 2", available=False)
            db.add_book(book1)
            db.add_book(book2)
            books = db.list_books()
            assert len(books) == 2

    def test_list_books_available_only(self):
        """Test listing only available books."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            book1 = Book(book_id=1, title="Book 1", author="Author 1", available=True)
            book2 = Book(book_id=2, title="Book 2", author="Author 2", available=False)
            db.add_book(book1)
            db.add_book(book2)
            books = db.list_books(available_only=True)
            assert len(books) == 1
            assert books[0].book_id == 1

    def test_update_book(self):
        """Test updating a book."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            book = Book(book_id=1, title="Old Title", author="Author")
            db.add_book(book)
            book.title = "New Title"
            db.update_book(book)
            retrieved = db.get_book(1)
            assert retrieved is not None
            assert retrieved.title == "New Title"

    def test_delete_book(self):
        """Test deleting a book."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            book = Book(book_id=1, title="Test", author="Author")
            db.add_book(book)
            deleted = db.delete_book(1)
            assert deleted is True
            retrieved = db.get_book(1)
            assert retrieved is None

    def test_add_user(self):
        """Test adding a user to the database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            user = User(first_name="John", last_name="Doe", email="john@example.com")
            user_id = db.add_user(user)
            assert user_id > 0
            retrieved = db.get_user(user_id)
            assert retrieved is not None
            assert retrieved.first_name == "John"
            assert retrieved.last_name == "Doe"

    def test_list_users(self):
        """Test listing all users."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            user1 = User(first_name="John", last_name="Doe")
            user2 = User(first_name="Jane", last_name="Smith")
            db.add_user(user1)
            db.add_user(user2)
            users = db.list_users()
            assert len(users) == 2

    def test_borrow_book(self):
        """Test borrowing a book."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            book = Book(book_id=1, title="Test", author="Author", available=True)
            user = User(first_name="John", last_name="Doe")
            db.add_book(book)
            user_id = db.add_user(user)
            result = db.borrow_book(1, user_id)
            assert result is True
            retrieved = db.get_book(1)
            assert retrieved is not None
            assert retrieved.available is False

    def test_borrow_unavailable_book(self):
        """Test borrowing an unavailable book."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            book = Book(book_id=1, title="Test", author="Author", available=False)
            user = User(first_name="John", last_name="Doe")
            db.add_book(book)
            user_id = db.add_user(user)
            result = db.borrow_book(1, user_id)
            assert result is False

    def test_return_book(self):
        """Test returning a book."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            db = LibraryDatabase(db_path=str(db_path))
            book = Book(book_id=1, title="Test", author="Author", available=True)
            user = User(first_name="John", last_name="Doe")
            db.add_book(book)
            user_id = db.add_user(user)
            db.borrow_book(1, user_id)
            result = db.return_book(1, user_id)
            assert result is True
            retrieved = db.get_book(1)
            assert retrieved is not None
            assert retrieved.available is True

