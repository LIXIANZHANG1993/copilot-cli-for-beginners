import pytest
import utils


def test_get_user_choice_retries_on_empty_input(monkeypatch, capsys):
    inputs = iter(["", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    choice = utils.get_user_choice()

    assert choice == "2"
    captured = capsys.readouterr()
    assert "Input cannot be empty. Please enter a number." in captured.out


def test_get_user_choice_retries_on_non_numeric_input(monkeypatch, capsys):
    inputs = iter(["abc", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    choice = utils.get_user_choice()

    assert choice == "5"
    captured = capsys.readouterr()
    assert "Invalid input. Please enter a number." in captured.out


def test_get_user_choice_retries_on_out_of_range_number(monkeypatch, capsys):
    inputs = iter(["9", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    choice = utils.get_user_choice()

    assert choice == "1"
    captured = capsys.readouterr()
    assert "Invalid choice. Please enter a number between 1 and 5." in captured.out


def test_get_book_details_retries_on_empty_title(monkeypatch, capsys):
    inputs = iter(["", "Dune", "Frank Herbert", "1965"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    title, author, year = utils.get_book_details()

    assert title == "Dune"
    assert author == "Frank Herbert"
    assert year == 1965
    captured = capsys.readouterr()
    assert "Title cannot be empty. Please enter a title." in captured.out


def test_get_book_details_valid_input(monkeypatch):
    inputs = iter(["The Hobbit", "J.R.R. Tolkien", "1937"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    title, author, year = utils.get_book_details()

    assert title == "The Hobbit"
    assert author == "J.R.R. Tolkien"
    assert year == 1937


def test_get_book_details_allows_empty_author_string(monkeypatch):
    inputs = iter(["Dune", "   ", "1965"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    title, author, year = utils.get_book_details()

    assert title == "Dune"
    assert author == ""
    assert year == 1965


def test_get_book_details_accepts_very_long_title(monkeypatch):
    long_title = "A" * 5000
    inputs = iter([long_title, "Author", "2020"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    title, author, year = utils.get_book_details()

    assert title == long_title
    assert author == "Author"
    assert year == 2020


def test_get_book_details_preserves_special_characters_in_author(monkeypatch):
    author = "Gabriel García Márquez / O'Connor-Łukasz"
    inputs = iter(["One Hundred Years of Solitude", author, "1967"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    title, returned_author, year = utils.get_book_details()

    assert title == "One Hundred Years of Solitude"
    assert returned_author == author
    assert year == 1967

@pytest.mark.parametrize("invalid_year", ["abc", "20O0", "19.84", "", "   "])
def test_get_book_details_invalid_year_formats_default_to_zero(monkeypatch, capsys, invalid_year):
    inputs = iter(["Dune", "Frank Herbert", invalid_year])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    title, author, year = utils.get_book_details()

    assert title == "Dune"
    assert author == "Frank Herbert"
    assert year == 0
    captured = capsys.readouterr()
    assert "Invalid year. Defaulting to 0." in captured.out


def test_parse_publication_year_returns_default_on_invalid():
    with pytest.raises(utils.ValidationError, match=r"Invalid year\. Please enter a valid integer\."):
        utils.parse_publication_year("not-a-year")


def test_format_books_returns_no_books_message():
    assert utils.format_books([]) == ["No books in your collection."]
