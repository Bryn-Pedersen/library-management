from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional, Union

from .models import Book, User


class LibraryDatabase:
    """SQLite database backend for the library management system."""

    def __init__(self, db_path: Union[str, Path] = "library.db") -> None:
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self) -> None:
        """Initialize database tables if they don't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Books table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    genre TEXT,
                    average_rating REAL,
                    isbn TEXT,
                    language_code TEXT,
                    rating_count INTEGER,
                    available INTEGER NOT NULL DEFAULT 1
                )
            """
            )
            # Users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone_num TEXT,
                    email TEXT,
                    address TEXT,
                    created_at TEXT NOT NULL
                )
            """
            )
            # Borrowed books tracking
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS borrowings (
                    borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    borrowed_at TEXT NOT NULL,
                    returned_at TEXT,
                    FOREIGN KEY (book_id) REFERENCES books(book_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """
            )
            conn.commit()

    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        """Get a database connection with proper error handling."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # Book operations
    def add_book(self, book: Book) -> None:
        """Add a book to the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO books 
                (book_id, title, author, genre, average_rating, isbn, language_code, rating_count, available)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    book.book_id,
                    book.title,
                    book.author,
                    book.genre,
                    book.average_rating,
                    book.isbn,
                    book.language_code,
                    book.rating_count,
                    1 if book.available else 0,
                ),
            )
            conn.commit()

    def get_book(self, book_id: int) -> Optional[Book]:
        """Get a book by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_book(row)
            return None

    def get_book_by_title(self, title: str) -> Optional[Book]:
        """Get a book by title (case-insensitive)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE LOWER(title) = LOWER(?)", (title.strip(),))
            row = cursor.fetchone()
            if row:
                return self._row_to_book(row)
            return None

    def list_books(self, available_only: bool = False) -> List[Book]:
        """List all books, optionally filtered by availability."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if available_only:
                cursor.execute("SELECT * FROM books WHERE available = 1")
            else:
                cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()
            return [self._row_to_book(row) for row in rows]

    def update_book(self, book: Book) -> None:
        """Update a book's information."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE books SET
                    title = ?, author = ?, genre = ?, average_rating = ?,
                    isbn = ?, language_code = ?, rating_count = ?, available = ?
                WHERE book_id = ?
            """,
                (
                    book.title,
                    book.author,
                    book.genre,
                    book.average_rating,
                    book.isbn,
                    book.language_code,
                    book.rating_count,
                    1 if book.available else 0,
                    book.book_id,
                ),
            )
            conn.commit()

    def delete_book(self, book_id: int) -> bool:
        """Delete a book by ID. Returns True if deleted, False if not found."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            conn.commit()
            return cursor.rowcount > 0

    def _row_to_book(self, row: sqlite3.Row) -> Book:
        """Convert a database row to a Book object."""
        return Book(
            book_id=row["book_id"],
            title=row["title"],
            author=row["author"],
            genre=row["genre"],
            average_rating=row["average_rating"],
            isbn=row["isbn"],
            language_code=row["language_code"],
            rating_count=row["rating_count"],
            available=bool(row["available"]),
        )

    # User operations
    def add_user(self, user: User) -> int:
        """Add a user to the database. Returns the user_id."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (first_name, last_name, phone_num, email, address, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    user.first_name,
                    user.last_name,
                    user.phone_num,
                    user.email,
                    user.address,
                    user.created_at.isoformat(),
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
            return None

    def list_users(self) -> List[User]:
        """List all users."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return [self._row_to_user(row) for row in rows]

    def _row_to_user(self, row: sqlite3.Row) -> User:
        """Convert a database row to a User object."""
        from datetime import datetime

        created_at_str = row["created_at"]
        created_at = datetime.fromisoformat(created_at_str) if created_at_str else datetime.utcnow()

        return User(
            first_name=row["first_name"],
            last_name=row["last_name"],
            phone_num=row["phone_num"],
            email=row["email"],
            address=row["address"],
            created_at=created_at,
        )

    # Borrowing operations
    def borrow_book(self, book_id: int, user_id: int) -> bool:
        """Record a book borrowing. Returns True if successful."""
        from datetime import datetime

        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Check if book is available
            cursor.execute("SELECT available FROM books WHERE book_id = ?", (book_id,))
            row = cursor.fetchone()
            if not row or not row["available"]:
                return False

            # Mark book as unavailable
            cursor.execute("UPDATE books SET available = 0 WHERE book_id = ?", (book_id,))
            # Record borrowing
            cursor.execute(
                """
                INSERT INTO borrowings (book_id, user_id, borrowed_at)
                VALUES (?, ?, ?)
            """,
                (book_id, user_id, datetime.utcnow().isoformat()),
            )
            conn.commit()
            return True

    def return_book(self, book_id: int, user_id: int) -> bool:
        """Record a book return. Returns True if successful."""
        from datetime import datetime

        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Find active borrowing
            cursor.execute(
                """
                SELECT borrowing_id FROM borrowings
                WHERE book_id = ? AND user_id = ? AND returned_at IS NULL
                ORDER BY borrowed_at DESC
                LIMIT 1
            """,
                (book_id, user_id),
            )
            row = cursor.fetchone()
            if not row:
                return False

            # Mark as returned
            cursor.execute(
                "UPDATE borrowings SET returned_at = ? WHERE borrowing_id = ?",
                (datetime.utcnow().isoformat(), row["borrowing_id"]),
            )
            # Mark book as available
            cursor.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
            conn.commit()
            return True

