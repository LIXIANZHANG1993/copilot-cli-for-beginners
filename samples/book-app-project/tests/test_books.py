import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import Book, BookCollection
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


@pytest.mark.parametrize(
    "title, author, year",
    [
        ("  Dune  ", "Frank Herbert", 1965),
        ("Dune", "  Frank Herbert  ", 1965),
        ("  Dune  ", "  Frank Herbert  ", 1965),
    ],
)
def test_add_book_normalizes_title_and_author_whitespace(title, author, year):
    collection = BookCollection()

    created = collection.add_book(title, author, year)

    assert created.title == "Dune"
    assert created.author == "Frank Herbert"
    assert collection.find_book_by_title("Dune") is not None


@pytest.mark.parametrize(
    "title, author, year, error_message",
    [
        (None, "George Orwell", 1949, "title must be a string"),
        ("1984", None, 1949, "author must be a string"),
        ("1984", "George Orwell", True, "year must be an integer"),
        ("1984", "George Orwell", 1949.5, "year must be an integer"),
    ],
)
def test_add_book_raises_for_invalid_types(title, author, year, error_message):
    collection = BookCollection()

    with pytest.raises(ValueError, match=error_message):
        collection.add_book(title, author, year)

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


def test_list_books_returns_internal_list_reference():
    collection = BookCollection()
    listed = collection.list_books()
    assert listed is collection.books
    assert listed == []


def test_find_by_author_exact_case_insensitive_match():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Children of Dune", "Frank Herbert", 1976)
    collection.add_book("Foundation", "Isaac Asimov", 1951)

    results = collection.find_by_author("  frank herbert ")

    assert len(results) == 2
    assert [b.title for b in results] == ["Dune", "Children of Dune"]


def test_find_by_author_with_hyphenated_name():
    collection = BookCollection()
    collection.add_book("Nausea", "Jean-Paul Sartre", 1938)
    collection.add_book("No Exit", "Jean-Paul Sartre", 1944)
    collection.add_book("The Stranger", "Albert Camus", 1942)

    results = collection.find_by_author("jean-paul sartre")

    assert len(results) == 2
    assert [b.title for b in results] == ["Nausea", "No Exit"]


def test_find_by_author_with_multiple_first_names():
    collection = BookCollection()
    collection.add_book("Don Quixote", "Miguel de Cervantes", 1605)
    collection.add_book("Exemplary Novels", "Miguel de Cervantes", 1613)
    collection.add_book("Hamlet", "William Shakespeare", 1603)

    results = collection.find_by_author("  miguel de cervantes ")

    assert len(results) == 2
    assert [b.title for b in results] == ["Don Quixote", "Exemplary Novels"]


def test_find_by_author_with_empty_string_returns_empty_list():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.find_by_author("") == []
    assert collection.find_by_author("   ") == []


def test_find_by_author_with_accented_characters():
    collection = BookCollection()
    collection.add_book("One Hundred Years of Solitude", "Gabriel García Márquez", 1967)
    collection.add_book("Love in the Time of Cholera", "Gabriel García Márquez", 1985)
    collection.add_book("Blindness", "Jose Saramago", 1995)

    results = collection.find_by_author("gabriel garcía márquez")

    assert len(results) == 2
    assert [b.title for b in results] == [
        "One Hundred Years of Solitude",
        "Love in the Time of Cholera",
    ]


def test_adding_multiple_books_preserves_insert_order():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Foundation", "Isaac Asimov", 1951)

    books_in_collection = collection.list_books()
    assert [b.title for b in books_in_collection] == ["Dune", "Foundation"]


def test_find_book_by_title_exact_case_insensitive_and_trimmed():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    result = collection.find_book_by_title("  the hobbit  ")
    assert result is not None
    assert result.author == "J.R.R. Tolkien"


def test_find_book_by_title_returns_none_when_empty_collection():
    collection = BookCollection()
    assert collection.find_book_by_title("Anything") is None


def test_find_by_author_returns_empty_when_collection_is_empty():
    collection = BookCollection()
    assert collection.find_by_author("Frank Herbert") == []


def test_remove_book_returns_false_when_collection_is_empty():
    collection = BookCollection()
    assert collection.remove_book("Missing") is False
    assert collection.list_books() == []


def test_mark_as_read_returns_false_when_collection_is_empty():
    collection = BookCollection()
    assert collection.mark_as_read("Missing") is False
    assert collection.list_books() == []


def test_edge_case_empty_data_collection_starts_and_stays_empty():
    collection = BookCollection()
    assert collection.list_books() == []
    assert collection.find_by_author("Anyone") == []
    assert collection.find_book_by_title("Unknown") is None
    assert collection.remove_book("Unknown") is False
    assert collection.mark_as_read("Unknown") is False


@pytest.mark.parametrize(
    "value,field_name,expected_message",
    [
        (None, "title", "title must be a string"),
        (123, "author", "author must be a string"),
        ("   ", "review", "review cannot be empty"),
    ],
)
def test_validate_text_input_raises_for_invalid_values(value, field_name, expected_message):
    with pytest.raises(ValidationError, match=expected_message):
        BookCollection._validate_text_input(value, field_name)


def test_validate_text_input_strips_and_returns_value():
    assert BookCollection._validate_text_input("  Dune  ", "title") == "Dune"


@pytest.mark.parametrize("year", [True, False, "1949", 1949.5, None])
def test_validate_year_raises_for_non_integer_values(year):
    with pytest.raises(ValidationError, match="year must be an integer"):
        BookCollection._validate_year(year)


