# Reflection

(Edit these into your own words before submitting. Your handout PDF did not list the four questions, so these are the usual four for this lab. Replace them with the exact questions from your course portal if they differ.)

**1. Which issues were easiest and hardest to fix, and why?**
Flake8 issues were the easiest because each message names the exact line and the fix is mechanical, such as adding a space or splitting a line. Pylint renames needed more care because every caller had to be updated. The hardest was the Bandit pickle finding, since the real fix was changing the backup format to JSON, not just silencing the warning.

**2. Did any tool report a false positive, or did you disagree with a finding?**
The MD5 finding is arguably a false positive in spirit: `contact_id` is only a short label, not a security feature. I did not suppress it with `# nosec`. I passed `usedforsecurity=False`, which documents the intent. The hardcoded-password warning was valid in principle even though the variable was unused, because secrets in source code get committed and leaked.

**3. How did fixing one tool's issues affect the others?**
Fixing Bandit's MD5 warning made one line longer than 79 characters, which Flake8 then flagged. Renaming functions for Pylint also changed every call site. Rerunning all three tools after each change is necessary, not optional.

**4. How does static analysis improve code quality and maintainability, and what are its limits?**
It catches problems without running the code: unsafe deserialization, swallowed exceptions, inconsistent naming and style. It acts like a tireless reviewer and gives the team a shared standard. It cannot judge whether the program does the right thing, and it can produce warnings that need human judgment (like the MD5 case). It complements testing and code review, it does not replace them. Running it automatically in CI would stop these issues from reaching the main branch.
