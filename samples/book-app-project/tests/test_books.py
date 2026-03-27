import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection
from errors import NotFoundError, StorageError, ValidationError


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_search_books_by_title_partial_case_insensitive():
    collection = BookCollection()
    collection.add_book("The Pragmatic Programmer", "Andrew Hunt", 1999)
    collection.add_book("Clean Code", "Robert C. Martin", 2008)

    results = collection.search_books("prag", "title")

    assert len(results) == 1
    assert results[0].title == "The Pragmatic Programmer"


def test_search_books_by_author_partial_case_insensitive():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Neuromancer", "William Gibson", 1984)

    results = collection.search_books("HERB", "author")

    assert len(results) == 1
    assert results[0].author == "Frank Herbert"


def test_search_books_default_scope_both():
    collection = BookCollection()
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    results = collection.search_books("dune")

    assert len(results) == 1
    assert results[0].title == "Dune Messiah"


def test_search_books_no_match_returns_empty_list():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)

    results = collection.search_books("asimov")

    assert results == []


def test_add_book_raises_for_empty_title():
    collection = BookCollection()

    with pytest.raises(ValueError, match="title cannot be empty"):
        collection.add_book("   ", "George Orwell", 1949)


def test_add_book_raises_for_negative_year():
    collection = BookCollection()

    with pytest.raises(ValueError, match="year cannot be negative"):
        collection.add_book("1984", "George Orwell", -1)


def test_search_books_raises_for_invalid_field():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)

    with pytest.raises(ValueError, match="field must be 'title', 'author', or 'both'"):
        collection.search_books("1984", "publisher")


def test_add_rating_success_and_average():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.add_rating("Dune", 8) is True
    assert collection.add_rating("Dune", 10) is True
    assert collection.get_average_rating("Dune") == 9.0


def test_add_rating_invalid_value_raises():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    with pytest.raises(ValueError, match="rating must be between 1 and 10"):
        collection.add_rating("Dune", 11)


def test_add_review_and_get_reviews_with_multiple_entries():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.add_review("Dune", "Excellent pacing.") is True
    assert collection.add_review("Dune", "Loved the characters.") is True
    assert collection.get_reviews("Dune") == ["Excellent pacing.", "Loved the characters."]


def test_add_review_empty_raises():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    with pytest.raises(ValueError, match="review cannot be empty"):
        collection.add_review("Dune", "   ")


def test_load_books_backward_compatible_without_ratings_reviews(tmp_path, monkeypatch):
    legacy_data = '[{"title":"Legacy Book","author":"Anon","year":2000,"read":false}]'
    temp_file = tmp_path / "legacy.json"
    temp_file.write_text(legacy_data)
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    book = collection.find_book_by_title("Legacy Book")

    assert book is not None
    assert book.ratings == []
    assert book.reviews == []


@pytest.mark.parametrize("invalid_title", ["", "   ", None, 123])
def test_find_book_by_title_returns_none_for_invalid_inputs(invalid_title):
    collection = BookCollection()
    assert collection.find_book_by_title(invalid_title) is None


@pytest.mark.parametrize("invalid_author", ["", "   ", None, 123])
def test_find_by_author_returns_empty_for_invalid_inputs(invalid_author):
    collection = BookCollection()
    assert collection.find_by_author(invalid_author) == []


def test_search_books_returns_empty_for_blank_query():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    assert collection.search_books("   ", "both") == []


def test_search_books_raises_for_non_string_query():
    collection = BookCollection()
    with pytest.raises(ValidationError, match="query must be a string"):
        collection.search_books(None, "both")


def test_search_books_normalizes_field_value():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    results = collection.search_books("dune", " Title ")
    assert len(results) == 1
    assert results[0].title == "Dune"


def test_add_rating_raises_not_found_for_missing_book():
    collection = BookCollection()
    with pytest.raises(NotFoundError, match="book not found"):
        collection.add_rating("Missing", 8)


def test_add_review_raises_not_found_for_missing_book():
    collection = BookCollection()
    with pytest.raises(NotFoundError, match="book not found"):
        collection.add_review("Missing", "Great")


def test_get_average_rating_returns_none_for_missing_or_unrated_book():
    collection = BookCollection()
    assert collection.get_average_rating("Missing") is None

    collection.add_book("Dune", "Frank Herbert", 1965)
    assert collection.get_average_rating("Dune") is None


def test_load_books_raises_storage_error_for_corrupted_json(tmp_path, monkeypatch):
    temp_file = tmp_path / "broken.json"
    temp_file.write_text("{not-valid-json")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    with pytest.raises(StorageError, match="data.json is corrupted"):
        BookCollection()


def test_save_books_raises_storage_error_on_oserror(monkeypatch):
    collection = BookCollection()

    def raise_oserror(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr("builtins.open", raise_oserror)

    with pytest.raises(StorageError, match="failed to save data file"):
        collection.save_books()
