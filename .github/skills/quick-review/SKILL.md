---
name: quick-review
description: quick-review Python 程式碼中的 bare except、缺少型別提示與不清晰的變數命名
---

# Quick Review

你是一個用來快速審查 Python 程式碼的技能。

當使用者要求你對某個 Python 檔案進行 quick review 時，請執行以下 3 點檢查清單：

1. 檢查是否有 `bare except`
   - 找出 `except:` 這種沒有指定例外型別的寫法
   - 建議改為明確的例外型別，例如 `except ValueError:` 或 `except Exception as e:`
   - 說明 bare except 可能會吞掉非預期錯誤，例如 `KeyboardInterrupt` 或 `SystemExit`

2. 檢查是否缺少型別提示
   - 找出沒有參數型別或回傳型別標註的函式
   - 特別注意公開函式、工具函式、資料轉換函式
   - 建議補上明確的 type hints

3. 檢查是否有不清晰的變數名稱
   - 找出名稱過短、語意不明或容易混淆的變數
   - 例如：`x`、`tmp`、`data2`、`val`
   - 如果該變數承載明確業務意義，請建議更具描述性的命名

## 使用方式

當使用者提出類似以下請求時，套用這個技能：

- Do a quick review of books.py
- 快速審查這個 Python 檔案
- 幫我檢查這份程式碼有沒有明顯問題
- Review this file for basic Python quality issues

## 回覆格式

請用以下格式輸出：

### Quick Review Summary
- 用一句話總結整體品質

### Findings

#### 1. Bare except
- 列出發現的位置
- 解釋問題
- 提供修正建議

#### 2. Missing type hints
- 列出缺少型別提示的函式
- 建議補上的型別

#### 3. Unclear variable names
- 列出不清晰的變數名稱
- 說明原因
- 提供更好的命名建議

### Recommended Next Steps
- 用 2 到 5 點列出最優先該修的項目

## 工作原則

- 只專注在這 3 類問題，不要擴大成完整 code review
- 回饋要簡潔、具體、可執行
- 優先指出最影響可讀性與維護性的問題
- 若沒有發現問題，也要明確說明「這 3 項未發現明顯問題」