import unittest
from Vector import NVector

VECTOR_3N = [1, 2, 3]
VECTOR_3N_SUM = [2, 4, 6]
VECTOR_3N_SUB = [0, 0, 0]
VECTOR_3N_MUL = [1, 4, 9]
VECTOR_5N = [1, 2, 3, 4, 5]
VECTOR_3N_STR = '1 2 3'


class VectorTest(unittest.TestCase):

    def test_equal_failed_params(self):
        with self.assertRaises(TypeError):
            NVector.is_equal(VECTOR_3N, VECTOR_5N)

    def test_vectors_equals(self):
        self.assertEqual(NVector.is_equal(NVector(VECTOR_3N), NVector(VECTOR_5N)), False)

    def test_vectors_add(self):
        self.assertEqual(NVector(VECTOR_3N) + NVector(VECTOR_3N), VECTOR_3N_SUM)

    def test_vectors_sub(self):
        self.assertEqual(NVector(VECTOR_3N) - NVector(VECTOR_3N), VECTOR_3N_SUB)

    def test_vectors_mul(self):
        self.assertEqual(NVector(VECTOR_3N) * NVector(VECTOR_3N), VECTOR_3N_MUL)

    def test_vector_to_str(self):
        self.assertEqual(str(NVector(VECTOR_3N)), VECTOR_3N_STR)


if __name__ == '__main__':
    unittest.main()
