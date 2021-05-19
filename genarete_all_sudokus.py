import numpy
import numpy as np


class generate_all_sudokus:
    __numbers_list = [x for x in range(1, 10)]
    __premutade_numbers = []
    __all_sudokus_possible = []

    def __init__(self):
        self.permutation(self.__numbers_list)
        self.create_all_sudokus()
        print(len(self.__all_sudokus_possible))
        print("____________________________________________")
        print(self.__all_sudokus_possible[1])
        print("____________________________________________")
        print(self.__all_sudokus_possible[90])

    def permutation(self, numbers_list: list, picked_list=None):
        if not picked_list:
            picked_list = []
        for i in numbers_list:
            if len(picked_list) == 0:
                picked_list = []
            templist = numbers_list.copy()
            templist.remove(i)
            temppicklist = picked_list.copy()
            temppicklist.append(i)
            if len(templist) == 0:
                nplst = np.array(temppicklist)
                nplst = nplst.reshape(3, 3)
                self.__premutade_numbers.append(nplst)
            else:
                self.permutation(templist, temppicklist)

    @staticmethod
    def create_table() -> np.ndarray:
        return np.zeros([9, 3, 3])

    def create_all_sudokus(self, counter=-1, one_table=None):
        if one_table is None:
            one_table = generate_all_sudokus.create_table()
        counter += 1
        for i in self.__premutade_numbers:
            one_table_temp = one_table.copy()
            one_table_temp[counter] = i
            if counter == 8:
                self.__all_sudokus_possible.append(one_table_temp)
            else:
                self.create_all_sudokus(counter, one_table_temp)


a = generate_all_sudokus()
