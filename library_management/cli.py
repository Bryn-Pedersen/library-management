"""Command-line interface for the library management system using Typer."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from . import LibrarySystem, load_books_from_csv
from .models import Book, User

app = typer.Typer(
    name="library",
    help="Library Management System CLI",
    add_completion=False,
)
console = Console()


def get_library(db_path: Optional[str] = None) -> LibrarySystem:
    """Get a library instance, optionally with database."""
    if db_path:
        return LibrarySystem(db_path=db_path)
    return LibrarySystem()


@app.command()
def load_csv(
    file: Path = typer.Argument(..., help="Path to CSV file"),
    db_path: Optional[str] = typer.Option(None, "--db", help="Path to SQLite database"),
) -> None:
    """Load books from a CSV file."""
    library = get_library(db_path)
    try:
        books = load_books_from_csv(str(file))
        for book in books:
            library.add_book(book)
        console.print(f"[green]✓[/green] Loaded {len(books)} books from {file}")
    except FileNotFoundError:
        console.print(f"[red]✗[/red] File not found: {file}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗[/red] Error loading CSV: {e}")
        raise typer.Exit(1)


@app.command()
def list_books(
    available_only: bool = typer.Option(False, "--available", "-a", help="Show only available books"),
    db_path: Optional[str] = typer.Option(None, "--db", help="Path to SQLite database"),
) -> None:
    """List all books in the library."""
    library = get_library(db_path)
    books = list(library.list_books(available_only=available_only))

    if not books:
        console.print("[yellow]No books found.[/yellow]")
        return

    table = Table(title="Books in Library", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Author", style="blue")
    table.add_column("Genre", style="yellow")
    table.add_column("Status", style="red")

    for book in books:
        status = "Available" if book.available else "Reserved"
        status_style = "green" if book.available else "red"
        table.add_row(
            str(book.book_id),
            book.title,
            book.author,
            book.genre or "N/A",
            f"[{status_style}]{status}[/{status_style}]",
        )

    console.print(table)
    console.print(f"\n[bold]Total: {len(books)} books[/bold]")


@app.command()
def reserve(
    title: str = typer.Argument(..., help="Book title"),
    db_path: Optional[str] = typer.Option(None, "--db", help="Path to SQLite database"),
) -> None:
    """Reserve a book by title."""
    library = get_library(db_path)
    book = library.find_book_by_title(title)

    if not book:
        console.print(f"[red]✗[/red] Book not found: {title}")
        raise typer.Exit(1)

    if book.reserve():
        library.update_book(book)
        console.print(f"[green]✓[/green] Reserved: {book.title}")
    else:
        console.print(f"[yellow]⚠[/yellow] Book already reserved: {book.title}")


@app.command()
def return_book(
    title: str = typer.Argument(..., help="Book title"),
    db_path: Optional[str] = typer.Option(None, "--db", help="Path to SQLite database"),
) -> None:
    """Return a book by title."""
    library = get_library(db_path)
    book = library.find_book_by_title(title)

    if not book:
        console.print(f"[red]✗[/red] Book not found: {title}")
        raise typer.Exit(1)

    book.return_book()
    library.update_book(book)
    console.print(f"[green]✓[/green] Returned: {book.title}")


@app.command()
def add_user(
    first_name: str = typer.Option(..., "--first", "-f", help="First name"),
    last_name: str = typer.Option(..., "--last", "-l", help="Last name"),
    phone: Optional[str] = typer.Option(None, "--phone", "-p", help="Phone number"),
    email: Optional[str] = typer.Option(None, "--email", "-e", help="Email address"),
    address: Optional[str] = typer.Option(None, "--address", "-a", help="Address"),
    db_path: Optional[str] = typer.Option(None, "--db", help="Path to SQLite database"),
) -> None:
    """Add a new user to the library."""
    library = get_library(db_path)
    user = User(
        first_name=first_name,
        last_name=last_name,
        phone_num=phone,
        email=email,
        address=address,
    )
    user_id = library.add_user(user)
    if user_id:
        console.print(f"[green]✓[/green] Added user (ID: {user_id}): {user}")
    else:
        console.print(f"[green]✓[/green] Added user: {user}")


@app.command()
def list_users(
    db_path: Optional[str] = typer.Option(None, "--db", help="Path to SQLite database"),
) -> None:
    """List all users in the library."""
    library = get_library(db_path)
    users = list(library.list_users())

    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Library Users", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="green")
    table.add_column("Phone", style="blue")
    table.add_column("Email", style="yellow")

    for user in users:
        table.add_row(
            f"{user.first_name} {user.last_name}",
            user.phone_num or "N/A",
            user.email or "N/A",
        )

    console.print(table)
    console.print(f"\n[bold]Total: {len(users)} users[/bold]")


@app.command()
def init_db(
    db_path: str = typer.Argument("library.db", help="Path to SQLite database file"),
) -> None:
    """Initialize a new SQLite database for the library."""
    from .database import LibraryDatabase

    try:
        db = LibraryDatabase(db_path)
        console.print(f"[green]✓[/green] Database initialized at: {db_path}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error initializing database: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

