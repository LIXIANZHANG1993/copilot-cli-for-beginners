import sys
from books import BookCollection
from utils import print_books
from errors import BookAppError, NotFoundError


# Global collection instance
collection = BookCollection()


def handle_list() -> None:
    books = collection.list_books()
    print_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except BookAppError as e:
        print(f"\nError: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    removed, message = collection.remove_book(title)
    if removed:
        print(f"\n{message}\n")
    else:
        print(f"\nNot removed: {message}\n")


def handle_find() -> None:

    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    print_books(books)


def handle_search() -> None:
    print("\nSearch Books\n")

    query = input("Keyword (title or author): ").strip()
    scope = input("Scope [both/title/author] (default: both): ").strip().lower() or "both"

    try:
        results = collection.search_books(query, scope)
        print_books(results)
    except BookAppError as e:
        print(f"\nError: {e}\n")


def handle_rate() -> None:
    print("\nRate a Book\n")

    title = input("Book title: ").strip()
    rating_str = input("Rating (1-10): ").strip()

    try:
        rating = int(rating_str)
        collection.add_rating(title, rating)
        average = collection.get_average_rating(title)
        print(f"\nRating added. Current average: {average:.1f}/10\n")
    except NotFoundError:
        print("\nBook not found.\n")
    except ValueError:
        print("\nError: rating must be a number.\n")
    except BookAppError as e:
        print(f"\nError: {e}\n")


def handle_review() -> None:
    print("\nAdd a Review\n")

    title = input("Book title: ").strip()
    review = input("Review text: ").strip()

    try:
        collection.add_review(title, review)
        print("\nReview added successfully.\n")
    except NotFoundError:
        print("\nBook not found.\n")
    except BookAppError as e:
        print(f"\nError: {e}\n")


def handle_reviews() -> None:
    print("\nShow Reviews\n")

    title = input("Book title: ").strip()
    reviews = collection.get_reviews(title)
    if not reviews:
        print("\nNo reviews found.\n")
        return

    print()
    for index, review in enumerate(reviews, start=1):
        print(f"{index}. {review}")
    print()


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  search   - Search books by title/author keyword
  rate     - Add a 1-10 rating to a book
  review   - Add a text review for a book
  reviews  - Show all reviews for a book
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    command_handlers = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "search": handle_search,
        "rate": handle_rate,
        "review": handle_review,
        "reviews": handle_reviews,
        "help": show_help,
    }

    handler = command_handlers.get(command)
    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
