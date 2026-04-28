# Authors: ENG1013 Team MI05
# Last modified: 28 April 2026
# Version: 2.0.0

# clean all type annotations before submitting!

from pymata4 import pymata4 as p4
from typing import Callable, TypedDict, Literal #clean -> del
import time

#region pins
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
#endregion

#region types
State = Literal[1, 0]
Stateset = list[State]

class ShiftRegisters(TypedDict):
    board: p4.Pymata4
    inputPin: int
    '''SER'''
    clockPin: int
    '''SRCLCK'''
    latchPin: int
    '''RCLCK'''
    states: Stateset
    '''The states of all the registers in series with the first element being the first bit of the first register. Needed to restore state after changes to single bits.'''
    size: int
    '''The total bit storage of the registers.'''

class TrafficLight(TypedDict):
    board: p4.Pymata4
    regs: ShiftRegisters
    regId: int
    redBit: int
    yellowBit: int
    greenBit: int

class PedestrianLight(TypedDict):
    board: p4.Pymata4
    regs: ShiftRegisters
    regId: int
    redBit: int
    greenBit: int

class WarningLight(TypedDict):
    board: p4.Pymata4
    regs: ShiftRegisters
    regId: int
    bit: int

class FloodlLight(TypedDict):
    board: p4.Pymata4
    regs: ShiftRegisters
    regId: int
    bit: int

class UltrasonicSensor(TypedDict):
    board: p4.Pymata4
    triggerPin: int
    echoPin: int

class DaylightSensor(TypedDict):
    board: p4.Pymata4
    inputPin: int

class Buzzer(TypedDict):
    board: p4.Pymata4
    regs: ShiftRegisters
    regId: int
    bit: int

class PushButton(TypedDict):
    board: p4.Pymata4
    inputPin: int
#endregion

#region constructors
def new_traffic_light(board: p4.Pymata4, regs: ShiftRegisters, regId: int, redBit: int, yellowBit: int, greenBit: int) -> TrafficLight:
    '''
    Create a traffic light dictionary.
    Params:
        regId: Register number of the light.
        redBit: Bit of the register the red light is connected to.
        yellowBit: Bit of the register the yellow light is connected to.
        greenBit: Bit of the register the green light is connected to.
    Returns:
        tl: A dictionary containg information about the traffic light.'''
    return {"board": board, "regs": regs, "regId": regId, "redBit": redBit, "yellowBit": yellowBit, "greenBit": greenBit}

def new_pedestrian_light(board: p4.Pymata4, regs: ShiftRegisters, regId: int, redBit: int, greenBit: int) -> PedestrianLight:
    '''
    Create a predestrian light dictionary.
    Params:
        board: The parent board.
        regs: The shift registers this connects to.
        regId: Register number of the light.
        redBit: Bit of the register the red light is connected to.
        greenBit: Bit of the register the green light is connected to.
    Returns:
        pl: A dictionary containg information about the pedestrian light.'''
    return {"board": board, "regs": regs, "regId": regId, "redBit": redBit, "greenBit": greenBit}

def new_warning_light(board: p4.Pymata4, regs: ShiftRegisters, regId: int, bit: int) -> WarningLight:
    '''
    Create a warning light dictionary.
    Params:
        board: The parent board.
        regs: The shift registers this connects to.
        regId: Register number of the light.
        bit: Bit of the register the light is connected to.
    Returns:
        wl: A dictionary containg information about the warning light.'''
    return {"board": board, "regs": regs, "regId": regId, "bit": bit}

def new_floodlight(board: p4.Pymata4, regs: ShiftRegisters, regId: int, bit: int) -> FloodlLight:
    '''
    Create a floodlight dictionary.
    Params:
        board: The parent board.
        regs: The shift registers this connects to.
        regId: Register number of the light.
        bit: Bit of the register the light is connected to.
    Returns:
        fl: A dictionary containg information about the floodlight.'''
    return {"board": board, "regs": regs, "regId": regId, "bit": bit}

def new_ultrasonic_sensor(board: p4.Pymata4, triggerPin: int, echoPin: int) -> UltrasonicSensor:
    '''
    Create an ultrasonic sensor dictionary. Registers the pins for sonar use.
    Params:
        board: The parent board.
        triggerPin: Pin number for triggering the sensor.
        echoPin: Pin number receiving input from the sensor.
    Returns:
        us: A dictionary containg information about the sensor.'''
    board.set_pin_mode_sonar(triggerPin, echoPin)
    return {"board": board, "triggerPin": triggerPin, "echoPin": echoPin}

