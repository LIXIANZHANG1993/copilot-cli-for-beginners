# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `f562430e-1a86-4c4e-9663-f190b2790a63`  
> - **Started:** 2026/3/27 下午1:17:31  
> - **Duration:** 4m 35s  
> - **Exported:** 2026/3/27 下午1:22:06  

---

<sub>⏱️ 1m 0s</sub>

### 👤 User

@samples/book-app-project/books.py @samples/book-app-project/book_app.py 追蹤一本書如何從使用者輸入到被儲存進 data.json。

---

<sub>⏱️ 1m 6s</sub>

### 💬 Copilot

我先快速讀這兩個檔案，然後用流程圖式步驟幫你追蹤資料怎麼進 `data.json`。

---

<sub>⏱️ 1m 6s</sub>

### ✅ `view`

**view the file at C:\Copilot_learn\copilot-cli-for-beginners\samples\book-app-project\book_app.py.**

C:\Copilot_learn\copilot-cli-for-beginners\samples\book-app-project\book_app.py

<details>
<summary>155 lines</summary>

```
1. import sys
2. from books import BookCollection
3. from utils import print_books
4. 
5. 
6. # Global collection instance
7. collection = BookCollection()
8. 
9. 
10. def handle_list() -> None:
11.     books = collection.list_books()
12.     print_books(books)
13. 
14. 
15. def handle_add() -> None:
16.     print("\nAdd a New Book\n")
17. 
18.     title = input("Title: ").strip()
19.     author = input("Author: ").strip()
20.     year_str = input("Year: ").strip()
21. 
22.     try:
23.         year = int(year_str) if year_str else 0
24.         collection.add_book(title, author, year)
25.         print("\nBook added successfully.\n")
26.     except ValueError as e:
27.         print(f"\nError: {e}\n")
28. 
29. 
30. def handle_remove() -> None:
31.     print("\nRemove a Book\n")
32. 
33.     title = input("Enter the title of the book to remove: ").strip()
34.     collection.remove_book(title)
35. 
36.     print("\nBook removed if it existed.\n")
37. 
38. 
39. def handle_find() -> None:
40. 
41.     print("\nFind Books by Author\n")
42. 
43.     author = input("Author name: ").strip()
44.     books = collection.find_by_author(author)
45. 
46.     print_books(books)
47. 
48. 
49. def handle_search() -> None:
50.     print("\nSearch Books\n")
51. 
52.     query = input("Keyword (title or author): ").strip()
53.     scope = input("Scope [both/title/author] (default: both): ").strip().lower() or "both"
54. 
55.     try:
56.         results = collection.search_books(query, scope)
57.         print_books(results)
58.     except ValueError as e:
59.         print(f"\nError: {e}\n")
60. 
61. 
62. def handle_rate() -> None:
63.     print("\nRate a Book\n")
64. 
65.     title = input("Book title: ").strip()
66.     rating_str = input("Rating (1-10): ").strip()
67. 
68.     try:
69.         rating = int(rating_str)
70.         if not collection.add_rating(title, rating):
71.             print("\nBook not found.\n")
72.             return
73.         average = collection.get_average_rating(title)
74.         print(f"\nRating added. Current average: {average:.1f}/10\n")
75.     except ValueError as e:
76.         print(f"\nError: {e}\n")
77. 
78. 
79. def handle_review() -> None:
80.     print("\nAdd a Review\n")
81. 
82.     title = input("Book title: ").strip()
83.     review = input("Review text: ").strip()
84. 
85.     try:
86.         if not collection.add_review(title, review):
87.             print("\nBook not found.\n")
88.             return
89.         print("\nReview added successfully.\n")
90.     except ValueError as e:
91.         print(f"\nError: {e}\n")
92. 
93. 
94. def handle_reviews() -> None:
95.     print("\nShow Reviews\n")
96. 
97.     title = input("Book title: ").strip()
98.     reviews = collection.get_reviews(title)
99.     if not reviews:
100.         print("\nNo reviews found.\n")
101.         return
102. 
103.     print()
104.     for index, review in enumerate(reviews, start=1):
105.         print(f"{index}. {review}")
106.     print()
107. 
108. 
109. def show_help():
110.     print("""
111. Book Collection Helper
112. 
113. Commands:
114.   list     - Show all books
115.   add      - Add a new book
116.   remove   - Remove a book by title
117.   find     - Find books by author
118.   search   - Search books by title/author keyword
119.   rate     - Add a 1-10 rating to a book
120.   review   - Add a text review for a book
121.   reviews  - Show all reviews for a book
122.   help     - Show this help message
123. """)
124. 
125. 
126. def main():
127.     if len(sys.argv) < 2:
128.         show_help()
129.         return
130. 
131.     command = sys.argv[1].lower()
132. 
133.     command_handlers = {
134.         "list": handle_list,
135.         "add": handle_add,
136.         "remove": handle_remove,
137.         "find": handle_find,
138.         "search": handle_search,
139.         "rate": handle_rate,
140.         "review": handle_review,
141.         "reviews": handle_reviews,
142.         "help": show_help,
143.     }
144. 
145.     handler = command_handlers.get(command)
146.     if handler:
147.         handler()
148.     else:
149.         print("Unknown command.\n")
150.         show_help()
151. 
152. 
153. if __name__ == "__main__":
154.     main()
155.
```

