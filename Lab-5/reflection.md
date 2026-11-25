# Static Analysis Reflection

1. **Which fixes required the most judgment?** Spacing and line wrapping were local changes confirmed by Flake8. Switching backups from pickle to JSON changed the persisted format. The address book stores strings and dictionaries, so JSON preserves the current data model. The before and after demonstrations produced identical stdout and restored the same contacts from a backup created in each version. Older pickle backups are not compatible with the JSON reader.

2. **Which findings required interpretation?** Bandit flagged MD5. Here the hash produces a short display ID, so marking the call as non-security preserves the display value. This ID should carry no authentication or integrity guarantees. The hardcoded demo password was unnecessary in the source, and the fixed code reads it from the environment.

3. **How did the tools interact?** Addressing the MD5 finding made the hash expression longer. Splitting it into two lines kept the result legible and satisfied Flake8. The Pylint changes also affected call sites, so the same demonstration was run again after the renames.

4. **What can static analysis establish?** The final scans produced a 10.00 Pylint score and zero Bandit or Flake8 findings. The separate demonstration comparison checks observed behavior that the scans alone cannot establish, including the positive and negative paths through the address book.
