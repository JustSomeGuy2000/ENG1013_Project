from pymata4 import pymata4 as p4
from typing import Callable, Coroutine
import asyncio

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

def arduinoContextManager(run: Callable[[p4.Pymata4], None]):
    '''Automatically handles board initialisation and shutdown, simulating a context manager.'''
    board = p4.Pymata4()
    try:
        run(board)
    finally:
        board.shutdown()
        print("Shutting down...")

def arduinoAsyncContextManager(run: Callable[[p4.Pymata4], Coroutine[None, None, None]]):
    '''Automatically handles board initialisation and shutdown, simulating an async context manager.'''
    board = p4.Pymata4()
    try:
        asyncio.run(run(board))
    finally:
        board.shutdown()
        print("Shutting down...")