</details>


---

<sub>⏱️ 1m 6s</sub>

### ✅ `view`

**view the file at C:\Copilot_learn\copilot-cli-for-beginners\samples\book-app-project\books.py.**

C:\Copilot_learn\copilot-cli-for-beginners\samples\book-app-project\books.py

<details>
<summary>189 lines</summary>

```
1. import json
2. from dataclasses import dataclass, asdict, field
3. from typing import List, Optional
4. 
5. DATA_FILE = "data.json"
6. VALID_SEARCH_FIELDS = {"title", "author", "both"}
7. 
8. 
9. @dataclass
10. class Book:
11.     title: str
12.     author: str
13.     year: int
14.     read: bool = False
15.     ratings: List[int] = field(default_factory=list)
16.     reviews: List[str] = field(default_factory=list)
17. 
18. 
19. class BookCollection:
20.     def __init__(self):
21.         self.books: List[Book] = []
22.         self.load_books()
23. 
24.     def load_books(self) -> None:
25.         """Load books from the JSON file if it exists."""
26.         try:
27.             with open(DATA_FILE, "r", encoding="utf-8") as f:
28.                 data = json.load(f)
29.                 self.books = [self._book_from_dict(b) for b in data]
30.         except FileNotFoundError:
31.             self.books = []
32.         except json.JSONDecodeError:
33.             print("Warning: data.json is corrupted. Starting with empty collection.")
34.             self.books = []
35. 
36.     def save_books(self) -> None:
37.         """Save the current book collection to JSON."""
38.         with open(DATA_FILE, "w", encoding="utf-8") as f:
39.             json.dump([asdict(b) for b in self.books], f, indent=2)
40. 
41.     def add_book(self, title: str, author: str, year: int) -> Book:
42.         validated_title = self._validate_text_input(title, "title")
43.         validated_author = self._validate_text_input(author, "author")
44.         validated_year = self._validate_year(year)
45.         book = Book(title=validated_title, author=validated_author, year=validated_year)
46.         self.books.append(book)
47.         self.save_books()
48.         return book
49. 
50.     def list_books(self) -> List[Book]:
51.         return self.books
52. 
53.     def find_book_by_title(self, title: str) -> Optional[Book]:
54.         if not isinstance(title, str) or not title.strip():
55.             return None
56. 
57.         normalized_title = title.strip().lower()
58.         for book in self.books:
59.             if book.title.lower() == normalized_title:
60.                 return book
61.         return None
62. 
63.     def mark_as_read(self, title: str) -> bool:
64.         book = self.find_book_by_title(title)
65.         if book:
66.             book.read = True
67.             self.save_books()
68.             return True
69.         return False
70. 
71.     def remove_book(self, title: str) -> bool:
72.         """Remove a book by title."""
73.         book = self.find_book_by_title(title)
74.         if book:
75.             self.books.remove(book)
76.             self.save_books()
77.             return True
78.         return False
79. 
80.     def find_by_author(self, author: str) -> List[Book]:
81.         """Find all books by a given author."""
82.         if not isinstance(author, str) or not author.strip():
83.             return []
84. 
85.         normalized_author = author.strip().lower()
86.         return [b for b in self.books if b.author.lower() == normalized_author]
87. 
88.     def search_books(self, query: str, field: str = "both") -> List[Book]:
89.         """Search books by title, author, or both using case-insensitive partial match."""
90.         if not isinstance(query, str):
91.             raise ValueError("query must be a string")
92. 
93.         normalized_query = query.strip().lower()
94.         if not normalized_query:
95.             return []
96. 
97.         normalized_field = self._normalize_search_field(field)
98.         if normalized_field not in VALID_SEARCH_FIELDS:
99.             raise ValueError("field must be 'title', 'author', or 'both'")
100. 
101.         results: List[Book] = []
102.         for book in self.books:
103.             title_match = normalized_query in book.title.lower()
104.             author_match = normalized_query in book.author.lower()
105. 
106.             if normalized_field == "title" and title_match:
107.                 results.append(book)
108.             elif normalized_field == "author" and author_match:
109.                 results.append(book)
110.             elif normalized_field == "both" and (title_match or author_match):
111.                 results.append(book)
112. 
113.         return results
114. 
115.     def add_rating(self, title: str, rating: int) -> bool:
116.         book = self.find_book_by_title(title)
117.         if not book:
118.             return False
119. 
120.         validated_rating = self._validate_rating(rating)
121.         book.ratings.append(validated_rating)
122.         self.save_books()
123.         return True
124. 
125.     def add_review(self, title: str, review: str) -> bool:
126.         book = self.find_book_by_title(title)
127.         if not book:
128.             return False
129. 
130.         validated_review = self._validate_text_input(review, "review")
131.         book.reviews.append(validated_review)
132.         self.save_books()
133.         return True
134. 
135.     def get_reviews(self, title: str) -> List[str]:
136.         book = self.find_book_by_title(title)
137.         if not book:
138.             return []
139.         return list(book.reviews)
140. 
141.     def get_average_rating(self, title: str) -> Optional[float]:
142.         book = self.find_book_by_title(title)
143.         if not book or not book.ratings:
144.             return None
145.         return sum(book.ratings) / len(book.ratings)
146. 
147.     @staticmethod
148.     def _validate_text_input(value: str, field_name: str) -> str:
149.         if not isinstance(value, str):
150.             raise ValueError(f"{field_name} must be a string")
151. 
152.         normalized_value = value.strip()
153.         if not normalized_value:
154.             raise ValueError(f"{field_name} cannot be empty")
155. 
156.         return normalized_value
157. 
158.     @staticmethod
159.     def _validate_year(year: int) -> int:
160.         if isinstance(year, bool) or not isinstance(year, int):
161.             raise ValueError("year must be an integer")
162.         if year < 0:
163.             raise ValueError("year cannot be negative")
164.         return year
165. 
166.     @staticmethod
167.     def _normalize_search_field(field: str) -> str:
168.         if not isinstance(field, str):
169.             raise ValueError("field must be 'title', 'author', or 'both'")
170.         return field.strip().lower()
171. 
172.     @staticmethod
173.     def _validate_rating(rating: int) -> int:
174.         if isinstance(rating, bool) or not isinstance(rating, int):
175.             raise ValueError("rating must be an integer")
176.         if rating < 1 or rating > 10:
177.             raise ValueError("rating must be between 1 and 10")
178.         return rating
179. 
180.     def _book_from_dict(self, raw_book: dict) -> Book:
181.         normalized_book = dict(raw_book)
182.         ratings = normalized_book.get("ratings", [])
183.         reviews = normalized_book.get("reviews", [])
184. 
185.         normalized_book["ratings"] = ratings if isinstance(ratings, list) else []
186.         normalized_book["reviews"] = reviews if isinstance(reviews, list) else []
187. 
188.         return Book(**normalized_book)
189.
```

