"""Tests for LibrarySystem."""

import pytest
import tempfile
from pathlib import Path

from library_management import LibrarySystem, Book, User


class TestLibrarySystemInMemory:
    """Test LibrarySystem without database."""

    def test_init(self):
        """Test initializing library system."""
        library = LibrarySystem()
        assert len(library.list_books()) == 0
        assert len(library.list_users()) == 0

    def test_add_book(self):
        """Test adding a book."""
        library = LibrarySystem()
        book = Book(book_id=1, title="Test Book", author="Test Author")
        library.add_book(book)
        assert len(library.list_books()) == 1
        assert library.list_books()[0] == book

    def test_add_user(self):
        """Test adding a user."""
        library = LibrarySystem()
        user = User(first_name="John", last_name="Doe")
        library.add_user(user)
        assert len(library.list_users()) == 1
        assert library.list_users()[0] == user

    def test_find_book_by_title(self):
        """Test finding a book by title."""
        library = LibrarySystem()
        book = Book(book_id=1, title="The Hobbit", author="Tolkien")
        library.add_book(book)
        found = library.find_book_by_title("The Hobbit")
        assert found == book
        found_case = library.find_book_by_title("the hobbit")
        assert found_case == book

    def test_find_book_by_title_not_found(self):
        """Test finding a book that doesn't exist."""
        library = LibrarySystem()
        found = library.find_book_by_title("Nonexistent")
        assert found is None

    def test_find_book_by_id(self):
        """Test finding a book by ID."""
        library = LibrarySystem()
        book = Book(book_id=1, title="Test", author="Author")
        library.add_book(book)
        found = library.find_book_by_id(1)
        assert found == book

    def test_list_books_available_only(self):
        """Test listing only available books."""
        library = LibrarySystem()
        book1 = Book(book_id=1, title="Available", author="Author", available=True)
        book2 = Book(book_id=2, title="Unavailable", author="Author", available=False)
        library.add_book(book1)
        library.add_book(book2)
        available = library.list_books(available_only=True)
        assert len(available) == 1
        assert available[0] == book1

    def test_update_book(self):
        """Test updating a book."""
        library = LibrarySystem()
        book = Book(book_id=1, title="Old Title", author="Author")
        library.add_book(book)
        book.title = "New Title"
        library.update_book(book)
        found = library.find_book_by_id(1)
        assert found is not None
        assert found.title == "New Title"

    def test_delete_book(self):
        """Test deleting a book."""
        library = LibrarySystem()
        book = Book(book_id=1, title="Test", author="Author")
        library.add_book(book)
        assert len(library.list_books()) == 1
        deleted = library.delete_book(1)
        assert deleted is True
        assert len(library.list_books()) == 0

    def test_delete_book_not_found(self):
        """Test deleting a book that doesn't exist."""
        library = LibrarySystem()
        deleted = library.delete_book(999)
        assert deleted is False

    def test_borrow_book_in_memory(self):
        """Test borrowing a book in memory mode."""
        library = LibrarySystem()
        book = Book(book_id=1, title="Test", author="Author", available=True)
        library.add_book(book)
        result = library.borrow_book(1, 1)
        assert result is True
        found = library.find_book_by_id(1)
        assert found is not None
        assert found.available is False

    def test_return_book_by_id_in_memory(self):
        """Test returning a book in memory mode."""
        library = LibrarySystem()
        book = Book(book_id=1, title="Test", author="Author", available=False)
        library.add_book(book)
        result = library.return_book_by_id(1, 1)
        assert result is True
        found = library.find_book_by_id(1)
        assert found is not None
        assert found.available is True


class TestLibrarySystemDatabase:
    """Test LibrarySystem with database."""

    def test_init_with_db(self):
        """Test initializing library system with database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            library = LibrarySystem(db_path=str(db_path))
            assert len(library.list_books()) == 0
            assert len(library.list_users()) == 0

    def test_add_book_to_db(self):
        """Test adding a book to database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            library = LibrarySystem(db_path=str(db_path))
            book = Book(book_id=1, title="Test Book", author="Test Author")
            library.add_book(book)
            assert len(library.list_books()) == 1
            # Verify persistence
            library2 = LibrarySystem(db_path=str(db_path))
            assert len(library2.list_books()) == 1

    def test_add_user_to_db(self):
        """Test adding a user to database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            library = LibrarySystem(db_path=str(db_path))
            user = User(first_name="John", last_name="Doe")
            user_id = library.add_user(user)
            assert user_id > 0
            assert len(library.list_users()) == 1

    def test_find_book_in_db(self):
        """Test finding a book in database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            library = LibrarySystem(db_path=str(db_path))
            book = Book(book_id=1, title="The Hobbit", author="Tolkien")
            library.add_book(book)
            found = library.find_book_by_title("The Hobbit")
            assert found is not None
            assert found.title == "The Hobbit"

    def test_borrow_book_in_db(self):
        """Test borrowing a book with database tracking."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            library = LibrarySystem(db_path=str(db_path))
            book = Book(book_id=1, title="Test", author="Author", available=True)
            user = User(first_name="John", last_name="Doe")
            library.add_book(book)
            user_id = library.add_user(user)
            result = library.borrow_book(1, user_id)
            assert result is True
            found = library.find_book_by_id(1)
            assert found is not None
            assert found.available is False

    def test_return_book_in_db(self):
        """Test returning a book with database tracking."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            library = LibrarySystem(db_path=str(db_path))
            book = Book(book_id=1, title="Test", author="Author", available=True)
            user = User(first_name="John", last_name="Doe")
            library.add_book(book)
            user_id = library.add_user(user)
            library.borrow_book(1, user_id)
            result = library.return_book_by_id(1, user_id)
            assert result is True
            found = library.find_book_by_id(1)
            assert found is not None
            assert found.available is True

