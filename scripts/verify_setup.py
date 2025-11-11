#!/usr/bin/env python
"""Quick verification script to test the library management setup."""

import sys
from pathlib import Path

# Add parent directory to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from library_management import LibrarySystem, Book, User, load_books_from_csv
    from library_management.database import LibraryDatabase
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test basic functionality
try:
    # Test in-memory mode
    library = LibrarySystem()
    book = Book(book_id=1, title="Test Book", author="Test Author")
    library.add_book(book)
    assert len(library.list_books()) == 1
    print("✓ In-memory library system works")

    # Test database mode
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        library_db = LibrarySystem(db_path=str(db_path))
        library_db.add_book(book)
        assert len(library_db.list_books()) == 1
    print("✓ Database library system works")

    # Test User
    user = User(first_name="John", last_name="Doe")
    library.add_user(user)
    assert len(library.list_users()) == 1
    print("✓ User management works")

    print("\n✅ All basic tests passed!")
    print("✅ Setup is correct!")

except Exception as e:
    print(f"✗ Error during testing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

