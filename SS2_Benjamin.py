from pymata4 import pymata4
import time
import math
board = pymata4.Pymata4()
 
# #Pin for US1
# triggerPin_1 = 9
# echoPin_1 = 10
# # pin for US2
# triggerPin_2 = 11 
# echoPin_2 = 12
# configure pin mode as sonar
# board.set_pin_mode_sonar(triggerPin_1, echoPin_1, timeout=200000)
# board.set_pin_mode_sonar(triggerPin_2, echoPin_2, timeout=200000)

# small sleep to allow sonar to be configured correctly
time.sleep(0.5) 
initialTime = time.time()
pbLastTime = -30
ser = 5
rclk = 6
srclk = 7
pb = 1
ldr = 5
#PB
board.set_pin_mode_analog_input(pb)
board.set_pin_mode_analog_input(ldr)
board.set_pin_mode_digital_output(ser)
board.set_pin_mode_digital_output(rclk)
board.set_pin_mode_digital_output(srclk)
board.digital_write(srclk, 0)
board.digital_write(rclk, 0)

time.sleep(0.5)

print("CTRL+C to end program")

def storage_1 ():
    board.digital_write(ser,1)
    board.digital_write(srclk,1)
    board.digital_write(srclk,0)

def storage_0():
    board.digital_write(ser,0)
    board.digital_write(srclk,1)
    board.digital_write(srclk,0)
    
def print_out():
    board.digital_write(rclk, 1)
    board.digital_write(rclk, 0)  

def clear_lights():
    clear_storage()
    print_out()

def clear_storage():
    for _ in range (16):
        storage_0()

def shiftSequence(seq: int):
    '''Implementation by JEHR'''
    clear_storage()
    binLength = math.floor(math.log(seq, 2)) + 1
    for i in range(binLength):
        if seq & (2 ** (binLength - i - 1)) == 0:
            storage_0()
        else:
            storage_1()
    print_out()
          
def PL1_PL2(): 
    shiftSequence(0b10100100100)
    time.sleep(3)
    shiftSequence(0b1100100)
    time.sleep(2)

def TL4_TL5_day():
    global initialTime
    global timeNow
    if (timeNow - initialTime) < 5: #TL4 green
        shiftSequence(0b101000100001)
        
    elif 8 > (timeNow - initialTime) >= 5: #20 TL4 yellow
        shiftSequence(0b101000100010)
        # print("b")

    
    elif 13 > (timeNow - initialTime) >= 8: #3 TL5 green
        shiftSequence(0b101000001100)
        # print("c")
        
    elif 16 > (timeNow - initialTime) >= 13:#10 TL5 Yellow
        shiftSequence(0b101000010100)  
        # print("d")
        
    elif (timeNow - initialTime) >= 16:#3
        initialTime = timeNow

def TL4_TL5_night():
    global initialTime
    global timeNow
    if (timeNow - initialTime) < 8:#30
        # print("a")
        shiftSequence(0b101000100001) 
    
    elif 11 > (timeNow - initialTime) >= 8: 
        shiftSequence(0b101000100010)
        # print("b")

    
    elif 16 > (timeNow - initialTime) >= 11: #3
        shiftSequence(0b101000001100)
        # print("c")
        
    elif 19 > (timeNow - initialTime) >= 16:#5
        shiftSequence(0b101000010100)   
        # print("d")
        
    elif (timeNow - initialTime) >= 19:#3
        initialTime = timeNow

def afterButtonPushed():
    '''Implementation by JEHR'''
    global initialTime
    global pbLastTime
    time.sleep(3)
    PL1_PL2()
    initialTime = time.time()
    pbLastTime = time.time()

