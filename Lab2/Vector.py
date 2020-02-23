import math


class n_vector(object):
    vector = []

    def __init__(self, vector):
        if isinstance(vector, list):
            self.vector = vector

    def __add__(self, other):
        return self.__operation(other, '+')

    def __sub__(self, other):
        return self.__operation(other, '-')

    def __mul__(self, other):
        return self.__operation(other, '*')

    def __str__(self):
        string = ''
        for i in self.vector:
            string += ' {}'.format(i)
        return string[1:]

    def __check(self, other, operation):
        if operation == '*':
            return isinstance(other, int) or isinstance(other, float) or isinstance(other, n_vector)
        else:
            return isinstance(other, n_vector) and len(other.vector) == len(self.vector)

    def __operation(self, other, operation):
        result = []
        if self.__check(other, operation):
            if operation == '+':
                result = list(map(lambda x, y: x + y, self.vector, other.vector))
            elif operation == '-':
                result = list(map(lambda x, y: x - y, self.vector, other.vector))
            elif isinstance(other, int):
                result = list(map(lambda x: x * other, self.vector))
            else:
                result = list(map(lambda x, y: x * y, self.vector, other.vector))
        return result

    def get_item(self, index):
        if len(self.vector) > index >= 0:
            return self.vector[index]

    def len(self):
        return math.sqrt(sum(i**2 for i in self.vector))

    @staticmethod
    def dot_product(vec1, vec2, angle):
        return vec1.len() * vec2.len() * math.cos(angle)

    @staticmethod
    def is_equal(vec1, vec2):
        if not isinstance(vec1, n_vector) or not isinstance(vec2, n_vector):
            raise TypeError('vectors must be n_vector')
        return list(set(vec1.vector) ^ set(vec2.vector)) == []
