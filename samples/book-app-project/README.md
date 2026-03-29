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
python book_app.py search-year
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

## Search by Year Range Example

```bash
python book_app.py search-year
```

Use this command to find books published between two years (inclusive).

Rules:

* Both values must be valid integers
* Range is inclusive (`start_year <= book.year <= end_year`)
* `start year` cannot be greater than `end year`

Example interaction:

```text
Search Books by Year Range

Start year: 1930
End year: 1970

Your Book Collection:

1. [ ] Dune by Frank Herbert (1965)
2. [ ] The Hobbit by J.R.R. Tolkien (1937)
```

Error examples:

```text
Search Books by Year Range

Start year: 2000
End year: 1990

Error: start year cannot be greater than end year
```

```text
Search Books by Year Range

Start year: 19xx
End year: 2000

Error: years must be numbers.
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

## 錯誤處理重構說明（Error Handling Refactor）

本次重構統一了錯誤語意：資料與業務層在失敗時拋出明確例外，CLI 層集中捕捉並輸出可讀訊息，不再混用旗標回傳表示失敗。

### 主要原則

* 統一例外層級：`BookAppError`（基類）、`ValidationError`、`NotFoundError`、`StorageError`
* 失敗優先用例外傳遞原因，避免 `False` / `None` 混雜錯誤語意
* CLI 對可預期錯誤提供清楚訊息，非預期錯誤維持 `BookAppError` 路徑

### 方法契約變更

* `remove_book(title)`：改為成功回傳 `None`，失敗時拋 `ValidationError` / `NotFoundError` / `StorageError`
* `mark_as_read(title)`：改為成功回傳 `None`，找不到時拋 `NotFoundError`
* `add_rating(title, rating)`、`add_review(title, review)`：成功回傳 `None`，失敗拋相對應例外
* `add_book(...)`、`search_books(...)` 維持以例外表示失敗

### 資料載入驗證策略

* `load_books()` 對 JSON 結構與欄位型別做驗證
* JSON 損壞時拋 `StorageError("data.json is corrupted")`
* 記錄欄位不合法時統一拋 `StorageError("data.json contains invalid book records")`
* 檔案不存在時仍視為空集合（相容既有行為）
* 針對舊資料缺少 `ratings` / `reviews` 時提供預設 `[]`

### CLI remove 行為調整

* 刪除成功：`Book removed successfully.`
* 失敗（輸入無效或找不到）：`Not removed: <reason>`

範例：

```text
$ python book_app.py remove
Enter the title of the book to remove: Missing

Not removed: Book 'Missing' not found.
```

### 驗證結果

```bash
python -m pytest tests/
```

目前測試全數通過：`135 passed`。

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later
