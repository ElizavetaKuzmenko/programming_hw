__author__ = 'liza'

import unittest, re

class TestFibonacci(unittest.TestCase):
    def setUp(self):  # операции, которые надо выполнить для любого теста
        pass

    def test_math(self):
        self.assertEqual(fib(0), 1)
        self.assertEqual(fib(1), 1)
        self.assertEqual(fib(14), 8)

    def test_bad_data(self):
        self.assertEqual(fib('котик'), -1)

class TestDrink(unittest.TestCase):
    def test_re(self):
        for line in open('drink.txt', 'r'):
            word = line.strip('\n,')
            print(word)
            self.assertTrue(drink(word))

def fib(n):
    if type(n) is not int:
        return -1
    elif n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return fib(n - 2) + fib(n - 1)

def drink(string):
    if re.search('^вып(ью|ьем|ьешь|ьет|ьют|ит|ив|ил|ей)', string.lower()) is None:
        return False
    else:
        return True


if __name__ == '__main__':
    unittest.main(verbosity=2)  # to write about tests that are successfully executed
