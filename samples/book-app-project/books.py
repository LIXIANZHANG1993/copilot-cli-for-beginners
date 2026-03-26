import json
from dataclasses import dataclass, asdict, field
from typing import List, Optional

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
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [self._book_from_dict(b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> None:
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        validated_title = self._validate_text_input(title, "title")
        validated_author = self._validate_text_input(author, "author")
        validated_year = self._validate_year(year)
        book = Book(title=validated_title, author=validated_author, year=validated_year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        if not isinstance(title, str) or not title.strip():
            return None

        normalized_title = title.strip().lower()
        for book in self.books:
            if book.title.lower() == normalized_title:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        if not isinstance(author, str) or not author.strip():
            return []

        normalized_author = author.strip().lower()
        return [b for b in self.books if b.author.lower() == normalized_author]

    def search_books(self, query: str, field: str = "both") -> List[Book]:
        """Search books by title, author, or both using case-insensitive partial match."""
        if not isinstance(query, str):
            raise ValueError("query must be a string")

        normalized_query = query.strip().lower()
        if not normalized_query:
            return []

        normalized_field = self._normalize_search_field(field)
        if normalized_field not in VALID_SEARCH_FIELDS:
            raise ValueError("field must be 'title', 'author', or 'both'")

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
        book = self.find_book_by_title(title)
        if not book:
            return False

        validated_rating = self._validate_rating(rating)
        book.ratings.append(validated_rating)
        self.save_books()
        return True

    def add_review(self, title: str, review: str) -> bool:
        book = self.find_book_by_title(title)
        if not book:
            return False

        validated_review = self._validate_text_input(review, "review")
        book.reviews.append(validated_review)
        self.save_books()
        return True

    def get_reviews(self, title: str) -> List[str]:
        book = self.find_book_by_title(title)
        if not book:
            return []
        return list(book.reviews)

    def get_average_rating(self, title: str) -> Optional[float]:
        book = self.find_book_by_title(title)
        if not book or not book.ratings:
            return None
        return sum(book.ratings) / len(book.ratings)

    @staticmethod
    def _validate_text_input(value: str, field_name: str) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty")

        return normalized_value

    @staticmethod
    def _validate_year(year: int) -> int:
        if isinstance(year, bool) or not isinstance(year, int):
            raise ValueError("year must be an integer")
        if year < 0:
            raise ValueError("year cannot be negative")
        return year

    @staticmethod
    def _normalize_search_field(field: str) -> str:
        if not isinstance(field, str):
            raise ValueError("field must be 'title', 'author', or 'both'")
        return field.strip().lower()

    @staticmethod
    def _validate_rating(rating: int) -> int:
        if isinstance(rating, bool) or not isinstance(rating, int):
            raise ValueError("rating must be an integer")
        if rating < 1 or rating > 10:
            raise ValueError("rating must be between 1 and 10")
        return rating

    def _book_from_dict(self, raw_book: dict) -> Book:
        normalized_book = dict(raw_book)
        ratings = normalized_book.get("ratings", [])
        reviews = normalized_book.get("reviews", [])

        normalized_book["ratings"] = ratings if isinstance(ratings, list) else []
        normalized_book["reviews"] = reviews if isinstance(reviews, list) else []

        return Book(**normalized_book)
