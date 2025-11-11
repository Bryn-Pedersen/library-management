from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Book:
    book_id: int
    title: str
    author: str
    genre: Optional[str] = None
    average_rating: Optional[float] = None
    isbn: Optional[str] = None
    language_code: Optional[str] = None
    rating_count: Optional[int] = None
    available: bool = True

    def __str__(self) -> str:
        status = "Available" if self.available else "Not Available"
        genre = self.genre or "Unknown"
        return f"'{self.title}' by {self.author} | Genre: {genre} | Status: {status}"

    def reserve(self) -> bool:
        if self.available:
            self.available = False
            return True
        return False

    def return_book(self) -> None:
        self.available = True


@dataclass
class User:
    first_name: str
    last_name: str
    phone_num: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __str__(self) -> str:
        phone = self.phone_num or "N/A"
        email = self.email or "N/A"
        return f"User: {self.first_name} {self.last_name} | Contact: {phone} / {email}"