</details>


---

<sub>⏱️ 1m 13s</sub>

### 💬 Copilot

下面是「新增一本書」寫入 `data.json` 的完整路徑：

1. 入口在 `book_app.py`  
   `main()` 讀 `sys.argv[1]`，如果是 `add`，就呼叫 `handle_add()`（`book_app.py:131-136,145-147`）。

2. 取得使用者輸入  
   `handle_add()` 用 `input()` 收 `Title/Author/Year`，並 `strip()` 去空白（`book_app.py:18-20`）。

3. 轉型與呼叫商業邏輯  
   `year_str` 轉成 `int`（空字串則給 `0`），接著呼叫 `collection.add_book(...)`（`book_app.py:23-24`）。

4. 驗證與建立資料  
   `books.py` 的 `add_book()` 會驗證：
   - title/author 不能空白（`_validate_text_input`）
   - year 必須是非負整數（`_validate_year`）  
   然後建立 `Book` dataclass，append 到 `self.books`（`books.py:41-47`）。

5. 寫入 `data.json`  
   `add_book()` 內呼叫 `save_books()`；`save_books()` 用 `json.dump([asdict(b) for b in self.books], ..., indent=2)` 寫到 `DATA_FILE = "data.json"`（`books.py:5,36-40,47`）。

補充：`collection` 是全域單例，程式啟動時就會 `load_books()` 先把既有 `data.json` 載入，新增時是在原集合上 append 後整包覆寫回檔案（`book_app.py:7`、`books.py:20-23`）。

