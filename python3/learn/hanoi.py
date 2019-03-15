# -*- coding: UTF-8 -*-


def move(n, a, b, c):
    if n == 1:
        print(a, '-->', c)
    else:
        # 把n-1个盘子移动到b
        move(n - 1, a, c, b)
        # 把最底下的一个盘子移动到c
        move(1, a, b, c)
        # 把b上的n-1个盘子移动到c
        move(n - 1, b, a, c)


if __name__ == '__main__':
    move(3, "A", "B", "C")
