import time

def check(): print("checked")

def traffic(counter: float):
    print(counter)
    if counter <= 5:
        print("red")
    elif 5 < counter <= 10:
        print("yellow")
    else:
        print("green")

ticker = (0.0, traffic)
while True:
    start = time.time()
    traffic(ticker[0])
    ticker = (ticker[0] + (time.time() - start), ticker[1])
    check()