---

<sub>⏱️ 1m 26s</sub>

### 👤 User

@samples/book-app-project/data.json 如果這個檔案遺失或損毀會發生什麼事？

---

<sub>⏱️ 1m 31s</sub>

### 💬 Copilot

在這個專案裡，兩種情況都不會讓程式直接崩潰：

- **`data.json` 遺失**：`load_books()` 會捕捉 `FileNotFoundError`，把 `self.books` 設成空清單。使用者看到的是「空書庫」。
- **`data.json` 損毀（非合法 JSON）**：會捕捉 `json.JSONDecodeError`，印出警告：`Warning: data.json is corrupted...`，然後一樣從空清單開始。

之後只要執行會觸發 `save_books()` 的操作（例如 `add`），就會重新建立/覆寫 `data.json`。

---

<sub>⏱️ 2m 11s</sub>

### ℹ️ Info

Environment loaded: 1 custom instruction, 1 MCP server, 4 skills, 3 agents, Visual Studio Code connected

---

<sub>⏱️ 2m 42s</sub>

### 👤 User

@samples/book-app-project/books.py @samples/book-app-project/utils.py 建議 a consistent error-handling strategy that works across both files.

---

<sub>⏱️ 2m 46s</sub>

### 💬 Copilot

我先快速看 `utils.py`，再給你一套可直接套在 `books.py` + `utils.py` 的一致錯誤處理策略。

---

<sub>⏱️ 2m 47s</sub>

### ✅ `view`

**view the file at C:\Copilot_learn\copilot-cli-for-beginners\samples\book-app-project\utils.py.**

C:\Copilot_learn\copilot-cli-for-beginners\samples\book-app-project\utils.py

<details>
<summary>63 lines</summary>

```
1. 
2. def print_menu():
3.     print("\n📚 Book Collection App")
4.     print("1. Add a book")
5.     print("2. List books")
6.     print("3. Mark book as read")
7.     print("4. Remove a book")
8.     print("5. Exit")
9. 
10. 
11. def get_user_choice() -> str:
12.     while True:
13.         choice = input("Choose an option (1-5): ").strip()
14.         if not choice:
15.             print("Input cannot be empty. Please enter a number.")
16.             continue
17.         if not choice.isdigit():
18.             print("Invalid input. Please enter a number.")
19.             continue
20.         return choice
21. 
22. 
23. def get_book_details():
24.     """Collect book details from user input with basic validation.
25. 
26.     Parameters:
27.         None: This function does not accept parameters. It prompts the user
28.         interactively via standard input.
29. 
30.     Returns:
31.         tuple[str, str, int]: A tuple containing:
32.             - title (str): Non-empty book title entered by the user.
33.             - author (str): Author name entered by the user (may be empty).
34.             - year (int): Publication year converted to an integer. If the
35.               entered value is invalid, defaults to 0.
36.     """
37.     while True:
38.         title = input("Enter book title: ").strip()
39.         if title:
40.             break
41.         print("Title cannot be empty. Please enter a title.")
42.     author = input("Enter author: ").strip()
43. 
44.     year_input = input("Enter publication year: ").strip()
45.     try:
46.         year = int(year_input)
47.     except ValueError:
48.         print("Invalid year. Defaulting to 0.")
49.         year = 0
50. 
51.     return title, author, year
52. 
53. 
54. def print_books(books):
55.     if not books:
56.         print("No books in your collection.")
57.         return
58. 
59.     print("\nYour Books:")
60.     for index, book in enumerate(books, start=1):
61.         status = "✅ Read" if book.read else "📖 Unread"
62.         print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
63.
```

