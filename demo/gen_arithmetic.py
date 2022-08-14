"""
生成四则运算表达式
"""
import math
from random import Random
from decimal import Decimal

MOD_MAX = int('9' * 6)
START_MAX = int('-' + '9' * 30)
END_MAX = int('9' * 30)


def gen_arithmetic(start, end, op, num):
    rand = Random()
    for _ in range(num):
        first = rand.randint(start, end)
        second = rand.randint(start, end)
        result = eval(f'{first}{op}{second}')
        if op == '/':
            if second == 0:
                while second != 0:
                    second = rand.randint(start, end)
                result = eval(f'{first}{op}{second}')
                result = int(result)
            else:
                result = int(result)
        print("{}{}{}={}".format(str(first), op, str(second), result))


def gen_mod_arithmetic(start, end, num):
    rand = Random()
    for _ in range(num):
        first = rand.randint(start, end)
        second = rand.randint(0, MOD_MAX)
        op = '%'
        print("{}{}{}={}".format(str(first), op, str(second), str(first % second)))


def gen_mod_arithmeticV2(start, end, num):
    rand = Random()
    for _ in range(num):
        first = rand.randint(start, end)
        second = rand.randint(start, end)
        op = '%'
        print("{}{}{}={}".format(str(first), op, str(second), str(first % second)))


def gen_mul(start, end, op, num):
    rand = Random()
    for _ in range(num):
        first = rand.randint(start, end)
        second = rand.randint(1, 1000)
        symbol = 1
        first1 = first
        second1 = second
        if first < 0:
            first1 = -first
            symbol = -symbol
        if second < 0:
            second1 = -second
            symbol = -symbol
        result = first1 // second1
        result = symbol * result
        print("{}{}{}={}".format(str(first), op, str(second), result))


def gen_decimal(start, end, op, num):
    rand = Random()
    for _ in range(num):
        first = str(round(rand.random() * rand.choice([1, 10, 100, 1000, 10000]), 4) * rand.choice([-1, 1]))
        second = str(round(rand.random() * rand.choice([1, 10, 100, 1000, 10000]), 4) * rand.choice([-1, 1]))
        # print(first, second)
        if op == '+':
            result = Decimal(first) + Decimal(second)
        elif op == '-':
            result = Decimal(first) - Decimal(second)
        elif op == '*':
            result = Decimal(first) * Decimal(second)
        elif op == '/':
            result = Decimal(first) * Decimal(second)
            first, result = result, first
        result = str(result)
        count = 0
        for item in reversed(result):
            if item == '0':
                count += 1
            else:
                break
        if op == '/':
            print("{}{}{}={:.7f}".format(first, op, second, float(result)))
        else:
            print("{}{}{}={}".format(first, op, second, result))


if __name__ == '__main__':
    gen_decimal(-100000, 1000000, '/', 500)
    # for _ in range(1000):
    #     gen_arithmeticV2(0, START_MAX, END_MAX, '/', 1000)
