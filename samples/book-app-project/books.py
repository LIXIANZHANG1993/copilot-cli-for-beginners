import json
from contextlib import contextmanager
from dataclasses import dataclass, asdict, field
from typing import Iterator, List, Optional, TextIO, Tuple
from errors import ValidationError, NotFoundError, StorageError

DATA_FILE = "data.json"
VALID_SEARCH_FIELDS = {"title", "author", "both"}


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False
    ratings: List[int] = field(default_factory=list)
    reviews: List[str] = field(default_factory=list)


class BookCollection:
    def __init__(self):
        """Initialize the collection and load persisted data.

        Args:
            None

        Returns:
            None

        Raises:
            StorageError: If the data file exists but cannot be read or is corrupted.

        Example:
            >>> collection = BookCollection()
            >>> isinstance(collection.books, list)
            True
        """
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON data file into memory.

        Args:
            None

        Returns:
            None

        Raises:
            StorageError: If JSON content is invalid or file access fails.

        Example:
            >>> collection = BookCollection()
            >>> collection.load_books()
        """
        try:
            with self._open_data_file("r") as f:
                data = json.load(f)
                self.books = [self._book_from_dict(b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            raise StorageError("data.json is corrupted")

    def save_books(self) -> None:
        """Persist the in-memory book list to the JSON data file.

        Args:
            None

        Returns:
            None

        Raises:
            StorageError: If writing to the data file fails.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.save_books()
        """
        with self._open_data_file("w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Validate input, create a book, append it, and save changes.

        Args:
            title (str): Book title. Must be a non-empty string.
            author (str): Author name. Must be a non-empty string.
            year (int): Publication year. Must be a non-negative integer.

        Returns:
            Book: The created and stored Book instance.

        Raises:
            ValidationError: If title/author/year validation fails.
            StorageError: If persisting updated data fails.

        Example:
            >>> collection = BookCollection()
            >>> book = collection.add_book("1984", "George Orwell", 1949)
            >>> book.title
            '1984'
        """
        validated_title = self._validate_text_input(title, "title")
        validated_author = self._validate_text_input(author, "author")
        validated_year = self._validate_year(year)
        book = Book(title=validated_title, author=validated_author, year=validated_year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books currently loaded in memory.

        Args:
            None

        Returns:
            List[Book]: The current list of books.

        Raises:
            None

        Example:
            >>> collection = BookCollection()
            >>> books = collection.list_books()
            >>> isinstance(books, list)
            True
        """
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a single book by normalized exact title match.

        Args:
            title (str): Title to match. Comparison is case-insensitive and
                normalizes extra whitespace.

        Returns:
            Optional[Book]: Matching Book if found, otherwise None.

        Raises:
            None

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.find_book_by_title("dune").author
            'Frank Herbert'
        """
        if not isinstance(title, str) or not title.strip():
            return None

        normalized_title = self._normalize_match_text(title)
        for book in self.books:
            if self._normalize_match_text(book.title) == normalized_title:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by title.

        Args:
            title (str): Title of the target book.

        Returns:
            bool: True if the book was found and updated, False otherwise.

        Raises:
            StorageError: If saving the updated state fails.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.mark_as_read("Dune")
            True
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> Tuple[bool, str]:
        """Remove a book by title.

        Args:
            title (str): Title of the book to remove.

        Returns:
            Tuple[bool, str]:
                - First item is True if a book was removed, otherwise False.
                - Second item is a user-friendly status message.

        Raises:
            StorageError: If saving after removal fails.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
            >>> collection.remove_book("The Hobbit")
            (True, "Book 'The Hobbit' removed.")
        """
        if not isinstance(title, str):
            return False, "Title must be a string."

        normalized_title = self._normalize_match_text(title)
        if not normalized_title:
            return False, "Title cannot be empty."

        for index, book in enumerate(self.books):
            if self._normalize_match_text(book.title) == normalized_title:
                removed_title = book.title
                del self.books[index]
                self.save_books()
                return True, f"Book '{removed_title}' removed."

        suggestions = [
            book.title for book in self.books if normalized_title in self._normalize_match_text(book.title)
        ][:3]
        if suggestions:
            return (
                False,
                "Book not found. Did you mean: " + ", ".join(f"'{candidate}'" for candidate in suggestions) + "?",
            )

        return False, f"Book '{title.strip()}' not found."

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by exact author match (case-insensitive).

        Args:
            author (str): Author name to match.

        Returns:
            List[Book]: Matching books. Empty list if none found or input is empty.

        Raises:
            None

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> len(collection.find_by_author("frank herbert"))
            1
        """
        if not isinstance(author, str) or not author.strip():
            return []

        normalized_author = author.strip().lower()
        return [b for b in self.books if b.author.lower() == normalized_author]

    def search_books(self, query: str, field: str = "both") -> List[Book]:
        """Search books by partial text in title, author, or both.

        Args:
            query (str): Search keyword. Empty/blank query returns an empty list.
            field (str): Search scope: "title", "author", or "both".

        Returns:
            List[Book]: Books matching the search criteria.

        Raises:
            ValidationError: If query is not a string or field is invalid.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune Messiah", "Frank Herbert", 1969)
            >>> [b.title for b in collection.search_books("dune", "title")]
            ['Dune Messiah']
        """
        if not isinstance(query, str):
            raise ValidationError("query must be a string")

        normalized_query = query.strip().lower()
        if not normalized_query:
            return []

        normalized_field = self._normalize_search_field(field)
        if normalized_field not in VALID_SEARCH_FIELDS:
            raise ValidationError("field must be 'title', 'author', or 'both'")

        results: List[Book] = []
        for book in self.books:
            title_match = normalized_query in book.title.lower()
            author_match = normalized_query in book.author.lower()

            if normalized_field == "title" and title_match:
                results.append(book)
            elif normalized_field == "author" and author_match:
                results.append(book)
            elif normalized_field == "both" and (title_match or author_match):
                results.append(book)

        return results

    def add_rating(self, title: str, rating: int) -> bool:
        """Add a numeric rating to a book.

        Args:
            title (str): Title of the target book.
            rating (int): Rating value from 1 to 10.

        Returns:
            bool: True when rating is successfully added.

        Raises:
            NotFoundError: If the target book does not exist.
            ValidationError: If rating is not an integer in range 1..10.
            StorageError: If saving updated data fails.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.add_rating("Dune", 9)
            True
        """
        book = self.find_book_by_title(title)
        if not book:
            raise NotFoundError("book not found")

        validated_rating = self._validate_rating(rating)
        book.ratings.append(validated_rating)
        self.save_books()
        return True

    def add_review(self, title: str, review: str) -> bool:
        """Add a text review to a book.

        Args:
            title (str): Title of the target book.
            review (str): Review text. Must be a non-empty string.

        Returns:
            bool: True when the review is successfully added.

        Raises:
            NotFoundError: If the target book does not exist.
            ValidationError: If review is empty or not a string.
            StorageError: If saving updated data fails.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.add_review("Dune", "Great world-building.")
            True
        """
        book = self.find_book_by_title(title)
        if not book:
            raise NotFoundError("book not found")

        validated_review = self._validate_text_input(review, "review")
        book.reviews.append(validated_review)
        self.save_books()
        return True

    def get_reviews(self, title: str) -> List[str]:
        """Get all reviews for a given book title.

        Args:
            title (str): Title of the target book.

        Returns:
            List[str]: Reviews for the book, or an empty list when not found.

        Raises:
            None

        Example:
            >>> collection = BookCollection()
            >>> collection.get_reviews("Unknown")
            []
        """
        book = self.find_book_by_title(title)
        if not book:
            return []
        return list(book.reviews)

    def get_average_rating(self, title: str) -> Optional[float]:
        """Compute the average rating for a book.

        Args:
            title (str): Title of the target book.

        Returns:
            Optional[float]: Average rating, or None if no ratings or no book.

        Raises:
            None

        Example:
            >>> collection = BookCollection()
            >>> collection.get_average_rating("Unknown") is None
            True
        """
        book = self.find_book_by_title(title)
        if not book or not book.ratings:
            return None
        return sum(book.ratings) / len(book.ratings)

    @staticmethod
    def _validate_text_input(value: str, field_name: str) -> str:
        """Validate and normalize user-provided text fields.

        Args:
            value (str): Input value to validate.
            field_name (str): Human-readable field name used in error messages.

        Returns:
            str: Stripped non-empty text value.

        Raises:
            ValidationError: If value is not a string or becomes empty after strip.

        Example:
            >>> BookCollection._validate_text_input("  Dune  ", "title")
            'Dune'
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")

        normalized_value = value.strip()
        if not normalized_value:
            raise ValidationError(f"{field_name} cannot be empty")

        return normalized_value

    @staticmethod
    def _validate_year(year: int) -> int:
        """Validate publication year value.

        Args:
            year (int): Year to validate.

        Returns:
            int: Original year when valid.

        Raises:
            ValidationError: If year is not an integer or is negative.

        Example:
            >>> BookCollection._validate_year(1965)
            1965
        """
        if isinstance(year, bool) or not isinstance(year, int):
            raise ValidationError("year must be an integer")
        if year < 0:
            raise ValidationError("year cannot be negative")
        return year

    @staticmethod
    def _normalize_search_field(field: str) -> str:
        """Normalize search field string for internal use.

        Args:
            field (str): Raw field value such as "title", "author", or "both".

        Returns:
            str: Lower-cased and stripped field value.

        Raises:
            ValidationError: If field is not a string.

        Example:
            >>> BookCollection._normalize_search_field(" Title ")
            'title'
        """
        if not isinstance(field, str):
            raise ValidationError("field must be 'title', 'author', or 'both'")
        return field.strip().lower()

    @staticmethod
    def _normalize_match_text(value: str) -> str:
        """Normalize text for robust title matching."""
        return " ".join(value.strip().split()).casefold()

    @staticmethod
    def _validate_rating(rating: int) -> int:
        """Validate rating input.

        Args:
            rating (int): Candidate rating value.

        Returns:
            int: Original rating when valid.

        Raises:
            ValidationError: If rating is not an integer in range 1..10.

        Example:
            >>> BookCollection._validate_rating(8)
            8
        """
        if isinstance(rating, bool) or not isinstance(rating, int):
            raise ValidationError("rating must be an integer")
        if rating < 1 or rating > 10:
            raise ValidationError("rating must be between 1 and 10")
        return rating

    def _book_from_dict(self, raw_book: dict) -> Book:
        """Convert a raw dictionary from JSON into a Book object.

        Args:
            raw_book (dict): Dictionary representing a book record.

        Returns:
            Book: Parsed Book instance with normalized ratings/reviews lists.

        Raises:
            TypeError: If required Book fields are missing or malformed.

        Example:
            >>> collection = BookCollection()
            >>> collection._book_from_dict({"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": False})
            Book(title='Dune', author='Frank Herbert', year=1965, read=False, ratings=[], reviews=[])
        """
        normalized_book = dict(raw_book)
        ratings = normalized_book.get("ratings", [])
        reviews = normalized_book.get("reviews", [])

        normalized_book["ratings"] = ratings if isinstance(ratings, list) else []
        normalized_book["reviews"] = reviews if isinstance(reviews, list) else []

        return Book(**normalized_book)

    @contextmanager
    def _open_data_file(self, mode: str) -> Iterator[TextIO]:
        """Open the app data file via a unified context manager.

        Args:
            mode (str): File mode. Supported modes in this class are "r" and "w".

        Returns:
            Iterator[TextIO]: A context-managed file handle for JSON read/write.

        Raises:
            FileNotFoundError: When opening in read mode and file does not exist.
            StorageError: If file open operation fails for other OS-level reasons.

        Example:
            >>> collection = BookCollection()
            >>> with collection._open_data_file("w") as f:
            ...     _ = f.write("[]")
        """
        try:
            with open(DATA_FILE, mode, encoding="utf-8") as data_file:
                yield data_file
        except FileNotFoundError:
            if mode == "r":
                raise
            raise StorageError("failed to save data file: file not found") from None
        except OSError as error:
            action = "load" if mode == "r" else "save"
            raise StorageError(f"failed to {action} data file: {error}") from error
