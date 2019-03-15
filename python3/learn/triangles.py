# -*- coding: UTF-8 -*-


def triangles():
    yield [1]
    result = [1, 1]
    while True:
        yield result
        temp = [1, 1]
        for x in range(0, len(result) - 1):
            temp.insert(1, result[x] + result[x + 1])
            print(temp)
        result = temp


if __name__ == '__main__':
    n = 0
    for x in triangles():
        print('d' + str(x))
        n += 1
        if n > 5:
            break
    # triangles()
