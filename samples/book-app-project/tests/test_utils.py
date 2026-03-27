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


def test_parse_publication_year_returns_default_on_invalid():
    year, used_default = utils.parse_publication_year("not-a-year")
    assert year == 0
    assert used_default is True


def test_format_books_returns_no_books_message():
    assert utils.format_books([]) == ["No books in your collection."]
