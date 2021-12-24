

def func(a, b , age=4, *args, **kw):
    print(a, b, age)
    print('args', args)
    print('kw', kw)


if __name__ == '__main__':
    func(1,2, 44, 5,6, first_name='larry', last_name='zhu')