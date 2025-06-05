from concurrent.futures import ThreadPoolExecutor, as_completed

def fizzbuzz(i):
    if i % 15 == 0:
        return i, "FizzBuzz"
    elif i % 3 == 0:
        return i, "Fizz"
    elif i % 5 == 0:
        return i, "Buzz"
    else:
        return i, str(i)

results = {}

# 並列処理でFizzBuzz計算（最大10スレッド）
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fizzbuzz, i) for i in range(1, 101)]

    for future in as_completed(futures):
        i, result = future.result()
        results[i] = result  # 順番がバラバラでも dict に入れて保持

# 最後に順番に出力
for i in range(1, 101):
    print(results[i])
