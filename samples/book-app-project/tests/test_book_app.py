import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import books
import book_app
from books import BookCollection


def _set_inputs(monkeypatch, values):
    inputs = iter(values)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))


def _setup_collection(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    book_app.collection = BookCollection()
    return book_app.collection


def test_handle_search_displays_matching_books(tmp_path, monkeypatch, capsys):
    collection = _setup_collection(tmp_path, monkeypatch)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    _set_inputs(monkeypatch, ["dune", "both"])
    book_app.handle_search()

    captured = capsys.readouterr()
    assert "Search Books" in captured.out
    assert "Dune by Frank Herbert (1965)" in captured.out
    assert "The Hobbit" not in captured.out


def test_handle_rate_adds_rating_and_shows_average(tmp_path, monkeypatch, capsys):
    collection = _setup_collection(tmp_path, monkeypatch)
    collection.add_book("Dune", "Frank Herbert", 1965)

    _set_inputs(monkeypatch, ["Dune", "9"])
    book_app.handle_rate()

    captured = capsys.readouterr()
    assert "Rating added. Current average: 9.0/10" in captured.out
    assert collection.get_average_rating("Dune") == 9.0


def test_handle_review_and_reviews_flow(tmp_path, monkeypatch, capsys):
    collection = _setup_collection(tmp_path, monkeypatch)
    collection.add_book("Dune", "Frank Herbert", 1965)

    _set_inputs(monkeypatch, ["Dune", "Great world-building."])
    book_app.handle_review()
    first_output = capsys.readouterr().out
    assert "Review added successfully." in first_output

    _set_inputs(monkeypatch, ["Dune"])
    book_app.handle_reviews()
    second_output = capsys.readouterr().out
    assert "1. Great world-building." in second_output


def test_show_help_lists_new_commands(capsys):
    book_app.show_help()

    captured = capsys.readouterr()
    assert "search   - Search books by title/author keyword" in captured.out
    assert "rate     - Add a 1-10 rating to a book" in captured.out
    assert "review   - Add a text review for a book" in captured.out
    assert "reviews  - Show all reviews for a book" in captured.out


def test_handle_remove_reports_not_removed_when_missing(tmp_path, monkeypatch, capsys):
    _setup_collection(tmp_path, monkeypatch)
    _set_inputs(monkeypatch, ["Missing"])

    book_app.handle_remove()

    captured = capsys.readouterr()
    assert "Not removed: Book 'Missing' not found." in captured.out
