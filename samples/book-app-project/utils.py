from errors import ValidationError


MENU_OPTIONS = {"1", "2", "3", "4", "5"}


def display_message(message: str) -> None:
    print(message)


def format_menu_lines() -> list[str]:
    return [
        "\n📚 Book Collection App",
        "1. Add a book",
        "2. List books",
        "3. Mark book as read",
        "4. Remove a book",
        "5. Exit",
    ]


def print_menu() -> None:
    for line in format_menu_lines():
        display_message(line)


def validate_user_choice(raw_choice: str) -> str:
    choice = raw_choice.strip()
    if not choice:
        raise ValidationError("Input cannot be empty. Please enter a number.")
    if not choice.isdigit():
        raise ValidationError("Invalid input. Please enter a number.")
    if choice not in MENU_OPTIONS:
        raise ValidationError("Invalid choice. Please enter a number between 1 and 5.")
    return choice


def get_user_choice() -> str:
    while True:
        raw_choice = input("Choose an option (1-5): ")
        try:
            return validate_user_choice(raw_choice)
        except ValidationError as error:
            display_message(str(error))


def validate_title(raw_title: str) -> str:
    title = raw_title.strip()
    if not title:
        raise ValidationError("Title cannot be empty. Please enter a title.")
    return title


def parse_publication_year(year_input: str) -> tuple[int, bool]:
    try:
        return int(year_input.strip()), False
    except ValueError:
        return 0, True


def get_book_details() -> tuple[str, str, int]:
    """Collect book details from user input with validation."""
    while True:
        raw_title = input("Enter book title: ")
        try:
            title = validate_title(raw_title)
            break
        except ValidationError as error:
            display_message(str(error))

    author = input("Enter author: ").strip()
    year_input = input("Enter publication year: ")
    year, used_default = parse_publication_year(year_input)
    if used_default:
        display_message("Invalid year. Defaulting to 0.")

    return title, author, year


def format_books(books) -> list[str]:
    if not books:
        return ["No books in your collection."]

    lines = ["\nYour Books:"]
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        lines.append(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
    return lines


def print_books(books) -> None:
    for line in format_books(books):
        display_message(line)