def new_buzzer(board: p4.Pymata4, regs: ShiftRegisters, regId: int, bit: int) -> Buzzer:
    '''
    Create a buzzer dictionary
    Params:
        board: The parent board.
        regs: The shift registers this connects to.
        regId: Register number of the buzzer.
        bit: Which bit of the register the buzzer is connected to.
    Returns:
        pa: A dictionary containg information about the buzzer.'''
    return {"board": board, "regs": regs, "regId": regId, "bit": bit}

def new_daylight_sensor(board: p4.Pymata4, inputPin: int) -> DaylightSensor:
    '''
    Create a daylight sensor dictionary. Registers the pin as analog input.
    Params:
        board: The parent board.
        inputPin: Pin number receiving input from the sensor.
    Returns:
        ds: A dictionary containg information about the sensor.'''
    board.set_pin_mode_analog_input(inputPin)
    return {"board": board, "inputPin": inputPin}

def new_push_button(board: p4.Pymata4, inputPin: int) -> PushButton:
    '''
    Create a push button dictionary. Registers the pin as input.
    Params:
        board: The parent board.
        inputPin: Pin number receiving input from the button.
    Returns:
        pb: A dictionary containg information about the button.'''
    board.set_pin_mode_digital_input(inputPin)
    return {"board": board, "inputPin": inputPin}

def new_shift_registers(board: p4.Pymata4, inputPin: int, clockPin: int, latchPin: int, count: int) -> ShiftRegisters:
    '''
    Create a shift registers dictionary. Registers the pins as output and initialises them.
    Params:
        board: The parent board.
        inputPin: Pin number for SER.
        clockPin: Pin number for SRCLCK.
        latchPin: Pin number for RCLCK.
        count: Number of registers in the series.
    Returns:
        sr: A dictionary containg information about the registers.'''
    board.set_pin_mode_digital_output(inputPin)
    board.set_pin_mode_digital_output(clockPin)
    board.set_pin_mode_digital_output(latchPin)
    board.digital_write(clockPin, 0)
    board.digital_write(latchPin, 0)
    return {"board": board, "inputPin": inputPin, "clockPin": clockPin, "latchPin": latchPin, "states": [0 for _ in range(count * 8)], "size": count * 8}
#endregion

#region interface
def tl_turn_red(tl: TrafficLight):
    '''
    Turn a traffic light red.
    Params:
        tl: The traffic light dictionary.
    Returns:
        None: None'''
    sr_set_bit(tl["regs"], tl["regId"], tl["redBit"], 1)
    sr_set_bit(tl["regs"], tl["regId"], tl["yellowBit"], 0)
    sr_set_bit(tl["regs"], tl["regId"], tl["greenBit"], 0)

def tl_turn_yellow(tl: TrafficLight):
    '''
    Turn a traffic light yellow.
    Params:
        tl: The traffic light dictionary.
    Returns:
        None: None'''
    sr_set_bit(tl["regs"], tl["regId"], tl["redBit"], 0)
    sr_set_bit(tl["regs"], tl["regId"], tl["yellowBit"], 1)
    sr_set_bit(tl["regs"], tl["regId"], tl["greenBit"], 0)

def tl_turn_green(tl: TrafficLight):
    '''
    Turn a traffic light green.
    Params:
        tl: The traffic light dictionary.
    Returns:
        None: None'''
    sr_set_bit(tl["regs"], tl["regId"], tl["redBit"], 0)
    sr_set_bit(tl["regs"], tl["regId"], tl["yellowBit"], 0)
    sr_set_bit(tl["regs"], tl["regId"], tl["greenBit"], 1)

def pl_turn_green(pl: PedestrianLight):
    '''
    Turn a pedestrian light yellow.
    Params:
        pl: The pedestrian light dictionary.
    Returns:
        None: None'''
    sr_set_bit(pl["regs"], pl["regId"], pl["greenBit"], 1)
    sr_set_bit(pl["regs"], pl["regId"], pl["redBit"], 0)

def pl_turn_red(pl: PedestrianLight):
    '''
    Turn a pedestrian light red.
    Params:
        pl: The pedestrian light dictionary.
    Returns:
        None: None'''
    sr_set_bit(pl["regs"], pl["regId"], pl["greenBit"], 0)
    sr_set_bit(pl["regs"], pl["regId"], pl["redBit"], 1)

def wl_switch(wl: FloodlLight, on: State):
    '''
    Switch a warning light on or off.
    Params:
        pl: The warning light dictionary.
        on: 1 to switch on, 0 to switch off.
    Returns:
        None: None'''
    sr_set_bit(wl["regs"], wl["regId"], wl["bit"], on)

def fl_switch(fl: FloodlLight, on: State):
    '''
    Switch a floodlight on or off.
    Params:
        pl: The floodlight dictionary.
        on: 1 to switch on, 0 to switch off.
    Returns:
        None: None'''
    sr_set_bit(fl["regs"], fl["regId"], fl["bit"], on)