def test_validate_year_raises_for_negative_value():
    with pytest.raises(ValidationError, match="year cannot be negative"):
        BookCollection._validate_year(-1)


def test_validate_year_accepts_zero_as_boundary():
    assert BookCollection._validate_year(0) == 0


def test_normalize_search_field_raises_for_non_string():
    with pytest.raises(ValidationError, match="field must be 'title', 'author', or 'both'"):
        BookCollection._normalize_search_field(None)


def test_normalize_search_field_trims_and_lowercases():
    assert BookCollection._normalize_search_field("  AuThOr ") == "author"


@pytest.mark.parametrize("rating", [True, False, "8", 8.5, None])
def test_validate_rating_raises_for_non_integer_values(rating):
    with pytest.raises(ValidationError, match="rating must be an integer"):
        BookCollection._validate_rating(rating)


@pytest.mark.parametrize("rating", [0, 11, -5])
def test_validate_rating_raises_for_out_of_range_values(rating):
    with pytest.raises(ValidationError, match="rating must be between 1 and 10"):
        BookCollection._validate_rating(rating)


@pytest.mark.parametrize("rating", [1, 10])
def test_validate_rating_accepts_boundaries(rating):
    assert BookCollection._validate_rating(rating) == rating


def test_book_from_dict_normalizes_non_list_ratings_and_reviews():
    collection = BookCollection()
    book = collection._book_from_dict(
        {
            "title": "Dune",
            "author": "Frank Herbert",
            "year": 1965,
            "read": False,
            "ratings": "not-a-list",
            "reviews": {"text": "wrong-shape"},
        }
    )

    assert isinstance(book, Book)
    assert book.ratings == []
    assert book.reviews == []


def test_book_from_dict_raises_type_error_when_required_fields_missing():
    collection = BookCollection()
    with pytest.raises(TypeError):
        collection._book_from_dict({"title": "Dune"})


def test_load_books_uses_empty_list_when_file_not_found(tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.json"
    monkeypatch.setattr(books, "DATA_FILE", str(missing_file))

    collection = BookCollection()
    assert collection.books == []


def test_open_data_file_write_mode_maps_file_not_found_to_storage_error(monkeypatch):
    collection = BookCollection()

    def raise_file_not_found(*args, **kwargs):
        raise FileNotFoundError("missing path")

    monkeypatch.setattr("builtins.open", raise_file_not_found)

    with pytest.raises(StorageError, match="failed to save data file: file not found"):
        with collection._open_data_file("w"):
            pass


def test_open_data_file_read_mode_propagates_file_not_found(monkeypatch):
    collection = BookCollection()

    def raise_file_not_found(*args, **kwargs):
        raise FileNotFoundError("missing path")

    monkeypatch.setattr("builtins.open", raise_file_not_found)

    with pytest.raises(FileNotFoundError):
        with collection._open_data_file("r"):
            pass


@pytest.mark.parametrize(
    "mode,expected_message",
    [
        ("r", "failed to load data file: permission denied"),
        ("w", "failed to save data file: permission denied"),
    ],
)
def test_open_data_file_maps_oserror_by_mode(monkeypatch, mode, expected_message):
    collection = BookCollection()

    def raise_oserror(*args, **kwargs):
        raise OSError("permission denied")

    monkeypatch.setattr("builtins.open", raise_oserror)

    with pytest.raises(StorageError, match=expected_message):
        with collection._open_data_file(mode):
            pass


def test_adding_duplicate_books_same_title_and_author_is_allowed():
    collection = BookCollection()

    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert len(collection.list_books()) == 2
    assert [book.title for book in collection.list_books()] == ["Dune", "Dune"]
    assert [book.author for book in collection.list_books()] == ["Frank Herbert", "Frank Herbert"]


def test_remove_book_partial_title_does_not_match():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    result = collection.remove_book("Hob")

    assert result is False
    assert collection.find_book_by_title("The Hobbit") is not None


def test_remove_book_with_duplicates_removes_only_one_record():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.remove_book("Dune") is True
    assert len(collection.list_books()) == 1
    assert collection.find_book_by_title("Dune") is not None


def test_search_books_returns_empty_when_collection_is_empty():
    collection = BookCollection()
    assert collection.search_books("dune", "both") == []


def test_save_books_raises_storage_error_on_permission_denied(monkeypatch):
    collection = BookCollection()

    def raise_permission_error(*args, **kwargs):
        raise OSError("permission denied")

    monkeypatch.setattr("builtins.open", raise_permission_error)

    with pytest.raises(StorageError, match="failed to save data file: permission denied"):
        collection.save_books()


def test_add_book_raises_storage_error_when_save_permission_denied(monkeypatch):
    collection = BookCollection()

    def raise_permission_error(*args, **kwargs):
        raise OSError("permission denied")

    monkeypatch.setattr("builtins.open", raise_permission_error)

    with pytest.raises(StorageError, match="failed to save data file: permission denied"):
        collection.add_book("Dune", "Frank Herbert", 1965)


def test_concurrent_access_two_instances_require_reload_to_see_updates():
    first_client = BookCollection()
    second_client = BookCollection()

    first_client.add_book("Dune", "Frank Herbert", 1965)
    assert second_client.find_book_by_title("Dune") is None

    second_client.load_books()
    assert second_client.find_book_by_title("Dune") is not None
