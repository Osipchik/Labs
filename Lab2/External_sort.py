from Sort import Sort
import tempfile
import os


class External_sort(object):
    __RESULT_FILE = 'sorted_numbers.txt'
    __TEMP_LINES = 1_000_000
    __temp_files = []

    def sort_file(self, filename):
        self.__read_file(filename)
        self.__sort_temp_files()
        self.__create_file()

    def __read_file(self, filename):
        temp_arr = []
        with open(filename, 'r') as f:
            line = f.readline()
            while line:
                if len(temp_arr) > self.__TEMP_LINES:
                    self.__create_temp_file(temp_arr)
                    temp_arr = []

                temp_arr.append(int(line))
                line = f.readline()

            if len(temp_arr) > 0:
                self.__create_temp_file(temp_arr)

    def __create_file(self):
        temp_file = self.__temp_files[0]
        with open(self.__RESULT_FILE, 'w') as f, open(temp_file.name, 'r') as temp:
            for i, val in enumerate(temp):
                f.writelines(val)
        self.__remove_temp_file(temp_file)

    def __create_temp_file(self, array):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
            array = Sort.merge_sort(array)
            temp.writelines(f'{i}\n' for i in array)
            self.__temp_files.append(temp)

    def __sort_temp_files(self):
        while len(self.__temp_files) > 1:
            with open(self.__temp_files[0].name, 'r') as temp_f, open(self.__temp_files[1].name, 'r') as temp_s:
                with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
                    self.__fill_temp(temp, [temp_f, temp_s])
                    self.__temp_files.append(temp)

            self.__remove_temp_file(temp_f)
            self.__remove_temp_file(temp_s)

    def __fill_temp(self, temp, files):
        first_line = files[0].readline()
        second_line = files[1].readline()
        while first_line and second_line:
            if int(first_line) > int(second_line):
                temp.writelines(f'{second_line}')
                second_line = files[1].readline()
            else:
                temp.writelines(f'{first_line}')
                first_line = files[0].readline()

        if first_line:
            self.__continue_fill(temp, files[0], first_line)
        else:
            self.__continue_fill(temp, files[1], second_line)

    @staticmethod
    def __continue_fill(temp, file, line):
        while line:
            temp.writelines(f'{line}')
            line = file.readline()

    def __remove_temp_file(self, file):
        if os.path.exists(file.name):
            self.__temp_files.pop(0)
            os.remove(file.name)

    def __del__(self):
        for i in self.__temp_files:
            self.__remove_temp_file(i)
