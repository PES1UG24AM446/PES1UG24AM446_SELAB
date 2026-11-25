# Lab 7 Fuzzing for Input Validation

Python 3.12. This lab uses the [assigned spam-scoring module](https://github.com/SETAPESU26/L6_L7_33_spam_scoring/tree/main/lab7). The application and tests retain its filenames.

```sh
python -m pip install -r requirements.txt
python spam_scoring.py
python -m pytest -q test_spam_scoring.py
```

| Function | Baseline behavior | Updated contract |
| --- | --- | --- |
| `sender_domain` | Missing separators raised `IndexError`. Repeated separators and empty domains returned misleading results. | Return a lowercase domain for a simple address with one separator and nonempty domain labels. Return `None` for malformed and non-string values. |
| `first_link` | Text without a match raised `ValueError`. The parser included punctuation and failed to delimit tabs and newlines. | Return the first syntactically valid HTTP(S) URL in prose, or `None`. Trim surrounding prose punctuation and validate the host and optional port locally. |
| `shout_ratio` | Inputs with no letters divided by zero. | Return the fraction of alphabetic Unicode characters that are uppercase. Return `0.0` if the input has no letters or is a non-string. |

The same six Hypothesis properties produced five failures on the original script and all six passed on the fixed script. The properties cover structured valid inputs, arbitrary text, non-string values, and Unicode capitalization. The report includes rendered terminal captures and the raw logs are in [evidence](evidence/).
