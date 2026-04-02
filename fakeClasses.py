'''Proof of concept for simulated classes to circumvent the no classes rule of the ENG1013 project.'''

from typing import Callable

# Create placeholder class to enable type checking
class Dice:
    def __init__(self) -> None:
        self.sides: int
    
    # Dummy implementation for type checking
    def roll(self) -> int: ...

# Helper function to abuse closures to imitate bound methods
def selfize(self: object, func: Callable):
    def inner(*args, **kwargs):
        return func(self, *args, **kwargs)
    return inner

# Actual implementation of roll
def roll(self: Dice) -> int:
    self.sides = 1 # chosen using fair roll, guranteed to be random
    return self.sides

def newObject(className: str) -> object:
    '''Create a basic object to tack fields onto.
    Functions are the simplest non-imported objects that support arbitrary attributes.'''
    def plc(): pass
    initFields(plc, [("__class_name__", className)])
    return plc

def initFields(base: object, fields: list[tuple[str, object]]):
    '''Initialise the fields of the class. Takes in the base object and a list of pairs. Each pair has the field name and its initial value.'''
    for (name, init) in fields:
        # Use setattr to set all relevant fields since it satisfies the type checker
        setattr(base, name, init)

def initMethods(base: object, fields: list[tuple[str, Callable]]):
    '''Initialise the methods of the class. Takes in the base object and a list of pairs. Each pair has the method name and its function object. Calls selfize to turn them into "bound methods."'''
    for (name, func) in fields:
        # Make sure to use selfize on functions to turn them into "bound methods"
        setattr(base, name, selfize(base, func))

# Accept an optional premade pbject for inheritance.
def newDice(sides, obj: object | None = None, parents: list[Callable[..., object]] = []) -> Dice:
    plc = newObject("Dice") if obj == None else obj
    for parent in parents:
        plc = parent(plc)
    initFields(plc, [("sides", sides)])
    initMethods(plc, [("roll", roll)])
    # Add type: ignore and the type checker is none the wiser
    return plc #type: ignore

# The returned value should act exactly like the imitated class, except for a few edge cases which hopefully should never come up.
die = newDice(6)
otherDie = newDice(6)
die.sides = 10
print(die.sides)
print(otherDie.sides)