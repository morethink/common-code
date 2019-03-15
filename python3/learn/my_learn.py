#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
from collections import Iterable


def trim(s):
    i = 0
    for x in s:
        if x != ' ':
            break
        i += 1

    j = len(s)
    for x in s[::-1]:
        if x != ' ':
            break
        j -= 1
    return s[i:j]


def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a + b
        n = n + 1
    return 'done'


if __name__ == '__main__':
    # i = 10
    # i = 'd'
    # print(i)
    # my_list = [1, 2]
    # print(len(my_list))
    # my_list.append("D")
    # print(len(my_list))
    # if my_list:
    #     print(my_list)
    # max(1, 2)
    #
    # print(trim("  中国  "))
    # fib(5)
    # from collections import Iterable

    print(isinstance(1, Iterable))
    n, a, b = 0, 1, 2
    a, b = b, a + b
    print(a)
    print(b)

    a, b = b, a
    print(a)
    print(b)
