"""Tests for Book and User models."""

from datetime import datetime

import pytest

from library_management.models import Book, User


class TestBook:
    """Test Book model."""

    def test_book_creation(self):
        """Test creating a book with all fields."""
        book = Book(
            book_id=1,
            title="The Hobbit",
            author="J.R.R. Tolkien",
            genre="Fantasy",
            average_rating=4.5,
            isbn="978-0547928227",
            language_code="en",
            rating_count=1000,
            available=True,
        )
        assert book.book_id == 1
        assert book.title == "The Hobbit"
        assert book.author == "J.R.R. Tolkien"
        assert book.genre == "Fantasy"
        assert book.average_rating == 4.5
        assert book.isbn == "978-0547928227"
        assert book.language_code == "en"
        assert book.rating_count == 1000
        assert book.available is True

    def test_book_creation_minimal(self):
        """Test creating a book with only required fields."""
        book = Book(book_id=1, title="Test Book", author="Test Author")
        assert book.book_id == 1
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.genre is None
        assert book.available is True  # Default value

    def test_book_str(self):
        """Test string representation of book."""
        book = Book(
            book_id=1,
            title="The Hobbit",
            author="J.R.R. Tolkien",
            genre="Fantasy",
            available=True,
        )
        str_repr = str(book)
        assert "The Hobbit" in str_repr
        assert "J.R.R. Tolkien" in str_repr
        assert "Fantasy" in str_repr
        assert "Available" in str_repr

    def test_book_reserve(self):
        """Test reserving a book."""
        book = Book(book_id=1, title="Test", author="Author", available=True)
        assert book.available is True
        result = book.reserve()
        assert result is True
        assert book.available is False

    def test_book_reserve_unavailable(self):
        """Test reserving an unavailable book."""
        book = Book(book_id=1, title="Test", author="Author", available=False)
        assert book.available is False
        result = book.reserve()
        assert result is False
        assert book.available is False

    def test_book_return(self):
        """Test returning a book."""
        book = Book(book_id=1, title="Test", author="Author", available=False)
        assert book.available is False
        book.return_book()
        assert book.available is True


class TestUser:
    """Test User model."""

    def test_user_creation(self):
        """Test creating a user with all fields."""
        user = User(
            first_name="John",
            last_name="Doe",
            phone_num="123-456-7890",
            email="john@example.com",
            address="123 Main St",
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.phone_num == "123-456-7890"
        assert user.email == "john@example.com"
        assert user.address == "123 Main St"
        assert isinstance(user.created_at, datetime)

    def test_user_creation_minimal(self):
        """Test creating a user with only required fields."""
        user = User(first_name="Jane", last_name="Smith")
        assert user.first_name == "Jane"
        assert user.last_name == "Smith"
        assert user.phone_num is None
        assert user.email is None
        assert user.address is None
        assert isinstance(user.created_at, datetime)

    def test_user_str(self):
        """Test string representation of user."""
        user = User(
            first_name="John",
            last_name="Doe",
            phone_num="123-456-7890",
            email="john@example.com",
        )
        str_repr = str(user)
        assert "John" in str_repr
        assert "Doe" in str_repr
        assert "123-456-7890" in str_repr
        assert "john@example.com" in str_repr

    def test_user_str_no_contact(self):
        """Test string representation with no contact info."""
        user = User(first_name="Jane", last_name="Smith")
        str_repr = str(user)
        assert "Jane" in str_repr
        assert "Smith" in str_repr
        assert "N/A" in str_repr

