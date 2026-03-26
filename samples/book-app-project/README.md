# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A Python app for managing books you have or want to read.
It can add, remove, and list books. Also mark them as read.

---

## Current Features

* Reads books from a JSON file (our database)
* Input checking is weak in some areas
* Some tests exist but probably not enough

---

## Files

* `book_app.py` - Main CLI entry point
* `books.py` - BookCollection class with data logic
* `utils.py` - Helper functions for UI and input
* `data.json` - Sample book data
* `tests/test_books.py` - Starter pytest tests

---

## Running the App

```bash
python book_app.py list
python book_app.py add
python book_app.py find
python book_app.py search
python book_app.py rate
python book_app.py review
python book_app.py reviews
python book_app.py remove
python book_app.py help
```

## Search Example

```bash
python book_app.py search
```

Example interaction:

```text
Search Books

Keyword (title or author): dune
Scope [both/title/author] (default: both): both

Your Book Collection:

1. [ ] Dune by Frank Herbert (1965)
2. [ ] Dune Messiah by Frank Herbert (1969)
```

## Rating and Review Examples

Add a rating:

```bash
python book_app.py rate
```

Example interaction:

```text
Rate a Book

Book title: Dune
Rating (1-10): 9

Rating added. Current average: 9.0/10
```

Add a review:

```bash
python book_app.py review
```

Example interaction:

```text
Add a Review

Book title: Dune
Review text: Great world-building and political depth.

Review added successfully.
```

Show reviews:

```bash
python book_app.py reviews
```

## Running Tests

```bash
python -m pytest tests/
```

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later
