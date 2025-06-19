# Solves Sudokus

A lot of the logical aspect of the code has been understood from the CS50 AI course; lecture 1: Knowledge. To learn more about ideas
related to this topic, see [this](https://www.youtube.com/watch?v=HWQLez87vqM). Lectures slides also available [here](https://cdn.cs50.net/ai/2020/spring/lectures/1/lecture1.pdf).

## Propositional Logic

A way to represent knowledge using boolean statements. These statements are communicated via symbols and operators.
Operators include the following:
- AND
- OR
- NOT
- Biconditional
- Implication

Consider the following statement:

> I'll go for a walk if I wake up early. This is an example of an implication.

Here, B, waking up early implies (->) A, going for a walk.

### Truth Tables

are used to represent all possible values a logical statement can equal by equating each term to be True or False.

Here's the Truth Table for the same.

| A        | B       | A -> B |
| -------- | ------- |--------|
| True     | True    | True   |
| True     | False   | True   |
| False    | True    | True   |
| False    | False   | False  |

Thus, A -> B is only False when A is True and B is False. (I know it can be a little confusing to get around to why A -> B is True when A is False)

Know, one way of evaluating long drawn out sentences is to form elaborate Truth tables for the same and it's only for a certain Truth value that the
expression shall resolve into a resulting True value.
This approach is called _Model Checking_. However, consider how the time complexity of the computation grows with increasingly many Propositional Symbols
and operators:
As each symbol can adopt 2 values, the total number of possibilities that need to be expresses to calculate a Truth table for n symbols is $2^n$ .
This method is thus expensive and inefficient. It should be noted that there exist a certain number of optimizations for this algorithm, (e.g., if additional)
information is available to us - like along with a complicated sentence, some smaller sentences which can be used to restrict the values of some symbols).
I believe these optimizations can greatly bring down the complexity by several degrees. I.e., $2 ^ n$ can be reduced to $2^{n/2}$ .

### Inference

Inference is the other powerful idea that perhaps thinks more like humans do.
It relies on manipulating certain operators in order to shape the entire sentence into a _Conjunctive Standard Form_ (CNF). Conjunction refers to the AND/Conjunction operator.
The idea is simple.

Sentences represented using some operators can also be represented alternatively via some other operators. Thus, the idea is to continue making inferences until
the entirety of the sentence is in CNF. Once in CNF, another crucial idea of inference can be used to the arrive at a desired result.

But first, what does the result look like? In the case of the Sudoku solver, each cell is represented via a Knowledge Base - i.e., a set of sentences.
The idea behind the inferences is to eliminate symbols so that the possible values the cell can hold may decrease. When there's only one possible value, the digit at the
cell has been found.

### Progress

Currently, the program can convert statements into CNF. The idea of resolving many statements into fewer symbols is now being looked at.

### 19th June:

Idea was to have grid as a global network and all the subclasses _Container_, _Rows_, _Columns_, _Boxes_ acess the cells inside grid via the index values -- so the subclasses only store indicies to the cells and no mutations are made in the sub-classes.

However, all of this is imported by the main file, so the global variable **grid** can no longer be accessed by these functions from the  main file. Thus, it becomes necessary to the take grid as an input whereever necessary and return the mutated grid which shall be assigned to a variable in the main file.


