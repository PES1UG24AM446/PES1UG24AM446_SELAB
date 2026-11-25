# Lab 5 Static Code Analysis

The source is the [assigned address book](https://github.com/SETAPESU26/L5_27_address_book/tree/12f84cd2821f7a74712fa8755f095758391c4fac). The repository history records the baseline and the three tool-specific fixes. See the [issues table](issues.md), [reflection](reflection.md) and [before](reports/before/) and [after](reports/after/) reports.

```sh
python -m pip install pylint==4.1.4 bandit==1.9.4 flake8==7.5.0
python address_book.py
python -m pylint address_book.py
python -m bandit -r address_book.py
python -m flake8 address_book.py
```

The demonstration prints identical output before and after the fixes. It generates `contacts.csv` and `contacts.bak` in the working directory. The fixed backup format is JSON.
