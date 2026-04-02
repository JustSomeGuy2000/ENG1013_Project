# Authors: ENG1013 Team MI05
# Last modified: 2 April 2026
# Version: 1.0.0

from pymata4 import pymata4 as p4
from typing import Callable
import time

P0_RX = 0
'''Do not use!!!'''
P1_TX = 1
'''Do not use!!!'''
P2 = 2
P3_PWM = 3
P4 = 4
P5_PWM = 5
P6_PWM = 6
P7 = 7
P8 = 8
P9_PWM = 9
P10_PWM = 10
P11_PWM = 11
P12 = 12
P13 = 13
P0_A = 14
P1_A = 15
P2_A = 16
P3_A = 17
P4_A = 18
P5_A = 19

def main():
    tickers: list[tuple[float, Callable[[float], None]]] = []
    '''A list of tuples. Each tuple has two members: a number and a function. The number is the time elapsed since the tuple was added to the ticker list. Every frame, the number is used as an argument to the function. Then, the number is updated for the next frame.

    This means that the function must contain the entire sequence inside it and decide which part of the sequence to play out based on the elapsed time.'''
    board = p4.Pymata4()
    try:
        while True:
            start = time.time()

            # all event loop code goes between here...
            # ... and here

            newTickers: list[tuple[float, Callable[[float], None]]] = []
            for ticker in tickers:
                ticker[1](ticker[0])
                newTickers.append((ticker[0] + (time.time() - start), ticker[1]))
            tickers = newTickers
    finally:
        board.shutdown()
        print("Shutting down...")

if __name__ == "__main__":
    main()

    print("Hello World")