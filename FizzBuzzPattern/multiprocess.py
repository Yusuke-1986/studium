from multiprocessing import Pool

def fizzbuzz(i):
    if i % 15 == 0:
        return i, "FizzBuzz"
    elif i % 3 == 0:
        return i, "Fizz"
    elif i % 5 == 0:
        return i, "Buzz"
    else:
        return i, str(i)

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        results = pool.map(fizzbuzz, range(1, 101))
    
    # mapは順番保持してくれる！
    for i, text in results:
        print(text)
