# Lab 6 Code and Branch Coverage

The [assigned spam scorer](https://github.com/SETAPESU26/L6_L7_33_spam_scoring/tree/main/lab6) is unchanged. Run the following in this directory with Python 3.12.

```sh
python -m pip install -r requirements.txt
python -m coverage run --include=spam_scoring.py -m pytest -q CodeCoverageTest_spam_scoring_application.py
python -m coverage report -m --fail-under=90
python -m coverage run --branch --include=spam_scoring.py -m pytest -q BranchCoverageTest_spam_scoring_application.py
python -m coverage report -m --fail-under=90
```

| Suite | Tests passed | Lines | Branches | Run evidence |
| --- | ---: | ---: | ---: | --- |
| Code coverage | 11 | 39/39 (100%) | | [Terminal image](evidence/line-coverage.png) |
| Branch coverage | 21 | 39/39 (100%) | 26/26 (100%) | [Terminal image](evidence/branch-coverage.png) |

The second suite checks link counts at 0, 1, 3, and 4, the sender-discount floor, classification at 4 and 8, and the exact inbox ratio boundaries of 20% and 50%. The images render the captured command output. Plain-text copies are in the same folder.
