"""
ENG1013 - Engineering Smart Systems
Tunnel Ave Control Subsystem (Subsystem 2)

Implemented features:
- 2.R1
- 2.R2
- 2.R3
- 2.G1
- 2.G2
- 2.I1

Notes:
- 2.G3 is intentionally not implemented.
- This file assumes active-high outputs.
- The flashing frequency for PL1/PL2 red is generated in hardware by a
  single 555 timer. This code only enables or disables that flashing path.
- Buttons are assumed to be explicitly debounced in hardware.
- For integration with subsystem 3, either:
    1) call set_us5_state(True/False) from your integrated main loop, or
    2) set useUs5InputPin = True and wire a clean digital signal to us5InputPin.
"""

from pymata4 import pymata4
import time


# -----------------------------------------------------------------------------
# Pin configuration
# Update these pin numbers to match your actual circuit.
# The example values below suit a simple Arduino Uno-style direct I/O build.
# If you use A0/A1/A2 as digital pins on an Uno, their digital numbers are
# 14/15/16 respectively.
# -----------------------------------------------------------------------------

# TL4 - Tunnel Ave traffic light
# Red, Yellow, Green

tl4RedPin = 2
tl4YellowPin = 3
tl4GreenPin = 4

# TL5 - side road traffic light
# Red, Yellow, Green

tl5RedPin = 5
tl5YellowPin = 6
tl5GreenPin = 7

# Pedestrian lights PL1 and PL2
# Each light has red and green.
# For flashing red, the 555 timer should drive the red path through hardware.
# plFlashEnablePin should enable that hardware path (for example via transistor,
# MOSFET or gating arrangement in your circuit).

pl1RedPin = 8
pl1GreenPin = 9
pl2RedPin = 10
pl2GreenPin = 11
plFlashEnablePin = 12

# Pedestrian buttons PB1 and PB2
pb1Pin = 14
pb2Pin = 15

# Optional US5 digital integration input.
# Leave this disabled if subsystem 3 will pass the state in software using
# set_us5_state().
useUs5InputPin = False
us5InputPin = 16

# Input configuration
buttonsUseInternalPullup = False
buttonPressedValue = 0 if buttonsUseInternalPullup else 1
us5DetectedValue = 1

# -----------------------------------------------------------------------------
# Timing constants from specification
# -----------------------------------------------------------------------------

tl4GreenTime = 20.0
tl5GreenTime = 10.0
yellowTime = 3.0
pedestrianDelayTime = 2.0
pedestrianGreenTime = 3.0
pedestrianFlashTime = 2.0
pedestrianCooldownTime = 30.0
loopDelayTime = 0.01

# -----------------------------------------------------------------------------
# Global runtime state
# -----------------------------------------------------------------------------

board: pymata4.Pymata4 = None #type: ignore
boardOwnedBySubsystemTwo = 0

tl4State = "red"
tl5State = "red"
pedestrianState = "solidRed"

systemState = "startup"
stateStartTime = 0.0

lastPedestrianServiceTime = -1000.0
pedestrianRequestPending = 0
pedestrianRequestPrinted = 0
pedestrianRequestTime = 0.0
pedestrianRoadToStop = "tl4"

us5DetectedSoftware = 0
us5OverrideActive = 0

previousPb1Value = 0
previousPb2Value = 0


# -----------------------------------------------------------------------------
# Time and console helpers
# -----------------------------------------------------------------------------

def current_time():
    """Return a monotonic time value for subsystem timing."""
    return time.monotonic()


