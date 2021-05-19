import numpy as np
import datetime
from typing import Literal, List
import logging as log

log.basicConfig(level=log.DEBUG)
tmm = datetime.datetime.now()


class SudokuTable:
    __numbers = [x for x in range(1, 10)]
    random_position = []

    def __init__(self, difficulty: Literal["easy", "normal", "hard"]):
        # build 9*9 table
        self.table_found=False
        self.table = np.zeros([9, 9])
        self.difficulty = difficulty
        self.__mark_number = 0
        if difficulty == "easy":
            self.__mark_number = np.random.randint(47, 53)
        elif difficulty == "normal":
            self.__mark_number = np.random.randint(34, 47)
        elif difficulty == "hard":
            self.__mark_number = np.random.randint(28, 34)
        else:
            raise Exception("difficulty is not valid")
        while not self.table_found:
            self.complete_table()


    def __all_positions_maker(self):
        self.all_positions = []
        for i in range(9):
            for j in range(9):
                position = np.array([i, j])
                self.all_positions.append(list(position))

    def __repr__(self):
        return str(self.table)

    def complete_table(self):
        self.__numbers = [x for x in range(1, 10)]
        n = self.__mark_number
        self.__all_positions_maker()
        self.random_position.clear()
        for i in range(n):
            self.__generate_random_position()
        for position in self.random_position:
            a = self.mark_random(position)
            if a is bool:
                self.table_found = False
                return
        self.table_found = True

    def __generate_random_position(self):
        inx = np.random.randint(0, len(self.all_positions))
        ch = self.all_positions[inx]
        self.random_position.append(ch)
        self.all_positions.remove(ch)

    def mark_random(self, position):
        if len(self.__numbers) > 0:
            rnd = np.random.choice(self.__numbers)
        else:
            return False
        slice_column: np.ndarray = self.table[position[0]]
        slice_row: np.ndarray = self.table[:, position[1]]
        # slice area
        remain_x = position[0] - (position[0] % 3)
        remain_y = position[1] - (position[1] % 3)
        slice_area: np.ndarray = self.table[remain_x: remain_x + 3, remain_y: remain_y + 3]

        if list(np.where(slice_area == rnd)[0]) == [] and list(np.where(slice_row == rnd)[0]) == [] and list(
                np.where(slice_column == rnd)[0]) == []:
            self.table[position[0], position[1]] = rnd
            self.__numbers = [x for x in range(1, 10)]
        else:
            self.__numbers.remove(rnd)
            self.mark_random(position)

    def check_mark(self, position):

        pass


class SudokuGame:
    __number = [x for x in range(1, 10)]
    __solutions = []

    def __init__(self, t: SudokuTable) -> None:
        super().__init__()
        # self.table = t.table
        self.__exit_solution = False
        self.__one_solution = False
        # self.table = np.array(
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 6, 0, 0, 0, 0, 2, 0, 5, 4, 0, 0, 3, 8, 0, 0, 8, 6, 0, 0, 0, 0, 4,
        #      4, 0, 0, 9, 1, 8, 0, 0, 7, 5, 0, 0, 0, 0, 4, 8, 0, 0, 2, 8, 0, 0, 3, 7, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0,
        #      3, 7, 0, 0, 0, 0, 4, 2, 6])
        self.table = np.zeros(81)
        self.table = self.table.reshape(9, 9)

    def one_solution(self, one: bool):
        self.__one_solution = one

    def solve(self, table=None):
        if table is None:
            pass
        else:
            self.table = table
        self.__solutions.clear()
        tbl, pbl = self.__easy_solve(self.table)
        g.__difficult_solve(tbl, pbl)
        return self.__solutions

    def __easy_solve(self, table: np.ndarray):
        zeros = np.where(table == 0)
        zeros_x = zeros[0]
        zeros_y = zeros[1]
        possible_numbers = {}
        for i in range(len(zeros_x)):
            slice_column: np.ndarray = table[zeros_x[i]]
            slice_row: np.ndarray = table[:, zeros_y[i]]
            remain_x = zeros_x[i] - (zeros_x[i] % 3)
            remain_y = zeros_y[i] - (zeros_y[i] % 3)
            slice_area: np.ndarray = table[remain_x: remain_x + 3, remain_y: remain_y + 3]
            choosable_numbers = []
            for number in self.__number:
                if list(np.where(slice_area == number)[0]) == [] and list(
                        np.where(slice_row == number)[0]) == [] and list(
                    np.where(slice_column == number)[0]) == []:
                    choosable_numbers.append(number)
            if len(choosable_numbers) == 0:
                return 1
            if len(choosable_numbers) == 1:
                table[zeros_x[i], zeros_y[i]] = choosable_numbers[0]
                return self.__easy_solve(table)
            else:
                possible_numbers[tuple([zeros_x[i], zeros_y[i]])] = choosable_numbers
        return table, possible_numbers

    def __difficult_solve(self, table: np.ndarray, possible_numbers: dict):
        for position, choosable_numbers in possible_numbers.items():
            for num in choosable_numbers:
                if self.__exit_solution:
                    return
                temp_table = table.copy()
                temp_table[position[0], position[1]] = num
                res = self.__easy_solve(temp_table)
                if type(res) == tuple:
                    t, pbl = res
                    if len(pbl) == 0:
                        exist = False
                        for sls in self.__solutions:
                            if (t == sls).all():
                                exist = True
                        if not exist:
                            self.__solutions.append(t)
                        if self.__one_solution:
                            self.__exit_solution = True
                            return
                    else:
                        self.__difficult_solve(t, pbl)

        # TODO
        #     rnd = np.random.choice(self.__number)
        # if list(np.where(slice_area == rnd)[0]) == [] and list(np.where(slice_row == rnd)[0]) == [] and list(
        #         np.where(slice_column == rnd)[0]) == []:
        #     log.debug("if where")
        #     self.table[pos[0], pos[1]] = rnd
        #     self.__number = [x for x in range(1, 10)]


# SudokuTable.random_position = []
# g = SudokuGame(None)
# g.one_solution(True)
# l = g.solve()
# print("___________________________________")
# for q in l:
#     print(q)
#     print("__________________________________")
# print(datetime.datetime.now() - tmm)

s = SudokuTable("normal")
print(s.table)
