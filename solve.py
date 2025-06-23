# This one actually solves sudokus

from sudoku import *
import copy



def main(grid, containers):
    def handle_new_vals(index, num):
        nonlocal grid, rows, cols, boxes
        global steps
        print("adding value", num, "at index", index)
        grid.setVal(index, num)
        # print("new grid:")
        print(grid)
        steps += 1
        rows, cols, boxes = newValue(num, index, [rows, cols, boxes])
        #print(rows[index[0]].rep(grid))
        #print([grid.fetch(elem).getValue() if elem not in rows[index[0]].getEmtpy() else grid.fetch(elem).possibilities for elem in rows[index[0]].cells])
        #print(cols[index[1]].rep(grid))
        #print([grid.fetch(elem).getValue() if elem not in cols[index[1]].getEmtpy() else grid.fetch(elem).possibilities for elem in cols[index[1]].cells])
        #print(boxes[(index[0]//3)*3+index[1]//3].rep(grid))
        #print([grid.fetch(elem).getValue() if elem not in boxes[(index[0]//3)*3+index[1]//3].getEmtpy() else grid.fetch(elem).possibilities for elem in boxes[(index[0]//3)*3+index[1]//3].cells])

        # looking for onlyPos values due to eliminations of all other numbers
        grid, onlyPos1 = rows[index[0]].eliminate(num, grid)
        #print("row found", onlyPos1)
        grid, onlyPos2 = cols[index[1]].eliminate(num, grid)
        #print(cols[index[1]].rep(grid))
        #print("col found", onlyPos2)
        grid, onlyPos3 = boxes[(index[0]//3)*3+index[1]//3].eliminate(num, grid)
        #print("box found", onlyPos3)
        # if len(rows[index[0]].getMissing()) == 1:
        #     assert len(rows[index[0]].getEmtpy()) == 1, "number empty and missing don't match"
        #     handle_new_vals(rows[index[0]].getEmtpy()[0], rows[index[0]].getMissing()[0])
        # if len(cols[index[1]].getMissing()) == 1:
        #     assert len(cols[index[1]].getEmtpy()) == 1, "number empty and missing don't match"
        #     handle_new_vals(cols[index[1]].getEmtpy()[0], cols[index[1]].getMissing()[0])
        # if len(boxes[(index[0]//3)*3+index[1]//3].getMissing()) == 1:
        #     assert len(boxes[(index[0]//3)*3+index[1]//3].getEmtpy()) == 1, "number empty and missing don't match"
        #     handle_new_vals(boxes[(index[0]//3)*3+index[1]//3].getEmtpy()[0], boxes[(index[0]//3)*3+index[1]//3].getMissing()[0])
        for i in list(set(onlyPos1+onlyPos2+onlyPos3)):
            #print("sent by the onlyPos ones")
            handle_new_vals(i[0], i[1])
    # rows, cols, boxes -> lists
    # step 1:
    global steps
    if steps % 500 < 10:
        print(steps)
    if steps >= 3500:
        exit()
    rows, cols, boxes = containers
    og = grid.getNumMap()
    # print("Type of grid", type(grid))
    #print("Original Puzzle:\n", grid)
    #print("looping through numbers in the order", sorted(grid.getNumMap().keys(), key=lambda x: len(grid.getNumMap()[x]), reverse=True))
    for num in sorted(grid.getNumMap().keys(), key=lambda x: len(grid.getNumMap()[x]), reverse=True):
        #print("\tnumber", num, "... getting boxes", containersWithoutNum(boxes, num))
        # print("\tnumber", num, "grid type", type(grid))
        for box in containersWithoutNum(boxes, num):
            # print("\tinside box", boxes[box], "grid type", type(grid))
            # print("num", num, "doesn't exist in box", boxes[box].getIndex(), boxes[box].rep(grid))
            pos = []
            #print("\tlooping through values in box", boxes[box].rep(grid))
            for empty in boxes[box].getEmtpy():
                if not cols[empty[1]].has(num) and not rows[empty[0]].has(num) and num in grid.fetch(empty).possibilities:
                    # print(empty, "could have num", type(grid))
                    pos.append(empty)
                else:
                    # print(empty, "couldn't have num", type(grid))
                    if grid.fetch(empty).couldHave(num):
                        # print("\t", empty, "thinks it could have it. correct it.", type(grid))
                        grid.g[empty[0]][empty[1]].consider(NOT(Symbol(num)))
            # print("num could be in the following indexes", pos, "box", boxes[box].rep(grid))
            #print("\tadded", pos)
            if len(pos) == 1:
                # print("only one solution")
                # print("type of grid before new_val", type(grid))
                #print("sending handle val")
                handle_new_vals(pos[0], num)
                # print("type of grid after new_val", type(grid))
                # print("checking if row/col/box has only one value left")
                index = pos[0]
                if len(rows[index[0]].getMissing()) == 1:
                    #print("sent by the row one")
                    assert len(rows[index[0]].getEmtpy()) == 1, "number empty and missing don't match"
                    handle_new_vals(rows[index[0]].getEmtpy()[0], rows[index[0]].getMissing()[0])
                if len(cols[index[1]].getMissing()) == 1:
                    #print("sent by the col one")
                    assert len(cols[index[1]].getEmtpy()) == 1, "number empty and missing don't match"
                    handle_new_vals(cols[index[1]].getEmtpy()[0], cols[index[1]].getMissing()[0])
                if len(boxes[(index[0]//3)*3+index[1]//3].getMissing()) == 1:
                    #print("sent by the box one")
                    assert len(boxes[(index[0]//3)*3+index[1]//3].getEmtpy()) == 1, "number empty and missing don't match"
                    handle_new_vals(boxes[(index[0]//3)*3+index[1]//3].getEmtpy()[0], boxes[(index[0]//3)*3+index[1]//3].getMissing()[0])
                continue
            vert_check = sameVert(pos)
            if vert_check[0]:   # if they lie on the same vertical,
                #print("\tpos", pos, "happen to lie on a vertical... eliminating",)
                # print("GOING TO ELIMINATE")
                if vert_check[1] == 1:
                    grid, onlyPos = rows[pos[0][0]].eliminate(num, grid, pos)
                else:
                    grid, onlyPos = cols[pos[0][1]].eliminate(num, grid, pos)
    # print("FULL?", grid.full())
    if grid.full():
        print("final steps:", steps)
        return grid
    if grid.getNumMap() == og:
        #print("NOTHING'S CHANGED THIS LOOP => BACKTRACKING METHOD TIME")
        # for i in range(Grid.size):
            #print(rows[i].rep(grid))
            #print([grid.fetch(elem).getValue() if elem not in rows[i].getEmtpy() else grid.fetch(elem).possibilities for elem in rows[i].cells])
        print("going to make a guess. least val:")
        index, least, pos_s = grid.leastPos()
        print("\t", index, least, pos_s)
        val = 1
        #print("leastval returned", index, least, pos_s)
        for pos in pos_s:
            # print("before guess")
            # print(grid)
            print(f"guessing...({val}) ..", pos, "at index", index)
            # new_grid = Grid(None, [grid.getGrid()[:], grid.getNumMap().copy(), grid.getContainer()[:]])
            nrow, ncol, nbox = [copy.deepcopy(i) for i in [rows, cols, boxes]]
            new_grid = copy.deepcopy(grid)
            #print("id match", id(new_grid), id(grid))
            #print("copy\n", new_grid)
            #print("here's the new grid:")
            #print(new_grid, id(new_grid), id(grid))
            # print(grid)
            #print("after", new_grid)
            try:
                handle_new_vals(index, pos)
                print("added number")
                return main(grid, [rows, cols, boxes])
            except IndexError as ind_err:
                raise IndexError(ind_err)
            except Exception as e:
                # print("Error:", e)
                if str(e) == "Number already present":
                    raise e
                if str(e) == "int() argument must be a string, a bytes-like object or a real number, not 'Symbol'":
                    raise e
                print("Num", pos, "at index", index, "caused exception:")
                print(grid)
                # print("swapping present grid value for the older new_grid value")
                # print("present grid", grid)
                # grid = Grid(None, [new_grid.getGrid()[:], new_grid.getNumMap().copy(), new_grid.getContainer()[:]])
                grid = copy.deepcopy(new_grid)
                rows, cols, boxes = [copy.deepcopy(i) for i in [nrow, ncol, nbox]]
                # print("older grid", grid)
                # print("backtracking... to:")
                val += 1
                # print(grid)
                steps += 1
                continue
        print("end backtrack...")
        # print(grid)
        raise ValueError("Okay, tried all possibilities after backtracking... No solution")


        # things didn't work out, proceed with guessing...
        # print(cols[index[1]].rep(grid))
        # print([grid.fetch(elem).getValue() if elem not in cols[index[1]].getEmtpy() else grid.fetch(elem).possibilities for elem in cols[index[1]].cells])
        # print(boxes[(index[0]//3)*3+index[1]//3].rep(grid))
        # print([grid.fetch(elem).getValue() if elem not in boxes[(index[0]//3)*3+index[1]//3].getEmtpy() else grid.fetch(elem).possibilities for elem in boxes[(index[0]//3)*3+index[1]//3].cells])
        return grid
    elif not grid.full():
        #print("FIRST LOOP Completed")
        return main(grid, [rows, cols, boxes])
    return grid


grid = Grid(loadFile("samples/sudoku5.txt"))
rows, cols, boxes = grid.container[:]
steps = 0
print(grid.getNumMap())
print(main(grid, [rows, cols, boxes]))
# print(grid)
# print("rows", [i.rep(grid) for i in rows])
# print("cols", [i.rep(grid) for i in cols])
# print("boxes", [i.rep(grid) for i in boxes])

