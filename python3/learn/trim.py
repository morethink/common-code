# -*- coding: UTF-8 -*-


def trim(s):
    while s != '' and s[0] == ' ':
        s = s[1:]
    while s != '' and s[-1] == ' ':
        s = s[:-1]
    return s


if __name__ == '__main__':
    # 测试:
    if trim('hello  ') != 'hello':
        print('测试失败!')
    elif trim('  hello') != 'hello':
        print('测试失败!')
    elif trim('  hello  ') != 'hello':
        print('测试失败!')
    elif trim('  hello  world  ') != 'hello  world':
        print('测试失败!')
    elif trim('') != '':
        print('测试失败!')
    elif trim('    ') != '':
        print('测试失败!')
    else:
        print('测试成功!')
