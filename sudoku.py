# This file is about the sudoku solver.abs

from resolve_knowledge import KnowledgeBase, resolve
from operations import Symbol, OR, NOT


def loadFile(filename):
    with open(filename) as f:
        data = f.read()
    # print(repr(data.split("\n")))
    return data.split("\n")

# loadFile("samples/sudoku1.txt")

class Cell:
    def __init__(self, value=None, possibilities=None, kb=None):
        """
        :param value: is either None or belonging to the class operations.Symbol
        Similarly, elim is either None or the Knowledge Base of the cell    
        """
        if value == ".":
            value = None
        if value is not None:
            value = int(value)
        self.value = value
        if possibilities is None:
            possibilities = [*range(Grid.size+1)]
        self.possibilities = possibilities
        if kb is None:
            kb = Grid.defaultBase(None)
        self.kb = kb
    
    def consider(self, proposition):
        """
        Applies proposition onto the knowledge base of the Cell
        and returns the probable numbers
        """
        # print("before adding", self.kb)
        self.kb.add(proposition)
        # print("after adding", self.kb)
        self.kb = resolve(self.kb)
        # print("after resolving", self.kb)
        self.possibilities = [int(i.content()) for i in self.kb.KB()[0]]
    
    def remove(self, num):
        assert num in self.possibilities
        del self.possibilities[self.possibilities.index(num)]

    def __str__(self):
        return [str(self.getValue()), "."][self.empty()]
    
    def __repr__(self):
        return str(self)
    
    def getValue(self):
        return self.value
    
    def setValue(self, num):
        assert type(num) is int, "Value being set must be an int" 
        self.value = num
        self.possibilities = []
        self.kb = KnowledgeBase(Symbol(num))

    def empty(self):
        return self.getValue() is None
    
    def couldHave(self, num):
        return num in self.possibilities


class Container:
    def __init__(self, index):
        """
        For boxes, index is a tuple    
        """
        self.index = index
        # These first two attributes have integer values
        self.avail = Grid.size
        self.missing = [*range(1, Grid.size+1)]
        # These are the indexes of the empty and filled cells
        # For box type containers, the index will by a tuple.
        # The index of the box itself is represented as the downward
        # and rightward distance of the top left cell of the box from the top-left
        # corner of the grid
        self.empty = [*range(1, Grid.size+1)]
        self.filled = []  # nothing's filled in the beginning
        self.filled_nums = {}
    
    def calcRelativeIndex(self):
        return self.getIndex()
    
    def string(self, grid):
        return str([grid.fetch(i) for i in self.cells])
    
    def getIndex(self):
        return self.index
    
    def numAvail(self):
        return self.avail
    
    def has(self, num):
        return num not in self.getMissing()
    
    def getMissing(self):
        return self.missing[:]
    
    def getEmtpy(self):
        return self.empty[:]
    
    def getFilled(self):
        return self.filled[:]
    
    def eliminate(self, num: int, grid, but_not=None):
        if but_not is None:
            but_not = []
        onlyPos = []
        print("value of", self.rep(grid), "before eliminating", num, ":")
        print([grid.fetch(elem).getValue() if elem not in self.getEmtpy() else grid.fetch(elem).possibilities for elem in self.cells])
        for empty in self.getEmtpy():
            if empty in but_not:
                continue
            if grid.fetch(empty) and grid.fetch(empty).couldHave(num):
                grid.g[empty[0]][empty[1]].consider(NOT(Symbol(num)))
                if len(grid.fetch(empty).possibilities) == 1:
                    onlyPos.append((empty, grid.fetch(empty).possibilities[0]))
        print("rows changed", type(self).__name__, "to", [grid.fetch(elem).getValue() if elem not in self.getEmtpy() else grid.fetch(elem).possibilities for elem in self.cells])
        print("only pos is", onlyPos)
        # print("GRID TYPE", type(grid))
        return grid, onlyPos

    
    def filledNums(self):
        return self.filled_nums
    
    def newVal(self, v, i):
        # print("tryna add", v, "in class", type(self).__name__, "index", i)
        # print("\twhat's empty", self.getEmtpy())
        if v in self.filledNums():
            raise ValueError("Number already present")
        elif self.numAvail() == 0:
            raise ValueError(self.__name__, self.getIndex(), "is full!")
        elif i not in self.getEmtpy():
            raise ValueError("index", i, "isn't empty!")
        self.filled_nums[v] = i
        del self.empty[self.getEmtpy().index(i)]
        self.filled.append(i)
        self.avail -= 1
        del self.missing[self.getMissing().index(v)]
    
    def rep(self, grid):
        indices = self.cells
        return f"{type(self).__name__}({[grid.fetch(i) for i in indices]})"


