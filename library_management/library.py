from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence, Union

from .models import Book, User

try:
    from .database import LibraryDatabase
except ImportError:
    LibraryDatabase = None  # type: ignore


class LibrarySystem:
    """Library management system with optional database persistence."""

    def __init__(self, db_path: Optional[Union[str, Path]] = None) -> None:
        """
        Initialize the library system.

        Args:
            db_path: If provided, use SQLite database for persistence.
                     If None, use in-memory storage only.
        """
        self._use_db = db_path is not None and LibraryDatabase is not None
        if self._use_db:
            self.db = LibraryDatabase(db_path)
            self._books: List[Book] = []
            self._users: List[User] = []
        else:
            self.books: List[Book] = []
            self.users: List[User] = []
            self.db = None

    def add_book(self, book: Book) -> None:
        """Add a book to the library."""
        if self._use_db and self.db:
            self.db.add_book(book)
        else:
            self.books.append(book)

    def add_user(self, user: User) -> int:
        """
        Add a user to the library.

        Returns:
            user_id if using database, 0 otherwise
        """
        if self._use_db and self.db:
            return self.db.add_user(user)
        else:
            self.users.append(user)
            return 0

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by title (case-insensitive)."""
        if self._use_db and self.db:
            return self.db.get_book_by_title(title)
        title_lower = title.strip().lower()
        for book in self.books:
            if book.title.strip().lower() == title_lower:
                return book
        return None

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        """Find a book by ID."""
        if self._use_db and self.db:
            return self.db.get_book(book_id)
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def list_books(self, available_only: bool = False) -> Sequence[Book]:
        """List all books, optionally filtered by availability."""
        if self._use_db and self.db:
            return self.db.list_books(available_only=available_only)
        if available_only:
            return tuple(book for book in self.books if book.available)
        return tuple(self.books)

    def list_users(self) -> Sequence[User]:
        """List all users."""
        if self._use_db and self.db:
            return self.db.list_users()
        return tuple(self.users)

    def update_book(self, book: Book) -> None:
        """Update a book's information."""
        if self._use_db and self.db:
            self.db.update_book(book)
        else:
            # In-memory: find and update
            for i, b in enumerate(self.books):
                if b.book_id == book.book_id:
                    self.books[i] = book
                    break

    def delete_book(self, book_id: int) -> bool:
        """Delete a book by ID. Returns True if deleted."""
        if self._use_db and self.db:
            return self.db.delete_book(book_id)
        for i, book in enumerate(self.books):
            if book.book_id == book_id:
                del self.books[i]
                return True
        return False

    def borrow_book(self, book_id: int, user_id: int) -> bool:
        """
        Borrow a book for a user. Requires database.

        Returns:
            True if successful, False otherwise
        """
        if self._use_db and self.db:
            return self.db.borrow_book(book_id, user_id)
        # In-memory: simple availability check
        book = self.find_book_by_id(book_id)
        if book and book.available:
            book.available = False
            return True
        return False

    def return_book_by_id(self, book_id: int, user_id: int) -> bool:
        """
        Return a book. Requires database for full tracking.

        Returns:
            True if successful, False otherwise
        """
        if self._use_db and self.db:
            return self.db.return_book(book_id, user_id)
        # In-memory: simple return
        book = self.find_book_by_id(book_id)
        if book:
            book.available = True
            return True
        return False