</details>


---

<sub>⏱️ 2m 47s</sub>

### ✅ `view`

**view the file at C:\Copilot_learn\copilot-cli-for-beginners\samples\book-app-project\books.py.**

C:\Copilot_learn\copilot-cli-for-beginners\samples\book-app-project\books.py (lines 1-189)

<details>
<summary>189 lines</summary>

```
1. import json
2. from dataclasses import dataclass, asdict, field
3. from typing import List, Optional
4. 
5. DATA_FILE = "data.json"
6. VALID_SEARCH_FIELDS = {"title", "author", "both"}
7. 
8. 
9. @dataclass
10. class Book:
11.     title: str
12.     author: str
13.     year: int
14.     read: bool = False
15.     ratings: List[int] = field(default_factory=list)
16.     reviews: List[str] = field(default_factory=list)
17. 
18. 
19. class BookCollection:
20.     def __init__(self):
21.         self.books: List[Book] = []
22.         self.load_books()
23. 
24.     def load_books(self) -> None:
25.         """Load books from the JSON file if it exists."""
26.         try:
27.             with open(DATA_FILE, "r", encoding="utf-8") as f:
28.                 data = json.load(f)
29.                 self.books = [self._book_from_dict(b) for b in data]
30.         except FileNotFoundError:
31.             self.books = []
32.         except json.JSONDecodeError:
33.             print("Warning: data.json is corrupted. Starting with empty collection.")
34.             self.books = []
35. 
36.     def save_books(self) -> None:
37.         """Save the current book collection to JSON."""
38.         with open(DATA_FILE, "w", encoding="utf-8") as f:
39.             json.dump([asdict(b) for b in self.books], f, indent=2)
40. 
41.     def add_book(self, title: str, author: str, year: int) -> Book:
42.         validated_title = self._validate_text_input(title, "title")
43.         validated_author = self._validate_text_input(author, "author")
44.         validated_year = self._validate_year(year)
45.         book = Book(title=validated_title, author=validated_author, year=validated_year)
46.         self.books.append(book)
47.         self.save_books()
48.         return book
49. 
50.     def list_books(self) -> List[Book]:
51.         return self.books
52. 
53.     def find_book_by_title(self, title: str) -> Optional[Book]:
54.         if not isinstance(title, str) or not title.strip():
55.             return None
56. 
57.         normalized_title = title.strip().lower()
58.         for book in self.books:
59.             if book.title.lower() == normalized_title:
60.                 return book
61.         return None
62. 
63.     def mark_as_read(self, title: str) -> bool:
64.         book = self.find_book_by_title(title)
65.         if book:
66.             book.read = True
67.             self.save_books()
68.             return True
69.         return False
70. 
71.     def remove_book(self, title: str) -> bool:
72.         """Remove a book by title."""
73.         book = self.find_book_by_title(title)
74.         if book:
75.             self.books.remove(book)
76.             self.save_books()
77.             return True
78.         return False
79. 
80.     def find_by_author(self, author: str) -> List[Book]:
81.         """Find all books by a given author."""
82.         if not isinstance(author, str) or not author.strip():
83.             return []
84. 
85.         normalized_author = author.strip().lower()
86.         return [b for b in self.books if b.author.lower() == normalized_author]
87. 
88.     def search_books(self, query: str, field: str = "both") -> List[Book]:
89.         """Search books by title, author, or both using case-insensitive partial match."""
90.         if not isinstance(query, str):
91.             raise ValueError("query must be a string")
92. 
93.         normalized_query = query.strip().lower()
94.         if not normalized_query:
95.             return []
96. 
97.         normalized_field = self._normalize_search_field(field)
98.         if normalized_field not in VALID_SEARCH_FIELDS:
99.             raise ValueError("field must be 'title', 'author', or 'both'")
100. 
101.         results: List[Book] = []
102.         for book in self.books:
103.             title_match = normalized_query in book.title.lower()
104.             author_match = normalized_query in book.author.lower()
105. 
106.             if normalized_field == "title" and title_match:
107.                 results.append(book)
108.             elif normalized_field == "author" and author_match:
109.                 results.append(book)
110.             elif normalized_field == "both" and (title_match or author_match):
111.                 results.append(book)
112. 
113.         return results
114. 
115.     def add_rating(self, title: str, rating: int) -> bool:
116.         book = self.find_book_by_title(title)
117.         if not book:
118.             return False
119. 
120.         validated_rating = self._validate_rating(rating)
121.         book.ratings.append(validated_rating)
122.         self.save_books()
123.         return True
124. 
125.     def add_review(self, title: str, review: str) -> bool:
126.         book = self.find_book_by_title(title)
127.         if not book:
128.             return False
129. 
130.         validated_review = self._validate_text_input(review, "review")
131.         book.reviews.append(validated_review)
132.         self.save_books()
133.         return True
134. 
135.     def get_reviews(self, title: str) -> List[str]:
136.         book = self.find_book_by_title(title)
137.         if not book:
138.             return []
139.         return list(book.reviews)
140. 
141.     def get_average_rating(self, title: str) -> Optional[float]:
142.         book = self.find_book_by_title(title)
143.         if not book or not book.ratings:
144.             return None
145.         return sum(book.ratings) / len(book.ratings)
146. 
147.     @staticmethod
148.     def _validate_text_input(value: str, field_name: str) -> str:
149.         if not isinstance(value, str):
150.             raise ValueError(f"{field_name} must be a string")
151. 
152.         normalized_value = value.strip()
153.         if not normalized_value:
154.             raise ValueError(f"{field_name} cannot be empty")
155. 
156.         return normalized_value
157. 
158.     @staticmethod
159.     def _validate_year(year: int) -> int:
160.         if isinstance(year, bool) or not isinstance(year, int):
161.             raise ValueError("year must be an integer")
162.         if year < 0:
163.             raise ValueError("year cannot be negative")
164.         return year
165. 
166.     @staticmethod
167.     def _normalize_search_field(field: str) -> str:
168.         if not isinstance(field, str):
169.             raise ValueError("field must be 'title', 'author', or 'both'")
170.         return field.strip().lower()
171. 
172.     @staticmethod
173.     def _validate_rating(rating: int) -> int:
174.         if isinstance(rating, bool) or not isinstance(rating, int):
175.             raise ValueError("rating must be an integer")
176.         if rating < 1 or rating > 10:
177.             raise ValueError("rating must be between 1 and 10")
178.         return rating
179. 
180.     def _book_from_dict(self, raw_book: dict) -> Book:
181.         normalized_book = dict(raw_book)
182.         ratings = normalized_book.get("ratings", [])
183.         reviews = normalized_book.get("reviews", [])
184. 
185.         normalized_book["ratings"] = ratings if isinstance(ratings, list) else []
186.         normalized_book["reviews"] = reviews if isinstance(reviews, list) else []
187. 
188.         return Book(**normalized_book)
189.
```