class Box(Container):
    def __init__(self, index):
        super().__init__(index)
        self.empty = [(i+index[0], j+index[1]) for i in range(Grid.size//3) for j in range(Grid.size//3)]
        # print("initialised box", self.empty)
        self.cells = self.empty[:]
    
    def rep(self, grid):
        """ 
        Represents the values of the box in a 1-dim list:
        left to right, top to bottom
        """
        indices = self.cells
        vals = [grid.fetch(i) for i in indices]
        return "Box("+str(vals)+")"
        # out += "\n".join(["\t"+str(vals[j*3:(j+1)//3]) for j in range(Grid.size//3)])
        # return out
    
    def string(self, grid):
        # print("str box calle this function")
        # print("going to convert box into string")
        out = "Box:\n"
        indices = self.cells
        vals = [grid.fetch(i) for i in indices]
        # return str(vals)
        out += "\n".join(["\t"+str(vals[(j*3):(j+1)*3]) for j in range(Grid.size//3)])
        return out
    
    def calcRelativeIndex(self):
        i = self.getIndex()
        return i[0]+i[1]//3


class Row(Container):
    def __init__(self, index):
        super().__init__(index)
        self.empty = [(index, i) for i in range(Grid.size)]
        self.cells = self.empty[:]


class Column(Container):
    def __init__(self, index):
        super().__init__(index)
        self.empty = [(i, index) for i in range(Grid.size)]
        self.cells = self.empty[:]

def init_containers():
    """
    returns rows, cols and boxes
    """
    cols = [Column(i) for i in range(Grid.size)]
    rows = [Row(i) for i in range(Grid.size)]
    boxes = [Box((i*3, j*3)) for i in range(Grid.size//3) for j in range(Grid.size//3)]
    print([[i.cells for i in boxes]])
    return rows, cols, boxes

def containersWithoutNum(containers, num):
    """
    Expects a list of containers of a single type.    
    """
    indicies = []
    for cont in containers:
        if not cont.has(num):
            indicies.append(cont.calcRelativeIndex())
    return indicies

def newValue(val, index, containers):
    """
    Expects containers to be a list of lists of containers arranged in the following order
    rows, cols and boxes
    """
    # print("val", val, "index", index)
    rows, cols, boxes = containers
    cols[index[1]].newVal(val, index)
    rows[index[0]].newVal(val, index)
    # print("boxes:", boxes, "\ntrying to add new value", val, "at index", index)
    # print("\taccessing index", (index[0]//3)*3+index[1]//3, "boxes", boxes[(index[0]//3)*3+index[1]//3])
    boxes[(index[0]//3)*3+index[1]//3].newVal(val, index)
    return [rows, cols, boxes]

def sameVert(indicies):
    """
    returns True if a set of indicies lie on the same row/col
    Assumes the indicies to lie in the same Box
    """
    if len(indicies) > 3:
        return False, None
    elif all([i[0] == indicies[0][0] for i in indicies]):
        return True, 1
    elif all([i[1] == indicies[0][1] for i in indicies]):
        return True, 0
    return False, None


class Grid:
    size = 9
    def __init__(self, g):
        """
        Take the grid and converts each cell into an instance of class Cell    
        """
        print("this is what came", g)
        r, c, b = init_containers()

        cells = []
        numMap = {i:[] for i in range(1, Grid.size+1)}
        for i in range(Grid.size):
            cells.append([])
            for j in range(Grid.size):
                # print("considering index", (i, j))
                cells[i].append(Cell(g[i][j] if i != "." else None))
                cell = g[i][j]
                if cell != ".":
                    # print("found to be non-empty, adding to all containers")
                    print("value being added at", (i, j), "is", int(cell))
                    numMap[int(cell)].append((i, j))
                    r, c, b = newValue(int(cell), (i, j), [r, c, b])
        self.numberMap = numMap
        self.container = [r, c, b]
        self.r = r
        self.c = c
        self.b = b
        print("*"*123, cells)
        self.g = cells
    
    def getNumMap(self):
        return self.numberMap.copy()
    
    def fetch(self, index):
        return self.getGrid()[index[0]][index[1]]
    
    def rows(self):
        return self.rows()
    
    def full(self):
        return all(all([self.fetch((i, j)).getValue() is not None]) for i in range(Grid.size) for j in range(Grid.size))
    
    def cols(self):
        return self.cols()
    
    def boxes(self):
        return self.boxes()

    def defaultBase(self):
        symbs = [Symbol(i) for i in range(1, Grid.size+1)]
        return KnowledgeBase(OR(*symbs))
    
    def getGrid(self):
        return self.g[:]
    
    def setVal(self, index, num):
        assert self.g[index[0]][index[1]].getValue() in [None, "."], f"Index {index} already has a value {self.fetch(index)}"
        self.numberMap[num].append(index)
        self.g[index[0]][index[1]].setValue(num)
    
    def __str__(self):
        g = self.getGrid()
        row_separator = "+".join(["-"*6 for i in range(3)])
        # A one liner stretched into multiple lines (just like that)
        r = "\n".join(
            [
                "\n".join([
                    "|".join(
                        [
                            " ".join(
                                [
                                    str(c) for c in g[j][i*3:(i+1)*3]
                                    ])+" "
                                for i in range(Grid.size // 3)
                            ]
                        ) for j in range(Grid.size)
                    ][k*3: (k+1)*3])+"\n"+row_separator for k in range(Grid.size//3) 
                ]
            )
        return r


if __name__ == "__main__":
    # Important! rows, cols and boxes are all lists now
    rows, cols, boxes = init_containers()
    symbols = [Symbol(i) for i in range(1, Grid.size+1)]


    d = loadFile("samples/sudoku1.txt")

    grid = Grid(d)
    c = Cell(None)
    print(c)
    print(c.kb)
    c.consider(NOT(Symbol(3)))
    print(sameVert([(0, 1), (3, 1), (6, 1)]))
    # print(c.possibilities)
    # print(repr(cols), repr(rows))
    # for box in boxes.values():
    #     print("printing box")
    #     print(str(box))
    # print(b.getGrid())





