# concordance
Generates a concordance (list of all words, their frequencies, and sentence positions) of a passed text

To run this program, call the following in the command line:

- For default input and output files:
  - `python -m concordance.src.Main`
- For specific input and output files:
  - `python -m concordance.src.Main $INPUT_FILE $OUTPUT_FILE`
- For tests, run any of the following:
  - `python -m concordance.test.MainTest`
  - `python -m concordance.test.RegexerTest`
  - `python -m concordance.test.ConcordanceObjTest`

There were a few things that I could have written to make this a cleaner final product, but I felt were out-of-scope for a small project. Here are some examples:

1. Spacing of the final concordance just uses tabs, but I could've used python libraries like `rjust` to preserve column spacing. However, testing this would take a lot of time and would likely not show up on different environments correctly anyway.
2. I use some simple arguments for file entry into `main()`. This could be much cleaner using Python's `argparse` library, but it would mostly be boiler-plate code that doesn't tell much about my software style.
3. All main functionality exists in one .py file. While in a production environment, I would split the objects into separate files, I didn't see this as necessary in a small project (as long as the implementation is itself Object-Oriented).
4. Handling words like "assoc.", short for "association". I didn't think there was a way to handle this issue without looking up shortened words in an existing dataset or online dictionary. So, "assoc." becomes "assoc".
5. I assumed that while there may be very large files, they will not exceed Python's built-in string length (or amount of data which can be maximally grabbed with a `read()` call). This could be handled with a `readline()` call and buffering the size of the received data. However, this would add to the complexity of reading sentences (since a sentence could span two or more lines) and I felt this wasn't the core question asked by the problem. In a more robust application for this problem, I would definitely account for this possibility.
