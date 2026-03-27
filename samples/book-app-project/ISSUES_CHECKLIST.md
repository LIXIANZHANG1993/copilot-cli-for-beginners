# Book App Project - Issue Checklist

此清單為 `samples/book-app-project/` 全專案程式碼審查結果，依嚴重度分類。

## Critical

- [ ] 無

## High

- [ ] `utils.py:get_user_choice` 未限制輸入範圍為 `1-5`，`"0"`、`"6"`、`"99"` 會被接受，可能導致上層流程收到無效選單值。  
  位置：`samples/book-app-project/utils.py:11-20`

- [ ] `utils.py:get_book_details` 對無效年份直接 fallback 為 `0`，會吞掉輸入錯誤並寫入可疑資料（資料品質風險）。  
  位置：`samples/book-app-project/utils.py:44-49`

## Medium

- [ ] 型別註記不完整，降低可讀性與靜態檢查效益（例如 `show_help`、`main`、`print_menu`、`get_book_details`、`print_books`）。  
  位置：`samples/book-app-project/book_app.py:109,126`、`samples/book-app-project/utils.py:2,23,54`、`samples/book-app-project/books.py:20`

- [ ] `book_app.py:handle_remove` 無論是否真的刪除成功都輸出「Book removed if it existed.」，對使用者回饋不夠明確。  
  位置：`samples/book-app-project/book_app.py:33-37`

- [ ] `books.py:_book_from_dict` 對資料結構驗證不足；若 JSON 項目缺少必要欄位或型別錯誤，可能在 `Book(**normalized_book)` 觸發未預期例外。  
  位置：`samples/book-app-project/books.py:180-189`

## Low

- [ ] `book_app.py` 使用全域 `collection`，可測試性與可注入性較差（雖目前測試有 monkeypatch workaround）。  
  位置：`samples/book-app-project/book_app.py:6-7`

- [ ] `README.md` 已明示「input checking is weak」但未具體列出限制與已知邊界行為，對初學者除錯指引不足。  
  位置：`samples/book-app-project/README.md:12-15`

- [ ] 專案目錄包含 `__pycache__` 與 `.pytest_cache`（若被追蹤會造成雜訊）；建議確認 `.gitignore` 規則。  
  位置：`samples/book-app-project/__pycache__/`、`samples/book-app-project/.pytest_cache/`

## Testing Gaps (cross-cutting)

- [ ] 缺少 `get_user_choice` 範圍外輸入測試（`0`、`6`、`99`）。  
  位置：`samples/book-app-project/tests/test_utils.py`

- [ ] 缺少 `get_book_details` 年份邊界測試（負數、極大值、空字串/非數字的預期策略）。  
  位置：`samples/book-app-project/tests/test_utils.py`

- [ ] 缺少 `book_app.main` 未知命令與缺少參數分支的完整行為測試。  
  位置：`samples/book-app-project/tests/test_book_app.py`

## Summary

- High: 2
- Medium: 3
- Low: 3
- Testing gaps: 3
- Total actionable items: 11
