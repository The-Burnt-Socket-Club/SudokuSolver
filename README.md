# Solves Sudokus

As the name suggests, this program solves sudokus.
My first idea involved the use of propositional logic to try and rule out the often perplexing connections between various numbers at play in a sudoku game. For this, I refered to the following:

- [CS50 AI: Lecture 1 - Knowledge](https://www.youtube.com/watch?v=HWQLez87vqM)
- [And lecture slides for the same](https://cdn.cs50.net/ai/2020/spring/lectures/1/lecture1.pdf)

However, I soon realised that solving this problem was perhaps better suited to another approach - the idea of elimination and later, backtracking.

These ideas were simple enough for me to implement my algorithms for the same. Still, I'm grateful to [SudokuWiki.org by Andrew Stuart](https://www.sudokuwiki.org/sudoku.htm) for widening my perspective on solving sudokus.

Having said this, let's get on with the implementation.

## Running the program

Needs no installed libraries. So simply clone this repository from the command line, change directory and run.

```bash
git clone https://github.com/The-Burnt-Socket-Club/SudokuSolver

cd SudokuSolver

python solver.py
```

To input a sudoku to be solved, head over to the `samples` directory and create a new file with 9 characters on each row, each representing a row of characters of a sudoku puzzle.

**NOTE: Use `.` characters to represented empty cells**

Here's an example grid:

```json
.4..2.865
7..6.8...
1....47.2
.1874....
..52.96..
....8615.
9.15....6
...8.2..7
873.6..2.
```

Finally, change the filename parameter in the `loadData` function as part of this line of code (currently at the bottom of the file)

```python
grid = Grid(loadFile("samples/sudoku3.txt"))
```


## Logic behind the program

This is the most interesting bit. The process of creating this program itself required more debugging than actual coding. I grappled with new ideas like propositional logic and implemented classes with more rigour than ever before.

While I would consider the `Grid`, `Clause`, `Container`, `Cell`, etc. classes to contain numerous utilities which this program wouldn't have been complete about, the essense of the program lies in the lines within `solve.py`.

Here's the idea in brief:


```
1. Repeat (recursion) until not solved
2. Go through the numbers (most frequent first),
3.   look into the boxes where this number isn't present
4.     if there's a hidden single, add it and eliminate num from row/col/box
5.     otherwise, if there's a pointing pair, eliminate from row or col (no need to eliminate box)
6.       if elimination leads to a single, repeat elimination with new num. Repeat until the chain exhausts
7. If this results in a solution, return.
8. Having gone through all numbers, repeat entire the entire function,
9. However, if no new number's been added in the present cycle, guess a value and be ready to backtrack.
```


You're free to look through the code and ask about any part of it. Though, currently, it's quite messy with numerous commented/uncommented print statements sprawled about everywhere.

