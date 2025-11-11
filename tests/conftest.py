"""Pytest configuration and shared fixtures."""

import pytest
import tempfile
from pathlib import Path

from library_management import LibrarySystem, Book, User


@pytest.fixture
def sample_book():
    """Create a sample book for testing."""
    return Book(
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


@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(
        first_name="John",
        last_name="Doe",
        phone_num="123-456-7890",
        email="john@example.com",
        address="123 Main St",
    )


@pytest.fixture
def library_in_memory():
    """Create an in-memory library system."""
    return LibrarySystem()


@pytest.fixture
def library_with_db():
    """Create a library system with a temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        library = LibrarySystem(db_path=str(db_path))
        yield library

