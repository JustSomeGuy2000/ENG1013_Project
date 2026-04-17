# Authors: ENG1013 Team MI05
# Last modified: 17 April 2026
# Version: 1.2.0

# clean all type annotations before submitting!

from pymata4 import pymata4 as p4
from typing import Callable, TypedDict #clean -> del
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
class TrafficLight(TypedDict):
    pass

class PedestrianLight(TypedDict):
    pass

class WarningLight(TypedDict):
    pass

class FloodlLight(TypedDict):
    pass

class UltrasonicSensor(TypedDict):
    pass

class DaylightSensor(TypedDict):
    pass

class Buzzer(TypedDict):
    pass

class PushButton(TypedDict):
    pass
#endregion

#region constructors
def new_traffic_light() -> TrafficLight:
    '''
    Create a traffic light dictionary.
    Params:
        None: for now
    Returns:
        tl: A dictionary containg information about the traffic light.'''
    return {}

def new_pedestrian_light() -> PedestrianLight:
    '''
    Create a predestrian light dictionary.
    Params:
        None: for now
    Returns:
        pl: A dictionary containg information about the pedestrian light.'''
    return {}

def new_warning_light() -> WarningLight:
    '''
    Create a warning light dictionary.
    Params:
        None: for now
    Returns:
        wl: A dictionary containg information about the warning light.'''
    return {}

def new_floodlight() -> FloodlLight:
    '''
    Create a floodlight dictionary.
    Params:
        None: for now
    Returns:
        fl: A dictionary containg information about the floodlight.'''
    return {}

def new_ultrasonic_sensor() -> UltrasonicSensor:
    '''
    Create an ultrasonic sensor dictionary.
    Params:
        None: for now
    Returns:
        us: A dictionary containg information about the sensor.'''
    return {}

def new_buzzer() -> Buzzer:
    '''
    Create a buzzer dictionary.
    Params:
        None: for now
    Returns:
        pa: A dictionary containg information about the buzzer.'''
    return {}

def new_daylight_sensor() -> DaylightSensor:
    '''
    Create a daylight sensor dictionary.
    Params:
        None: for now
    Returns:
        ds: A dictionary containg information about the sensor.'''
    return {}

def new_push_button() -> PushButton:
    '''
    Create a push button dictionary.
    Params:
        None: for now
    Returns:
        pb: A dictionary containg information about the button.'''
    return {}
#endregion

#region interface
def tl_turn_red(tl: dict):
    '''
    Turn a traffic light red.
    Params:
        tl: The traffic light dictionary.
    Returns:
        None: None'''
    pass

def tl_turn_yellow(tl: dict):
    '''
    Turn a traffic light yellow.
    Params:
        tl: The traffic light dictionary.
    Returns:
        None: None'''
    pass

def tl_turn_green(tl: dict):
    '''
    Turn a traffic light green.
    Params:
        tl: The traffic light dictionary.
    Returns:
        None: None'''
    pass

def pl_turn_green(pl: dict):
    '''
    Turn a pedestrian light yellow.
    Params:
        pl: The pedestrian light dictionary.
    Returns:
        None: None'''
    pass

def pl_turn_red(pl: dict):
    '''
    Turn a pedestrian light red.
    Params:
        pl: The pedestrian light dictionary.
    Returns:
        None: None'''
    pass

def wl_switch(wl: dict, on: bool):
    '''
    Switch a warning light on or off.
    Params:
        pl: The warning light dictionary.
        on: True to switch on, False to switch off.
    Returns:
        None: None'''
    pass

def fl_switch(wl: dict, on: bool):
    '''
    Switch a floodlight on or off.
    Params:
        pl: The floodlight dictionary.
        on: True to switch on, False to switch off.
    Returns:
        None: None'''
    pass

def us_read(us: dict) -> int:
    '''
    Read the value from an ultrasonic sensor.
    Params:
        us: The sensor dictionary.
    Returns:
        distance: The value read.'''
    return 0

def pa_sound(pa: dict, on: bool):
    '''
    Switch a buzzer on or off.
    Params:
        pl: The buzzer dictionary.
        on: True to switch on, False to switch off.
    Returns:
        None: None'''
    pass

def ds_is_day(ds: dict) -> bool:
    '''
    Read the daytime status from a daylight sensor.
    Params:
        ds: The daylight sensor dictionary.
    Returns:
        isDay: True if its bright enough to be daytime, False otherwise.'''
    return True

def pb_read(pb: dict) -> bool:
    '''
    Read the state of a push button.
    Params:
        pb: The push button dictionary.
    Returns:
        pushed: True if the button is currently being pushed, False otherwise.'''
    return False
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