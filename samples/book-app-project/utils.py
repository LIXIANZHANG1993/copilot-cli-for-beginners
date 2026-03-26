def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if not choice:
            print("Input cannot be empty. Please enter a number.")
            continue
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        return choice


def get_book_details():
    """Collect book details from user input with basic validation.

    Parameters:
        None: This function does not accept parameters. It prompts the user
        interactively via standard input.

    Returns:
        tuple[str, str, int]: A tuple containing:
            - title (str): Non-empty book title entered by the user.
            - author (str): Author name entered by the user (may be empty).
            - year (int): Publication year converted to an integer. If the
              entered value is invalid, defaults to 0.
    """
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please enter a title.")
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
