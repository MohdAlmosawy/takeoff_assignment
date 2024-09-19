def number_generator():
    while True:
        for i in range(10):
            yield i

if __name__ == '__main__':
    gen = number_generator()
    for _ in range(24):
        print(next(gen))