def get_time_stamp_string():
    """Return a wall-clock timestamp string for console output."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def log_event(messageText):
    """Print a clear, non-spamming console message with a timestamp."""
    print(f"[{get_time_stamp_string()}] Subsystem 2: {messageText}")


# -----------------------------------------------------------------------------
# Low-level I/O helpers
# -----------------------------------------------------------------------------

def write_pin(pinNumber, value):
    """Write a logical 0 or 1 to an Arduino digital output pin."""
    board.digital_write(pinNumber, value)


def read_digital_input(pinNumber):
    """Read the last cached pymata4 digital input value for a pin."""
    data = board.digital_read(pinNumber)
    if data:
        return data[0]
    return 0


def configure_button_pin(pinNumber):
    """Configure a pedestrian button pin as a digital input."""
    if buttonsUseInternalPullup:
        board.set_pin_mode_digital_input_pullup(pinNumber)
    else:
        board.set_pin_mode_digital_input(pinNumber)


# -----------------------------------------------------------------------------
# Traffic light output helpers
# -----------------------------------------------------------------------------

def set_tl4_red():
    """Set TL4 to red."""
    global tl4State
    write_pin(tl4RedPin, 1)
    write_pin(tl4YellowPin, 0)
    write_pin(tl4GreenPin, 0)
    tl4State = "red"



def set_tl4_yellow():
    """Set TL4 to yellow."""
    global tl4State
    write_pin(tl4RedPin, 0)
    write_pin(tl4YellowPin, 1)
    write_pin(tl4GreenPin, 0)
    tl4State = "yellow"



def set_tl4_green():
    """Set TL4 to green."""
    global tl4State
    write_pin(tl4RedPin, 0)
    write_pin(tl4YellowPin, 0)
    write_pin(tl4GreenPin, 1)
    tl4State = "green"



def set_tl5_red():
    """Set TL5 to red."""
    global tl5State
    write_pin(tl5RedPin, 1)
    write_pin(tl5YellowPin, 0)
    write_pin(tl5GreenPin, 0)
    tl5State = "red"



def set_tl5_yellow():
    """Set TL5 to yellow."""
    global tl5State
    write_pin(tl5RedPin, 0)
    write_pin(tl5YellowPin, 1)
    write_pin(tl5GreenPin, 0)
    tl5State = "yellow"



def set_tl5_green():
    """Set TL5 to green."""
    global tl5State
    write_pin(tl5RedPin, 0)
    write_pin(tl5YellowPin, 0)
    write_pin(tl5GreenPin, 1)
    tl5State = "green"


# -----------------------------------------------------------------------------
# Pedestrian light helpers
# -----------------------------------------------------------------------------

def set_pedestrian_solid_red():
    """Set PL1 and PL2 to solid red."""
    global pedestrianState
    write_pin(plFlashEnablePin, 0)
    write_pin(pl1GreenPin, 0)
    write_pin(pl2GreenPin, 0)
    write_pin(pl1RedPin, 1)
    write_pin(pl2RedPin, 1)
    pedestrianState = "solidRed"



def set_pedestrian_green():
    """Set PL1 and PL2 to green."""
    global pedestrianState
    write_pin(plFlashEnablePin, 0)
    write_pin(pl1RedPin, 0)
    write_pin(pl2RedPin, 0)
    write_pin(pl1GreenPin, 1)
    write_pin(pl2GreenPin, 1)
    pedestrianState = "green"



def set_pedestrian_flashing_red():
    """
    Set PL1 and PL2 to flashing red.

    The flash frequency itself must come from a single 555 timer as required by
    feature 2.G2. Software only enables that flashing path here.
    """
    global pedestrianState
    write_pin(pl1RedPin, 0)
    write_pin(pl2RedPin, 0)
    write_pin(pl1GreenPin, 0)
    write_pin(pl2GreenPin, 0)
    write_pin(plFlashEnablePin, 1)
    pedestrianState = "flashingRed"



def set_all_outputs_off():
    """Turn all subsystem two outputs off."""
    write_pin(tl4RedPin, 0)
    write_pin(tl4YellowPin, 0)
    write_pin(tl4GreenPin, 0)
    write_pin(tl5RedPin, 0)
    write_pin(tl5YellowPin, 0)
    write_pin(tl5GreenPin, 0)
    write_pin(pl1RedPin, 0)
    write_pin(pl1GreenPin, 0)
    write_pin(pl2RedPin, 0)
    write_pin(pl2GreenPin, 0)
    write_pin(plFlashEnablePin, 0)


# -----------------------------------------------------------------------------
# Integration helpers
# -----------------------------------------------------------------------------

def set_us5_state(isDetected):
    """
    Receive the integrated US5 vehicle-detected state from subsystem 3.

    This should be called by your integrated main loop if subsystem 3 owns the
    real US5 sensor reading and filtering.
    """
    global us5DetectedSoftware
    if isDetected:
        us5DetectedSoftware = 1
    else:
        us5DetectedSoftware = 0



def get_us5_state():
    """Return the current integrated US5 detection state."""
    if useUs5InputPin:
        if read_digital_input(us5InputPin) == us5DetectedValue:
            return 1
        return 0

    return us5DetectedSoftware


# -----------------------------------------------------------------------------
# Setup and shutdown
# -----------------------------------------------------------------------------

def configure_pin_modes():
    """Configure all pins used by subsystem two."""
    board.set_pin_mode_digital_output(tl4RedPin)
    board.set_pin_mode_digital_output(tl4YellowPin)
    board.set_pin_mode_digital_output(tl4GreenPin)

    board.set_pin_mode_digital_output(tl5RedPin)
    board.set_pin_mode_digital_output(tl5YellowPin)
    board.set_pin_mode_digital_output(tl5GreenPin)

    board.set_pin_mode_digital_output(pl1RedPin)
    board.set_pin_mode_digital_output(pl1GreenPin)
    board.set_pin_mode_digital_output(pl2RedPin)
    board.set_pin_mode_digital_output(pl2GreenPin)
    board.set_pin_mode_digital_output(plFlashEnablePin)

    configure_button_pin(pb1Pin)
    configure_button_pin(pb2Pin)

    if useUs5InputPin:
        board.set_pin_mode_digital_input(us5InputPin)



def initialise_runtime_state():
    """Initialise subsystem state to the normal starting condition."""
    global systemState
    global stateStartTime
    global lastPedestrianServiceTime
    global pedestrianRequestPending
    global pedestrianRequestPrinted
    global pedestrianRequestTime
    global pedestrianRoadToStop
    global us5OverrideActive
    global previousPb1Value
    global previousPb2Value

    set_tl4_green()
    set_tl5_red()
    set_pedestrian_solid_red()

    systemState = "normalTl4Green"
    stateStartTime = current_time()
    lastPedestrianServiceTime = -1000.0
    pedestrianRequestPending = 0
    pedestrianRequestPrinted = 0
    pedestrianRequestTime = 0.0
    pedestrianRoadToStop = "tl4"
    us5OverrideActive = 0

    previousPb1Value = read_digital_input(pb1Pin)
    previousPb2Value = read_digital_input(pb2Pin)

    log_event("started normal cycle (TL4 green, TL5 red, PL solid red).")



def setup_subsystem_two(sharedBoard=None):
    """
    Configure subsystem two for standalone use or for an integrated system.

    If sharedBoard is provided, subsystem two uses that existing Pymata4 board.
    Otherwise, subsystem two creates and owns its own board instance.
    """
    global board
    global boardOwnedBySubsystemTwo

    if sharedBoard is None:
        board = pymata4.Pymata4()
        boardOwnedBySubsystemTwo = 1
    else:
        board = sharedBoard
        boardOwnedBySubsystemTwo = 0

    configure_pin_modes()
    initialise_runtime_state()

    return board



def shutdown_subsystem_two(shutdownBoard=False):
    """Turn subsystem two outputs off and optionally shut down the board."""
    set_all_outputs_off()

    if shutdownBoard and board is not None:
        board.shutdown()


# -----------------------------------------------------------------------------
# Input processing
# -----------------------------------------------------------------------------

def register_pedestrian_request():
    """Register a single pending pedestrian request and print it once."""
    global pedestrianRequestPending
    global pedestrianRequestPrinted
    global pedestrianRequestTime

    if pedestrianRequestPending == 0:
        pedestrianRequestPending = 1
        pedestrianRequestPrinted = 1
        pedestrianRequestTime = current_time()
        log_event("pedestrian request received from PB1/PB2.")



def poll_pedestrian_buttons():
    """Detect button press edges from PB1 and PB2."""
    global previousPb1Value
    global previousPb2Value

    pb1Value = read_digital_input(pb1Pin)
    pb2Value = read_digital_input(pb2Pin)

    pb1Pressed = pb1Value == buttonPressedValue and previousPb1Value != buttonPressedValue
    pb2Pressed = pb2Value == buttonPressedValue and previousPb2Value != buttonPressedValue

    if pb1Pressed or pb2Pressed:
        if us5OverrideActive == 0:
            register_pedestrian_request()

    previousPb1Value = pb1Value
    previousPb2Value = pb2Value


# -----------------------------------------------------------------------------
# Pedestrian sequence control
# -----------------------------------------------------------------------------

def pedestrian_request_ready(nowTime):
    """Return 1 if the pending request may begin its sequence now."""
    if pedestrianRequestPending == 0:
        return 0

    if nowTime - pedestrianRequestTime < pedestrianDelayTime:
        return 0

    if nowTime - lastPedestrianServiceTime < pedestrianCooldownTime:
        return 0

    if us5OverrideActive == 1:
        return 0

    if systemState in [
        "normalTl4Green",
        "normalTl4Yellow",
        "normalTl5Green",
        "normalTl5Yellow"
    ]:
        return 1

    return 0



def start_pedestrian_sequence(nowTime):
    """
    Start the 2.R1 pedestrian sequence after the request delay and cooldown.

    If TL5 is not currently red, TL5 is the road stopped.
    Otherwise TL4 is the road stopped.
    """
    global systemState
    global stateStartTime
    global pedestrianRoadToStop

    if tl5State != "red":
        pedestrianRoadToStop = "tl5"
        set_tl4_red()
        set_tl5_yellow()
    else:
        pedestrianRoadToStop = "tl4"
        set_tl5_red()
        set_tl4_yellow()

    set_pedestrian_solid_red()

    systemState = "pedestrianRoadYellow"
    stateStartTime = nowTime

    log_event("pedestrian crossing sequence started.")



def complete_pedestrian_sequence(nowTime):
    """Return to the normal TL4-green starting state after the pedestrian cycle."""
    global systemState
    global stateStartTime
    global lastPedestrianServiceTime
    global pedestrianRequestPending
    global pedestrianRequestPrinted
    global pedestrianRequestTime

    set_pedestrian_solid_red()
    set_tl4_green()
    set_tl5_red()

    systemState = "normalTl4Green"
    stateStartTime = nowTime
    lastPedestrianServiceTime = nowTime

    pedestrianRequestPending = 0
    pedestrianRequestPrinted = 0
    pedestrianRequestTime = 0.0

    log_event("pedestrian sequence finished. Normal cycle restarted with TL4 green.")


# -----------------------------------------------------------------------------
# US5 integration override control (2.I1)
# -----------------------------------------------------------------------------

def clear_pending_pedestrian_request():
    """Clear any pending pedestrian request when a higher-priority override begins."""
    global pedestrianRequestPending
    global pedestrianRequestPrinted
    global pedestrianRequestTime

    pedestrianRequestPending = 0
    pedestrianRequestPrinted = 0
    pedestrianRequestTime = 0.0



def start_us5_override(nowTime):
    """
    Start the subsystem 3 integration override described by feature 2.I1.

    This override has priority over the normal traffic cycle and any pending
    pedestrian button request.
    """
    global systemState
    global stateStartTime
    global us5OverrideActive

    us5OverrideActive = 1
    clear_pending_pedestrian_request()

    if tl4State != "red":
        set_tl4_yellow()
    else:
        set_tl4_red()

    if tl5State != "red":
        set_tl5_yellow()
    else:
        set_tl5_red()

    set_pedestrian_solid_red()

    if tl4State == "red" and tl5State == "red":
        set_pedestrian_green()
        systemState = "us5PedestrianGreen"
    else:
        systemState = "us5RoadsToRed"

    stateStartTime = nowTime

    log_event("US5 override started. Tunnel Ave traffic is being stopped.")



def begin_us5_exit_sequence(nowTime):
    """Begin the exit sequence after US5 is no longer detecting a vehicle."""
    global systemState
    global stateStartTime

    set_pedestrian_flashing_red()
    systemState = "us5PedestrianFlash"
    stateStartTime = nowTime

    log_event("US5 clear detected. Restoring normal cycle.")



def complete_us5_override(nowTime):
    """Finish the US5 override and restart the normal TL4-green cycle."""
    global systemState
    global stateStartTime
    global us5OverrideActive

    set_pedestrian_solid_red()
    set_tl4_green()
    set_tl5_red()

    systemState = "normalTl4Green"
    stateStartTime = nowTime
    us5OverrideActive = 0

    log_event("US5 override finished. Normal TL4/TL5 cycle resumed.")



def update_us5_override(nowTime):
    """Start or progress the US5 integration override if required."""
    us5State = get_us5_state()

    if us5State == 1 and us5OverrideActive == 0:
        start_us5_override(nowTime)
        return

    if us5OverrideActive == 1 and systemState == "us5PedestrianGreen" and us5State == 0:
        begin_us5_exit_sequence(nowTime)


# -----------------------------------------------------------------------------
# Main state machine updates
# -----------------------------------------------------------------------------

def update_normal_cycle(nowTime):
    """Update the base 20s / 10s TL4/TL5 cycle from feature 2.R3."""
    global systemState
    global stateStartTime

    if systemState == "normalTl4Green":
        if nowTime - stateStartTime >= tl4GreenTime:
            set_tl4_yellow()
            set_tl5_red()
            set_pedestrian_solid_red()
            systemState = "normalTl4Yellow"
            stateStartTime = nowTime

    elif systemState == "normalTl4Yellow":
        if nowTime - stateStartTime >= yellowTime:
            set_tl4_red()
            set_tl5_green()
            set_pedestrian_solid_red()
            systemState = "normalTl5Green"
            stateStartTime = nowTime

    elif systemState == "normalTl5Green":
        if nowTime - stateStartTime >= tl5GreenTime:
            set_tl4_red()
            set_tl5_yellow()
            set_pedestrian_solid_red()
            systemState = "normalTl5Yellow"
            stateStartTime = nowTime

    elif systemState == "normalTl5Yellow":
        if nowTime - stateStartTime >= yellowTime:
            set_tl4_green()
            set_tl5_red()
            set_pedestrian_solid_red()
            systemState = "normalTl4Green"
            stateStartTime = nowTime



def update_pedestrian_sequence(nowTime):
    """Update the pedestrian crossing sequence states."""
    global systemState
    global stateStartTime

    if systemState == "pedestrianRoadYellow":
        if nowTime - stateStartTime >= yellowTime:
            set_tl4_red()
            set_tl5_red()
            set_pedestrian_green()
            systemState = "pedestrianGreen"
            stateStartTime = nowTime

    elif systemState == "pedestrianGreen":
        if nowTime - stateStartTime >= pedestrianGreenTime:
            set_pedestrian_flashing_red()
            systemState = "pedestrianFlash"
            stateStartTime = nowTime

    elif systemState == "pedestrianFlash":
        if nowTime - stateStartTime >= pedestrianFlashTime:
            complete_pedestrian_sequence(nowTime)



def update_us5_sequence(nowTime):
    """Update the active US5 override states."""
    global systemState
    global stateStartTime

    if systemState == "us5RoadsToRed":
        if nowTime - stateStartTime >= yellowTime:
            set_tl4_red()
            set_tl5_red()
            set_pedestrian_green()
            systemState = "us5PedestrianGreen"
            stateStartTime = nowTime

    elif systemState == "us5PedestrianFlash":
        if nowTime - stateStartTime >= pedestrianFlashTime:
            complete_us5_override(nowTime)



def update_state_machine(nowTime):
    """Advance whichever subsystem state is currently active."""
    if systemState in [
        "normalTl4Green",
        "normalTl4Yellow",
        "normalTl5Green",
        "normalTl5Yellow"
    ]:
        update_normal_cycle(nowTime)

    elif systemState in [
        "pedestrianRoadYellow",
        "pedestrianGreen",
        "pedestrianFlash"
    ]:
        update_pedestrian_sequence(nowTime)

    elif systemState in [
        "us5RoadsToRed",
        "us5PedestrianGreen",
        "us5PedestrianFlash"
    ]:
        update_us5_sequence(nowTime)


# -----------------------------------------------------------------------------
# Public loop functions
# -----------------------------------------------------------------------------

def subsystem_two_loop():
    """
    Run one non-blocking iteration of subsystem two.

    Use this function inside a shared main loop for full-system integration.
    """
    nowTime = current_time()

    poll_pedestrian_buttons()
    update_us5_override(nowTime)

    if pedestrian_request_ready(nowTime):
        start_pedestrian_sequence(nowTime)

    update_state_machine(nowTime)



def run_subsystem_two():
    """
    Standalone entry point for subsystem two.

    This is useful for testing subsystem two on its own. For full integration,
    call setup_subsystem_two(sharedBoard), then repeatedly call
    subsystem_two_loop() from your main.py file.
    """
    setup_subsystem_two()

    try:
        while True:
            subsystem_two_loop()
            time.sleep(loopDelayTime)

    except KeyboardInterrupt:
        log_event("KeyboardInterrupt received. Shutting down subsystem two.")
        shutdown_subsystem_two(True)


# -----------------------------------------------------------------------------
# Standalone execution
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_subsystem_two()
