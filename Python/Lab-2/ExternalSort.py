import tempfile
import os

from Singleton import Singleton


class ExternalSort(metaclass=Singleton):
    __temp_file = None

    def sort_file(self, src_filename, dist_filename, read_lines):
        self.__is_src_exist(src_filename)
        temp_arr = []
        with open(src_filename, 'r') as f:
            for line in f:
                temp_arr.append(int(line))
                if len(temp_arr) >= read_lines:
                    temp_arr.sort()
                    if self.__temp_file is not None:
                        self.__merge_sorted_temp(temp_arr)
                    else:
                        self.__create_temp(temp_arr)
                    temp_arr = []

        self.__create_result_file(dist_filename)

    def __is_src_exist(self, src):
        if not os.path.exists(src):
            raise FileNotFoundError('no such file: {}'.format(src))

    def __create_temp(self, lines):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
            temp.writelines('{}\n'.format(i) for i in lines)
            self.__temp_file = temp.name

    def __merge_sorted_temp(self, array):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
            with open(self.__temp_file, 'r') as f:
                line = self.__merge_file_with_array(f, temp, iter(array), array[-1])
                while line:
                    temp.writelines('{}'.format(line))
                    line = f.readline()

        self.__remove_temp_file()
        self.__temp_file = temp.name

    @staticmethod
    def __merge_file_with_array(file, f_temp, iterator, last):
        item = next(iterator)
        f_line = file.readline()
        while f_line:
            if int(f_line) > item:
                f_temp.writelines('{}\n'.format(item))
                if item != last:
                    item = next(iterator)
                else:
                    break
            else:
                f_temp.writelines('{}'.format(f_line))
                f_line = file.readline()

        return f_line

    def __remove_temp_file(self):
        if os.path.exists(self.__temp_file):
            os.remove(self.__temp_file)
            self.__temp_file = None

    def __create_result_file(self, dist_filename):
        with open(dist_filename, 'w') as f, open(self.__temp_file, 'r') as temp:
            for line in temp:
                f.writelines('{}'.format(line))

        self.__remove_temp_file()