def SS2 ():
    time.sleep(0.1)
    global initialTime
    global pbLastTime
    initialTime = time.time()
    while True:
        global timeNow
        try:
            timeNow = time.time()
            pbTimeNow = time.time()
            pb_read = board.analog_read(pb)
            ldr_read = board.analog_read(ldr)
            time.sleep(0.1)
            if ldr_read[0] > 650:
                if (pbTimeNow - pbLastTime) >= 5: #30
                    
                    if (pb_read[0] < 75) and (timeNow - initialTime) < 5:
                        print("PB1 is pressed")
                        shiftSequence(0b101000100010)
                        afterButtonPushed()
                        # TL4_TL5_day()
                        # time.sleep(3) #30   
                        
                    elif (pb_read[0] < 75) and 8 > (timeNow - initialTime) >= 5:
                        
                        print("PB1 is pressed")
                        shiftSequence(0b101000100010)
                        afterButtonPushed()
                        
                    elif (pb_read[0] < 75) and 13 > (timeNow - initialTime) >= 8:
                        print("PB1 is pressed")
                        shiftSequence(0b101000010100) 
                        afterButtonPushed()
                        
                    elif (pb_read[0] < 75) and 16 > (timeNow - initialTime) >= 13:
                        print("PB1 is pressed")
                        shiftSequence(0b101000010100)  
                        afterButtonPushed()
                        
                    elif (100 > pb_read[0] >= 75) and (timeNow - initialTime) < 5:
                        print("PB2 is pressed")
                        shiftSequence(0b101000100010)
                        afterButtonPushed()
                        # TL4_TL5_day()
                        # time.sleep(3) #30   
                        
                    elif (100 > pb_read[0] >= 75) and 8 > (timeNow - initialTime) >= 5:
                        
                        print("PB2 is pressed")
                        shiftSequence(0b101000100010)
                        afterButtonPushed()
                        
                    elif (100 > pb_read[0] >= 75) and 13 > (timeNow - initialTime) >= 8:
                        print("PB2 is pressed")
                        shiftSequence(0b101000010100)  
                        afterButtonPushed()
                        
                    elif (100 > pb_read[0] >= 75) and 16 > (timeNow - initialTime) >= 13:
                        print("PB2 is pressed")
                        shiftSequence(0b101000010100)  
                        afterButtonPushed()
                    
                    else:
                    # print("day")
                        TL4_TL5_day()
   
                else:
                    # print("day")
                    TL4_TL5_day()
            
            elif ldr_read[0] <= 650:
                
                if (pbTimeNow - pbLastTime) >= 5: #30
                        
                    if (pb_read[0] < 75) and (timeNow - initialTime) < 8:
                        print("PB1 is pressed/N")
                        shiftSequence(0b101000100010)
                        afterButtonPushed()
                        # TL4_TL5_day()
                        # time.sleep(3) #30   
                        
                    elif (pb_read[0] < 75) and 11 > (timeNow - initialTime) >= 8:
                        
                        print("PB1 is pressed/N")
                        shiftSequence(0b101000100010)
                        afterButtonPushed()
                        
                    elif (pb_read[0] < 75) and 16 > (timeNow - initialTime) >= 11:
                        print("PB1 is pressed/N")
                        shiftSequence(0b101000010100)  
                        afterButtonPushed()
                        
                    elif (pb_read[0] < 75) and 19 > (timeNow - initialTime) >= 16:
                        print("PB1 is pressed/N")
                        shiftSequence(0b101000010100)
                        afterButtonPushed()
                        
                    elif (100 > pb_read[0] >= 75) and (timeNow - initialTime) < 8:
                        print("PB2 is pressed/N")
                        shiftSequence(0b101000100010)
                        afterButtonPushed()
                        # TL4_TL5_day()
                        # time.sleep(3) #30   
                        
                    elif (100 > pb_read[0] >= 75) and 11 > (timeNow - initialTime) >= 8:
                        
                        print("PB2 is pressed/N")
                        shiftSequence(0b101000100010)
                        afterButtonPushed()
                        
                    elif (100 > pb_read[0] >= 75) and 16 > (timeNow - initialTime) >= 11:
                        print("PB2 is pressed/N")
                        shiftSequence(0b101000010100)
                        afterButtonPushed()
                        
                    elif (100 > pb_read[0] >= 75) and 19 > (timeNow - initialTime) >= 16:
                        print("PB2 is pressed/N")
                        shiftSequence(0b101000010100)   
                        afterButtonPushed()
                        
                    else:
                        # print("day")
                        TL4_TL5_night()
                
                else:
                        # print("day")
                        TL4_TL5_night()
                        
        except KeyboardInterrupt:
            
            clear_lights()
            time.sleep(0.3)
            print("l")
            # board.shutdown()
            break
     
SS2()
# time.sleep(3)
# TL4_TL5()

# clear_lights()
# time.sleep(0.5)

board.shutdown()