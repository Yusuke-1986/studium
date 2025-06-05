def fzbz():
    i = 1
    while True:
        if i % 15 == 0:
            yield "FizzBuzz"
        elif i % 3 == 0:
            yield "Fizz"
        elif i % 5 == 0:
            yield "Buzz"
        else:
            yield str(i)
        i += 1

gen = fzbz()

for _ in range(100):
    print(next(gen))