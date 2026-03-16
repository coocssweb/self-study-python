# Project Structure

Scripts are organized into numbered folders by topic area. Within each folder, files are numbered sequentially and named after the concept they cover.

```
01/          — Python basics (data types, control flow)
  01_hello.py    Strings, numbers, type casting
  02_list.py     List operations and slicing
  03_tuple.py    Tuples
  04_dict.py     Dictionaries
  05_set.py      Sets and set operations
  06_if.py       Conditionals (if/elif/else)
  07_for.py      Loops (for, while, range)

02/          — Functions and iteration
  01_def.py      Functions (comprehensive: args, decorators, closures, etc.)
  02_yield.py    Generators and yield
  03_iter.py     Iterators (__iter__, __next__)
```

## Conventions

- Folder names: two-digit numbers (`01`, `02`, ...)
- File names: `{nn}_{concept}.py` where `nn` is a two-digit sequence number
- Each file is self-contained and runnable independently
- Output uses `print()` to demonstrate concepts inline
- Comments are written in Chinese (中文) for explanations; code identifiers are in English
- Longer files use section headers with `# ===` separator lines and numbered sections
