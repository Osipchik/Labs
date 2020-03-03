import tempfile
import os


class external_sort:
    __temp_file = None

    @classmethod
    def sort_file(cls, src_filename, dist_filename, read_lines):
        cls.__is_src_exist(src_filename)
        temp_arr = []
        with open(src_filename, 'r') as f:
            for line in f:
                temp_arr.append(int(line))
                if len(temp_arr) >= read_lines:
                    temp_arr.sort()
                    if cls.__temp_file is not None:
                        cls.__merge_sorted_temp(temp_arr)
                    else:
                        cls.__create_temp(temp_arr)
                    temp_arr = []

        cls.__create_result_file(dist_filename)

    @staticmethod
    def __is_src_exist(src):
        if not os.path.exists(src):
            raise FileNotFoundError('no such file: {}'.format(src))

    @classmethod
    def __create_temp(cls, lines):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
            temp.writelines('{}\n'.format(i) for i in lines)
            cls.__temp_file = temp.name

    @classmethod
    def __merge_sorted_temp(cls, array):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
            with open(cls.__temp_file, 'r') as f:
                line = cls.__merge_file_with_array(f, temp, iter(array), array[-1])
                while line:
                    temp.writelines('{}'.format(line))
                    line = f.readline()

        cls.__remove_temp_file()
        cls.__temp_file = temp.name

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

    @classmethod
    def __remove_temp_file(cls):
        if os.path.exists(cls.__temp_file):
            os.remove(cls.__temp_file)
            cls.__temp_file = None

    @classmethod
    def __create_result_file(cls, dist_filename):
        with open(dist_filename, 'w') as f, open(cls.__temp_file, 'r') as temp:
            for line in temp:
                f.writelines('{}'.format(line))

        cls.__remove_temp_file()
