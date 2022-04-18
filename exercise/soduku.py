#   Soduku.py
#
#   By Angus Lin, 2022.04.16

class soduku:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.avail = []

    def isSolved(self):
        pass

    def solve(self):
        while self.solve_fillsingle():
            pass

    def available(self):
        if not self.avail:
            for i in range(0, 9):
                self.avail.append([])
                for j in range(0, 9):
                    if self.puzzle[i][j]:
                        self.avail[i].append([])
                    else:
                        self.avail[i].append([1, 2, 3, 4, 5, 6, 7, 8, 9])
            for i in range(9):
                for j in range(9):
                    if self.puzzle[i][j]:
                        self.puzzle_fill(i, j, self.puzzle[i][j])

    def avail_row(self, row):
        result = []
        for i in range(9):
            result.extend(self.avail[row][i])
        return result

    def avail_col(self, col):
        result = []
        for i in range(9):
            result.extend(self.avail[i][col])
        return result

    def avail_q(self, q):
        result = []
        for i in range((q // 3) * 3, (q // 3) * 3 + 3):
            for j in range((q % 3) * 3, (q % 3) * 3 + 3):
                result.extend(self.avail[i][j])
        return result

    def solve_fillsingle(self):
        result = False
        for i in range(9):
            for j in range(9):
                if len(self.avail[i][j]) == 1:
                    self.puzzle_fill(i, j, self.avail[i][j][0])
                    result = True
        for q in range(9):
            print(f'processing {q}...')
            countx = [(self.avail_row(q)).count(i+1) for i in range(9)]
            while 1 in countx:
                idx = countx.index(1)
                countx[idx] = 0
                for i in range(9):
                    if (idx + 1) in self.avail[q][i]:
                        self.puzzle_fill(q, i, idx+1)
                        result = True
                        break
            print(self)
            print(self.avail_print())

            county = [(self.avail_col(q)).count(i+1) for i in range(9)]
            while 1 in county:
                idx = county.index(1)
                county[idx] = 0
                for i in range(9):
                    if (idx + 1) in self.avail[i][q]:
                        self.puzzle_fill(i, q, idx+1)
                        result = True
                        break

            print(self)
            print(self.avail_print())
            print(self.avail_q(q))
            countq = [(self.avail_q(q)).count(i+1) for i in range(9)]
            print(countq)
            while 1 in countq:
                idx = countq.index(1)
                countq[idx] = 0
                for i in range((q // 3) * 3, (q // 3) * 3 + 3):
                    for j in range((q % 3) * 3, (q % 3)*3 + 3):
                        if (idx+1) in self.avail[i][j]:
                            self.puzzle_fill(i, j, idx+1)
                            result = True
                            break
                    else:
                        continue
                    break
            print(self)
            print(self.avail_print())
        return result

    def puzzle_fill(self, x, y, data):
        """
        """
        if not data:
            return
        print(f"filling {x}{y} with {data}")
        self.puzzle[x][y] = data
        self.avail[x][y] = []
        for i in range(9):
            if data in self.avail[x][i]:
                (self.avail[x][i]).remove(data)
            if data in self.avail[i][y]:
                (self.avail[i][y]).remove(data)
        qx = x // 3
        qy = y // 3
        for i in range(qx*3, qx*3+3):
            for j in range(qy*3, qy*3+3):
                if data in self.avail[i][j]:
                    (self.avail[i][j]).remove(data)

    def avail_print(self):
        result = ''
        for row in self.avail:
            for item in row:
                temp = ""
                for a in item:
                    temp += f'{a}'
                result += f'{temp: <9},'
            result += '\n'
        return result

    def avail_del(self, x, y, data):
        pass

    def __str__(self):
        result = ''
        for i, row in enumerate(self.puzzle):
            if i == 3 or i == 6:
                result += '\n'
            for j, item in enumerate(row):
                if j == 3 or j == 6:
                    result += ' '
                result += f'{item}' if item else '_'
            result += '\n'
            #result += f'{row[0]}{row[1]}{row[2]} {row[3]}{row[4]}{row[5]} {row[6]}{row[7]}{row[8]}\n'
        return result


def main():
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
    solver = soduku(puzzle)
    solver.available()
    solver.solve()
    print('\n')
    print(solver)
    print(solver.avail_print())

    # print(solvepuzzle(puzzle))


if __name__ == "__main__":
    main()
