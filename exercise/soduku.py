#   Soduku.py
#
#   By Angus Lin, 2022.04.16
import copy
from dataclasses import dataclass
import time
import os
from tkinter import Y


class soduku2:
    def __init__(self, puzzle: list) -> list:
        self._puzzle = copy.deepcopy(puzzle)
        self._avail = dict()
        self._trial = []
        self._coord = [(x, y) for x in range(9)
                       for y in range(9)]
        self.available()

    def isSolved(self) -> bool:
        """returns True if puzzle is solved, False otherwise
        """
        # sumcol = [0] * 9
        for row in self._puzzle:
            if sum(row) != 45:
                return False
        for col in zip(*self._puzzle):
            if sum(col) != 45:
                return False
        return True

    def solvedFail(self):
        for key in self._avail:
            if not self._avail[key]:
                raise ValueError(
                    f'Solution fails, ({key[0]},{key[1]}) has no available option.')

    def solve(self):
        while self.solve_fillsingle():
            pass
        self.solve_trial()
        print(f"Puzzle solved state : {self.isSolved()}")
        print(f"Puzzle failure : {self.solvedFail()}")

    def solve_trial(self) -> bool:
        """Try to fill in the puzzle one by one.
        """
        if self.isSolved():
            return True
        else:
            try:
                [x, y, data] = self.avail_first()
                self._trial.append([x, y, data, copy.deepcopy(
                    self._puzzle), copy.deepcopy(self._avail)])
                self.puzzle_fill(x, y, data)
                while self.solve_fillsingle():
                    if self.isSolved():
                        return True
                self.solve_trial()
            except ValueError:
                self.solve_revert()
                self.solve_trial()

    def solve_revert(self):
        """revert last trial
        """
        self._puzzle = copy.deepcopy(self._trial[-1][-2])
        self._avail = copy.deepcopy(self._trial[-1][-1])
        self._avail[(self._trial[-1][0], self._trial[-1]
                    [1])].remove(self._trial[-1][2])
        goback = not self._avail[(self._trial[-1][0], self._trial[-1][1])]
        self._trial.pop()
        if goback:
            self.solve_revert()

    def solve_fillsingle(self):
        """solve the puzzle by filling in only available option
        Returns: True if at least one fill, False otherwise
        """
        result = False
        for (i, j) in list(self._avail.keys()):
            if len(self._avail[(i, j)]) == 1:
                self.puzzle_fill(i, j, self._avail[(i, j)][0])
                result = True

        for q in range(9):
            countx = [(self.avail_row(q)).count(i+1) for i in range(9)]
            while 1 in countx:
                idx = countx.index(1)
                countx[idx] = 0
                for i in range(9):
                    if (q, i) in self._avail and (idx + 1) in self._avail[(q, i)]:
                        self.puzzle_fill(q, i, idx+1)
                        result = True
                        break

            county = [(self.avail_col(q)).count(i+1) for i in range(9)]
            while 1 in county:
                idx = county.index(1)
                county[idx] = 0
                for i in range(9):
                    if (i, q) in self._avail and (idx + 1) in self._avail[(i, q)]:
                        self.puzzle_fill(i, q, idx+1)
                        result = True
                        break

            countq = [(self.avail_q(q)).count(i+1) for i in range(9)]
            while 1 in countq:
                idx = countq.index(1)
                countq[idx] = 0
                for i in range((q // 3) * 3, (q // 3) * 3 + 3):
                    for j in range((q % 3) * 3, (q % 3)*3 + 3):
                        if (i, j) in self._avail and (idx+1) in self._avail[(i, j)]:
                            self.puzzle_fill(i, j, idx+1)
                            result = True
                            break
                    else:
                        continue
                    break
        return result

    def available(self):
        """generate available options for puzzle
        """
        for key in [(x, y) for x in range(9)
                    for y in range(9) if not self._puzzle[x][y]]:
            self._avail[key] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for (i, j) in self._coord:
            if self._puzzle[i][j]:
                self.puzzle_fill(i, j, self._puzzle[i][j])

    def avail_row(self, row) -> list:
        """return available options in row
        """
        result = []
        for i in range(9):
            if (row, i) in self._avail:
                result.extend(self._avail[(row, i)])
        return result

    def avail_col(self, col) -> list:
        """return available options in column
        """
        result = []
        for i in range(9):
            if (i, col) in self._avail:
                result.extend(self._avail[(i, col)])
        return result

    def avail_q(self, q) -> list:
        """return available options in quadrant q
        """
        result = []
        for i in range((q // 3) * 3, (q // 3) * 3 + 3):
            for j in range((q % 3) * 3, (q % 3) * 3 + 3):
                if (i, j) in self._avail:
                    result.extend(self._avail[(i, j)])
        return result

    def avail_remove(self, x: int, y: int, data: int):
        if (x, y) in self._avail:
            if data in self._avail[(x, y)]:
                self._avail[(x, y)].remove(data)
                if not self._avail[(x, y)]:
                    #   available option is empty => solve fail
                    raise ValueError(
                        f'Solution fails, ({x},{y}) has no available option.')

    def avail_first(self) -> list:
        """return first available option (x, y, data)
        """
        for (x, y) in self._avail:
            return ([x, y, self._avail[(x, y)][0]])

    def avail_print(self):
        """return available options in a string
        """
        result = ''
        for i in range(9):
            for j in range(9):
                temp = ''
                if (i, j) in self._avail:
                    for a in self._avail[(i, j)]:
                        temp += f'{a}'
                result += f'{temp: <9},'
            result += '\n'
        return result

    def puzzle_fill(self, x: int, y: int, data: int):
        if not data:
            return
        self._puzzle[x][y] = data
        if (x, y) in self._avail:
            self._avail.pop((x, y))
        try:
            for i in range(9):
                self.avail_remove(x, i, data)
                self.avail_remove(i, y, data)
                # if (x, i) in self._avail and (data in self._avail[(x, i)]):
                #     self._avail[(x, i)].remove(data)
                # if (i, y) in self._avail and (data in self._avail[(i, y)]):
                #     self._avail[(i, y)].remove(data)
            qx = x // 3
            qy = y // 3
            for i in range(qx*3, qx*3+3):
                for j in range(qy*3, qy*3+3):
                    self.avail_remove(i, j, data)
                    # if (i, j) in self._avail:
                    #     if data in self._avail[(i, j)]:
                    #         self._avail[(i, j)].remove(data)
        except:
            raise ValueError(
                f'Solution fails, ({x},{y}) has no available option.')

    def __str__(self) -> str:
        """Return the puzzle in string
        """
        result = ''
        for i, row in enumerate(self._puzzle):
            if i == 3 or i == 6:
                result += '\n'
            for j, item in enumerate(row):
                if j == 3 or j == 6:
                    result += ' '
                result += f'{item}' if item else '_'
            result += '\n'
            # result += f'{row[0]}{row[1]}{row[2]} {row[3]}{row[4]}{row[5]} {row[6]}{row[7]}{row[8]}\n'
        return result


class soduku:
    def __init__(self, puzzle) -> list:
        self._puzzle = copy.deepcopy(puzzle)
        self._avail = []
        self._trial = []
        self.available()

    def isSolved(self) -> bool:
        """returns True if puzzle is solved, False otherwise
        """
        # sumcol = [0] * 9
        for row in self._puzzle:
            if sum(row) != 45:
                return False
        for col in zip(*self._puzzle):
            if sum(col) != 45:
                return False
        return True

    def solvedFail(self) -> bool:
        """return True if the current puzzle cannot be solved, False otherwise
        """
        for i in range(9):
            for j in range(9):
                if (not self._puzzle[i][j]) and (not self._avail[i][j]):
                    return True
        return False

    def solve(self):
        """solve the soduku puzzle
        """
        while self.solve_fillsingle():
            pass
        while not self.isSolved():
            self.solve_trial()

        print(f"Puzzle solved state : {self.isSolved()}")
        print(f"Puzzle failure : {self.solvedFail()}")

    def available(self):
        """generate available options for puzzle
        """
        if not self._avail:
            # for j in range(9):
            #     self.avail.append([[1, 2, 3, 4, 5, 6, 7, 8, 9]
            #                       for i in range(9)])
            self._avail = [copy.deepcopy(
                [[1, 2, 3, 4, 5, 6, 7, 8, 9] for i in range(9)]) for j in range(9)]

            for i in range(9):
                for j in range(9):
                    if self._puzzle[i][j]:
                        self.puzzle_fill(i, j, self._puzzle[i][j])

    def avail_row(self, row) -> list:
        """return available options in row
        """
        result = []
        for i in range(9):
            result.extend(self._avail[row][i])
        return result

    def avail_col(self, col) -> list:
        """return available options in column
        """
        result = []
        for i in range(9):
            result.extend(self._avail[i][col])
        return result

    def avail_q(self, q) -> list:
        """return available options in quadrant q
        """
        result = []
        for i in range((q // 3) * 3, (q // 3) * 3 + 3):
            for j in range((q % 3) * 3, (q % 3) * 3 + 3):
                result.extend(self._avail[i][j])
        return result

    def avail_first(self):
        """return first available option (x, y, data)
        """
        for i in range(9):
            for j in range(9):
                if self._avail[i][j]:
                    return([i, j, self._avail[i][j][0]])

    def avail_print(self):
        """return available options in a string
        """
        result = ''
        for row in self._avail:
            for item in row:
                temp = ""
                for a in item:
                    temp += f'{a}'
                result += f'{temp: <9},'
            result += '\n'
        return result

    def solve_fillsingle(self):
        """solve the puzzle by filling in only available option
        Returns: True if at least one fill, False otherwise
        """
        result = False
        for i in range(9):
            for j in range(9):
                if len(self._avail[i][j]) == 1:
                    self.puzzle_fill(i, j, self._avail[i][j][0])
                    result = True
        for q in range(9):
            countx = [(self.avail_row(q)).count(i+1) for i in range(9)]
            while 1 in countx:
                idx = countx.index(1)
                countx[idx] = 0
                for i in range(9):
                    if (idx + 1) in self._avail[q][i]:
                        self.puzzle_fill(q, i, idx+1)
                        result = True
                        break

            county = [(self.avail_col(q)).count(i+1) for i in range(9)]
            while 1 in county:
                idx = county.index(1)
                county[idx] = 0
                for i in range(9):
                    if (idx + 1) in self._avail[i][q]:
                        self.puzzle_fill(i, q, idx+1)
                        result = True
                        break

            countq = [(self.avail_q(q)).count(i+1) for i in range(9)]
            while 1 in countq:
                idx = countq.index(1)
                countq[idx] = 0
                for i in range((q // 3) * 3, (q // 3) * 3 + 3):
                    for j in range((q % 3) * 3, (q % 3)*3 + 3):
                        if (idx+1) in self._avail[i][j]:
                            self.puzzle_fill(i, j, idx+1)
                            result = True
                            break
                    else:
                        continue
                    break
        return result

    def solve_trial(self) -> bool:
        """Try to fill in the puzzle one by one.
        """
        # try:
        if self.solvedFail():
            # #   solve fail, revert
            # self._puzzle = copy.deepcopy(self._trial[-1][-2])
            # self._avail = copy.deepcopy(self._trial[-1][-1])
            # self._avail[self._trial[-1][0]][self._trial[-1]
            #                                 [1]].remove(self._trial[-1][2])
            # self._trial.pop()
            pass
        else:
            [x, y, data] = self.avail_first()
            self._trial.append([x, y, data, copy.deepcopy(
                self._puzzle), copy.deepcopy(self._avail)])
            self.puzzle_fill(x, y, data)
            while self.solve_fillsingle():
                if self.isSolved():
                    return True
                if self.solvedFail():
                    #   solve fail, revert
                    self._puzzle = copy.deepcopy(self._trial[-1][-2])
                    self._avail = copy.deepcopy(self._trial[-1][-1])
                    self._avail[self._trial[-1][0]][self._trial[-1]
                                                    [1]].remove(self._trial[-1][2])
                    self._trial.pop()
                else:
                    self.solve_trial()
        # except:
        #     self._puzzle = copy.deepcopy(self._trial[-1][-2])
        #     self._avail = copy.deepcopy(self._trial[-1][-1])
        #     self._avail[self._trial[-1][0]][self._trial[-1]
        #                                     [1]].remove(self._trial[-1][2])
        #     self._trial.pop()

    def puzzle_fill(self, x: int, y: int, data: int):
        """fill x,y of the puzzle with data, update available accordingly
        """
        if not data:
            return
        self._puzzle[x][y] = data
        self._avail[x][y] = []
        for i in range(9):
            if data in self._avail[x][i]:
                (self._avail[x][i]).remove(data)
            if data in self._avail[i][y]:
                (self._avail[i][y]).remove(data)
        qx = x // 3
        qy = y // 3
        for i in range(qx*3, qx*3+3):
            for j in range(qy*3, qy*3+3):
                if data in self._avail[i][j]:
                    (self._avail[i][j]).remove(data)

    def __str__(self) -> str:
        """Return the puzzle in string
        """
        result = ''
        for i, row in enumerate(self._puzzle):
            if i == 3 or i == 6:
                result += '\n'
            for j, item in enumerate(row):
                if j == 3 or j == 6:
                    result += ' '
                result += f'{item}' if item else '_'
            result += '\n'
            # result += f'{row[0]}{row[1]}{row[2]} {row[3]}{row[4]}{row[5]} {row[6]}{row[7]}{row[8]}\n'
        return result


def main(fname=""):
    puzzle = []
    if fname:
        with open(fname, 'r') as f:
            for line in f:
                puzzle.append([])
                for n, j in enumerate(line):
                    if n > 8:
                        break
                    if j == '_':
                        puzzle[-1].append(0)
                    else:
                        puzzle[-1].append(int(j))
        f.close()
    else:
        puzzle = [[0, 2, 0, 5, 0, 1, 0, 9, 0],
                  [8, 0, 0, 2, 0, 3, 0, 0, 6],
                  [0, 3, 0, 0, 6, 0, 0, 7, 0],
                  [0, 0, 1, 0, 0, 0, 6, 0, 0],
                  [5, 4, 0, 0, 0, 0, 0, 1, 9],
                  [0, 0, 2, 0, 0, 0, 7, 0, 0],
                  [0, 9, 0, 0, 3, 0, 0, 8, 0],
                  [2, 0, 0, 8, 0, 4, 0, 0, 7],
                  [0, 1, 0, 9, 0, 7, 0, 6, 0]]
        answer = [[4, 2, 6, 5, 7, 1, 3, 9, 8],
                  [8, 5, 7, 2, 9, 3, 1, 4, 6],
                  [1, 3, 9, 4, 6, 8, 2, 7, 5],
                  [9, 7, 1, 3, 8, 5, 6, 2, 4],
                  [5, 4, 3, 7, 2, 6, 8, 1, 9],
                  [6, 8, 2, 1, 4, 9, 7, 5, 3],
                  [7, 9, 4, 6, 3, 2, 5, 8, 1],
                  [2, 6, 5, 8, 1, 4, 9, 3, 7],
                  [3, 1, 8, 9, 5, 7, 4, 6, 2]]
    starttime = time.time()
    # solver = soduku(puzzle)
    # print(solver)
    # solver.solve()
    solver = soduku2(puzzle)
    solver.solve()
    endtime = time.time()
    print(solver)
    print('\n')
    print(f'time taken = {endtime - starttime} seconds')

    starttime = time.time()
    solver = soduku(puzzle)
    solver.solve()
    endtime = time.time()
    print(solver)
    print('\n')
    print(f'time taken = {endtime - starttime} seconds')


if __name__ == "__main__":
    os.chdir('//home//al//project//VSCode//exercise')
    main('test1.txt')