def us_read(us: UltrasonicSensor) -> int:
    '''
    Read the value from an ultrasonic sensor.
    Params:
        us: The sensor dictionary.
    Returns:
        distance: The value read.'''
    return us["board"].sonar_read(us["triggerPin"])[0]

def pa_sound(pa: Buzzer, on: State):
    '''
    Switch a buzzer on or off.
    Params:
        pl: The buzzer dictionary.
        on: 1 to switch on, 0 to switch off.
    Returns:
        None: None'''
    sr_set_bit(pa["regs"], pa["regId"], pa["bit"], on)

def ds_is_day(ds: DaylightSensor) -> bool:
    '''
    Read the daytime status from a daylight sensor.
    Params:
        ds: The daylight sensor dictionary.
    Returns:
        isDay: True if its bright enough to be daytime, False otherwise.'''
    raise NotImplementedError

def pb_read(pb: PushButton) -> bool:
    '''
    Read the state of a push button.
    Params:
        pb: The push button dictionary.
    Returns:
        pushed: True if the button is currently being pushed, False otherwise.'''
    return pb["board"].digital_read(pb["inputPin"])[0] == 1

def sr_read(sr: ShiftRegisters, regId: int, bit: int) -> State:
    '''
    Read the value of a single bit from the shift register chain.
    Params:
        sr: The shift register chain.
        regId: Register number to target (starting from 0).
        bit: Bit number to read (0-7).'''
    return sr["states"][regId * 8 + bit]

def sr_store_0(sr: ShiftRegisters):
    '''
    Push 0 to the shift register chain.
    Params:
        sr: The shift register chain.
    Returns:
        None: None'''
    board = sr["board"]
    board.digital_write(sr["inputPin"], 0)
    board.digital_write(sr["clockPin"], 1)
    board.digital_write(sr["clockPin"], 0)

def sr_store_1(sr: ShiftRegisters):
    '''
    Push 1 to the shift register chain.
    Params:
        sr: The shift register chain.
    Returns:
        None: None'''
    board = sr["board"]
    board.digital_write(sr["inputPin"], 1)
    board.digital_write(sr["clockPin"], 1)
    board.digital_write(sr["clockPin"], 0)

def sr_set_bit(sr: ShiftRegisters, regId: int, bit: int, setTo: State):
    '''
    Set the state of a single bit in a shift register chain.
    Params:
        sr: The shift register chain.
        regId: Register number to target (starting from 0).
        bit: Bit number to change (0-7).
        setTo: What to change the bit to.
    Returns:
        None: None'''
    final = sr["states"][:8 * regId + bit]
    final.append(setTo)
    final += sr["states"][8 * regId + bit + 1:]
    sr_set_all(sr, final)

def sr_set_all(sr: ShiftRegisters, seq: Stateset):
    '''
    Set the entire state of a shift register chain.
    Params:
        sr: The shift register chain.
        seq: An list representing the final state of the entire chain.
    Returns:
        None: None'''
    length = len(seq)
    if length != sr["size"]: # strict checking, errors are better than silent mistakes
        raise ValueError(f"Incorrect length: {length}")
    sr["states"] = seq
    for i in range(length): # reverse iteration for proper order
        if seq[length - i - 1] == 0:
            sr_store_0(sr)
        else:
            sr_store_1(sr)
    sr_latch(sr)

def sr_latch(sr: ShiftRegisters):
    '''
    Latch some shift registers, setting their output.
    Params:
        sr: The shift registers.
    Returns:
        None: None'''
    board = sr["board"]
    board.digital_write(sr["latchPin"], 1)
    board.digital_write(sr["latchPin"], 0)
#endregion

#region main
def main():
    tickers: list[tuple[float, Callable[[float], bool]]] = []
    '''A list of tuples. Each tuple has two members: a number and a function. The number is the time elapsed since the tuple was added to the ticker list. Every frame, the number is used as an argument to the function. Then, the number is updated for the next frame. If the function returns False, it is removed from the list.

    This means that the function must contain the entire sequence inside it and decide which part of the sequence to play out based on the elapsed time.'''
    board = p4.Pymata4()
    overheightLimit: float = 0

    try:
        while True:
            start = time.time()

            # all event loop code goes between here...
            # ... and here

            newTickers: list[tuple[float, Callable[[float], bool]]] = []
            for ticker in tickers:
                if (ticker[1](ticker[0])):
                    newTickers.append((ticker[0] + (time.time() - start), ticker[1]))
            tickers = newTickers
    finally:
        board.shutdown()
        print("Shutting down...")
#endregion 

if __name__ == "__main__":
    main()