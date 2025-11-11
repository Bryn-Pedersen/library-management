from __future__ import annotations

import csv
from typing import Iterable, List, Optional

from .models import Book


def _parse_bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if normalized in {"true", "yes", "1"}:
        return True
    if normalized in {"false", "no", "0"}:
        return False
    return None


def load_books_from_csv(file_path: str, starting_id: int = 1) -> List[Book]:
    """
    Load books from a CSV file. Tries to be flexible with headers.
    Required columns: title, author
    Optional columns: genre, average_rating, isbn/ISBN, language_code, rating_count, available, book_id
    """
    books: List[Book] = []
    next_id = starting_id
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = (row.get("title") or "").strip()
            author = (row.get("author") or "").strip()
            if not title or not author:
                continue

            # Flexible field handling
            isbn = (row.get("isbn") or row.get("ISBN") or "").strip() or None
            genre = (row.get("genre") or "").strip() or None
            language_code = (row.get("language_code") or "").strip() or None

            avg_rating_raw = row.get("average_rating")
            try:
                average_rating = float(avg_rating_raw) if avg_rating_raw not in (None, "") else None
            except ValueError:
                average_rating = None

            rating_count_raw = row.get("rating_count")
            try:
                rating_count = int(rating_count_raw) if rating_count_raw not in (None, "") else None
            except ValueError:
                rating_count = None

            available_parsed = _parse_bool(row.get("available"))
            available = True if available_parsed is None else available_parsed

            book_id_raw = row.get("book_id")
            try:
                book_id = int(book_id_raw) if book_id_raw not in (None, "") else next_id
            except ValueError:
                book_id = next_id

            books.append(
                Book(
                    book_id=book_id,
                    title=title,
                    author=author,
                    genre=genre,
                    average_rating=average_rating,
                    isbn=isbn,
                    language_code=language_code,
                    rating_count=rating_count,
                    available=available,
                )
            )
            next_id = max(next_id, book_id + 1)
    return books


