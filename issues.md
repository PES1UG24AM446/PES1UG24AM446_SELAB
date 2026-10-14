# Issue Table - address_book.py

Line numbers refer to the ORIGINAL file. Ordered by severity (high/medium first).

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| B324 weak MD5 hash (High) | Security (Bandit) | 20 | `hashlib.md5()` flagged as a weak hash for security use. | Passed `usedforsecurity=False`, since the value is only a short display ID. Output unchanged (`ecc177`). |
| B301 / B403 unsafe pickle (Medium / Low) | Security (Bandit) | 3, 67 | `pickle.load` can execute arbitrary code if `contacts.bak` is tampered with. | Replaced `pickle` with `json` in `backup_book` and `restore_book`. Contacts are plain str/dict data, so JSON is a safe fit. |
| B105 hardcoded password (Low) | Security (Bandit) | 6 | `SYNC_PASSWORD = "contacts-demo"` stores a secret in source. | Read it from the `SYNC_PASSWORD` environment variable via `os.environ.get`. |
| Broad exception | Bug / Quality (Pylint W0718) | 35 | `except Exception` hides real errors. The only expected failure is a missing key. | Changed to `except KeyError`. |
| Range/len loop | Quality (Pylint C0200) | 49 | `for i in range(len(names))` is unidiomatic. | Used `enumerate(sorted(contacts), start=1)`. |
| Missing encoding | Bug (Pylint W1514) | 54 | `open()` without `encoding` depends on the OS default and can break non-ASCII names. | Added `encoding="utf-8"` to every `open()`. |
| Naming style | Style (Pylint C0103) | 11-65 | camelCase functions/arguments (`addContact`, `fullName`, `fileName`) break PEP 8. | Renamed to snake_case (`add_contact`, `full_name`, `file_name`) and updated all calls. |
| Missing docstrings | Docs (Pylint C0114 / C0116) | 1, 11-70 | No module or function docstrings. | Added a one-line docstring to the module and every function. |
| No main guard | Quality | 88 | `main()` runs on import, so importing the module has side effects. | Wrapped in `if __name__ == "__main__":`. |
| E225 missing whitespace | Style (Flake8) | 24 | `found=[]` | Changed to `found = []`. |
| E231 missing whitespace after comma | Style (Flake8) | 84 | `"| first:",sorted(...)` | Added a space after the comma. |
| E501 line too long | Style (Flake8) | 85 | 86 characters (limit 79). | Split the `print(...)` call over several lines. |

## Results

| Tool | Before | After |
| ---- | ------ | ----- |
| Pylint | 5.47 / 10 (28 messages) | 10.00 / 10 |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | No issues identified |
| Flake8 | 3 issues | 0 issues |

Program output is identical before and after the fixes.
