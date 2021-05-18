import numpy as np
from typing import Literal, List
import logging as log

log.basicConfig(level=log.DEBUG)


class SudokuTable:
    __numbers = [x for x in range(1, 10)]
    random_position = []

    def __init__(self, difficulty: Literal["easy", "normal", "hard"]):
        # build 9*9 table
        self.table = np.zeros([9, 9])
        self.difficulty = difficulty
        __mark_number = 0
        if difficulty == "easy":
            self.__mark_number = np.random.randint(47, 53)
        elif difficulty == "normal":
            self.__mark_number = np.random.randint(34, 47)
        elif difficulty == "hard":
            self.__mark_number = np.random.randint(28, 34)
        else:
            raise Exception("difficulty is not valid")
        self.complete_table(self.__mark_number)

    def __repr__(self):
        return str(self.table)

    def complete_table(self, n):
        for i in range(n):
            self.__generate_random_position()
        for position in self.random_position:
            self.mark_random(position)

    def __generate_random_position(self):
        position = np.array([np.random.randint(0, 9), np.random.randint(0, 9)])
        log.debug(f"{self.random_position} ops")
        if list(position) not in self.random_position:
            self.random_position.append(list(position))
            return self.random_position
        else:
            self.__generate_random_position()

    def mark_random(self, position):
        log.debug(f"{self.__numbers} ,,,,,")
        try:
            rnd = np.random.choice(self.__numbers)
        except ValueError:
            # self.__generate_random_position()
            # self.mark_random(self.random_position[-1])
            # self.random_position.remove(self.random_position[-1])
            self.__numbers = [x for x in range(1, 10)]
            self.random_position = []
            self.table = np.zeros([9, 9])
            self.mark_random(self.__mark_number)
            return
        log.debug(f"{position} && {rnd}rnd")  # log
        slice_column: np.ndarray = self.table[position[0]]
        slice_row: np.ndarray = self.table[:, position[1]]
        # slice area
        remain_x = position[0] - (position[0] % 3)
        remain_y = position[1] - (position[1] % 3)
        slice_area: np.ndarray = self.table[remain_x: remain_x + 3, remain_y: remain_y + 3]
        log.debug(slice_row)
        log.debug(slice_column)
        log.debug(slice_area)

        if list(np.where(slice_area == rnd)[0]) == [] and list(np.where(slice_row == rnd)[0]) == [] and list(
                np.where(slice_column == rnd)[0]) == []:
            log.debug("if where")

            self.table[position[0], position[1]] = rnd
            self.__numbers = [x for x in range(1, 10)]
        else:
            self.__numbers.remove(rnd)
            self.mark_random(position)

    def check_mark(self, position):

        pass


class SudokuGame:
    __number = [x for x in range(1, 10)]
    possible_numbers = {}

    def __init__(self, t: SudokuTable) -> None:
        super().__init__()
        # self.table = t.table
        self.table = np.array(
            [6, 5, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 6, 0, 0, 0, 0, 2, 0, 5, 4, 0, 0, 3, 8, 0, 0, 8, 6, 0, 0, 0, 0, 4,
             4, 0, 0, 9, 1, 8, 0, 0, 7, 5, 0, 0, 0, 0, 4, 8, 0, 0, 2, 8, 0, 0, 3, 7, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0,
             3, 7, 0, 0, 0, 0, 4, 2, 6])
        # self.table = np.zeros(81)
        self.table = self.table.reshape(9, 9)

    def easy_solve(self, table: np.ndarray):
        zeros = np.where(table == 0)
        zeros_x = zeros[0]
        zeros_y = zeros[1]
        # log.info(f"{zeros_x} ras")
        # is_change_happened = False
        possible_numbers = {}

        for i in range(len(zeros_x)):
            # print("zero")
            slice_column: np.ndarray = table[zeros_x[i]]
            slice_row: np.ndarray = table[:, zeros_y[i]]
            remain_x = zeros_x[i] - (zeros_x[i] % 3)
            remain_y = zeros_y[i] - (zeros_y[i] % 3)
            slice_area: np.ndarray = table[remain_x: remain_x + 3, remain_y: remain_y + 3]
            choosable_numbers = []
            for number in self.__number:
                # print(np.where(slice_area == number)[0])
                if list(np.where(slice_area == number)[0]) == [] and list(
                        np.where(slice_row == number)[0]) == [] and list(
                    np.where(slice_column == number)[0]) == []:
                    choosable_numbers.append(number)
            if len(choosable_numbers) == 0:
                return 1
            if len(choosable_numbers) == 1:
                table[zeros_x[i], zeros_y[i]] = choosable_numbers[0]
                return self.easy_solve(table)
            else:
                possible_numbers[tuple([zeros_x[i], zeros_y[i]])] = choosable_numbers
        return table, possible_numbers

    def difficult_solve(self, table: np.ndarray, possible_numbers: dict):
        print(type(possible_numbers))

        for position, choosable_numbers in possible_numbers.items():
            for num in choosable_numbers:
                temp_table = table.copy()
                temp_table[position[0], position[1]] = num
                res = self.easy_solve(temp_table)
                if type(res) == tuple:

                    t, pbl = res
                    if len(pbl) == 0:
                        yield t
                        break
                    self.difficult_solve(t, pbl)

            # slice_column: np.ndarray = self.table[position[0]]
            # slice_row: np.ndarray = self.table[:, position[1]]
            # remain_x = position[0] - (position[0] % 3)
            # remain_y = position[1] - (position[1] % 3)
            # slice_area: np.ndarray = self.table[remain_x: remain_x + 3, remain_y: remain_y + 3]

        pass
        # TODO
        #     rnd = np.random.choice(self.__number)
        # if list(np.where(slice_area == rnd)[0]) == [] and list(np.where(slice_row == rnd)[0]) == [] and list(
        #         np.where(slice_column == rnd)[0]) == []:
        #     log.debug("if where")
        #     self.table[pos[0], pos[1]] = rnd
        #     self.__number = [x for x in range(1, 10)]


def try_many_times():
    try:
        a = 1
        counter = 0
        while a == 1:
            SudokuTable.random_position = []
            s = SudokuTable("easy")
            print(s)
            g = SudokuGame(s)
            a, z = g.easy_solve(g.table)
            g.difficult_solve(a, z)

            counter += 1
        print(a)
        print(counter)
        return

    except:
        try_many_times()


# try_many_times()
g = SudokuGame(None)
a, z = g.easy_solve(g.table)
# print(z)
# print(a)
print("____________________________________")
# cnt = 0
# for i in g.difficult_solve(a, z):
#     print(i)
#     cnt +=1
# print(cnt)
# # print(g.difficult_solve(a, z))
ls = [x for x in g.difficult_solve(a, z)]
cn = 0
for ip in ls:
    for itm in ls:
        if not (ip == itm).all():
            cn += 1

print(cn)
print(len(ls))
# numbers = [1, 2, 3, 4, 5, 6, 7]
# for number in numbers:
#     print(number)
#     if number == 1:
#         numbers.remove(1)
# print(*list(np.zeros([9])))