</details>


---

<sub>⏱️ 2m 53s</sub>

### 💬 Copilot

很好的問題。現在兩檔風格有點混：`books.py` 有時 `raise`、有時 `print`；`utils.py` 會直接 `print` 並默默 fallback（如 year=0）。

我建議統一成「**分層處理**」：

- `books.py`（domain/data）：**不印訊息**，只 `raise` 明確例外（`ValidationError`, `StorageError`, `DataCorruptionError`）。
- `utils.py`（UI/input）：負責 `input`、重試、顯示錯誤訊息。
- 禁止 silent fallback（例如無效年份不要自動 0，改為重輸入）。
- 錯誤訊息格式一致：`Error: \<原因\>`.
- `FileNotFoundError` 可視為正常初始化空集合；`JSONDecodeError` 回報為 corruption 例外，由 UI 決定提示與後續動作。

---

<sub>⏱️ 4m 14s</sub>

### ℹ️ Info

Share Command Usage:
/share [path] - Share session to a markdown file (defaults to current directory)
/share file [path] - Share session to a markdown file at the specified path
/share gist - Create a secret GitHub gist with the session content
/share file research [path] - Save research report to file
/share gist research - Share research report to gist
/share research [path] - Shorthand for /share file research

Examples:
/share - Share to copilot-session-\<id\>.md in current directory
/share ~/sessions/my-session.md - Share to specific file path
/share gist - Create a secret gist (requires login)
/share research - Save research report to file

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
