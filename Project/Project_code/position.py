#import statements
import sys
import math
import time
import datetime
import random
import traceback
import threading
import keyboard


# Import the xArm libraries
try:
    from xarm.tools import utils
except:
    pass
from xarm import version
from xarm.wrapper import XArmAPI
def pprint(*args, **kwargs):
    try:
        stack_tuple = traceback.extract_stack(limit=2)[0]
        print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
    except:
        print(*args, **kwargs)
pprint('xArm-Python-SDK Version:{}'.format(version.__version__))


# Initialize xArm
arm = XArmAPI('10.2.172.20')
arm.clean_warn()
arm.clean_error()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)


# Defining zones so the arm knows where it is
def is_within_zone1(position):
    if isinstance(position, tuple) and len(position) == 2:
        coords = position[1]  # Extract the list of coordinates from current_position
        if len(coords) >= 2:
            x, y = coords[0], coords[1]  # Extract x and y coordinates
            return 0 <= x <= 425 and -405 <= y <= 0
    return False

def is_within_zone2(position):
    if isinstance(position, tuple) and len(position) == 2:
        coords = position[1]  # Extract the list of coordinates from current_position
        if len(coords) >= 2:
            x, y = coords[0], coords[1]  # Extract x and y coordinates
            return 0 <= x <= 425 and 0 <= y <= 405
    return False

def is_within_zone3(position):
    if isinstance(position, tuple) and len(position) == 2:
        coords = position[1]  # Extract the list of coordinates from current_position
        if len(coords) >= 2:
            x, y = coords[0], coords[1]  # Extract x and y coordinates
            return -425 <= x <= 0 and 0 <= y <= 405
    return False

def is_within_zone4(position):
    if isinstance(position, tuple) and len(position) == 2:
        coords = position[1]  # Extract the list of coordinates from current_position
        if len(coords) >= 2:
            x, y = coords[0], coords[1]  # Extract x and y coordinates
            return -425 <= x <= 0 and -405 <= y <= 0
    return False


# Define the parameters for the arm
variables = {}
params = {'speed': 300, 'acc': 2000, 'angle_speed': 20, 'angle_acc': 500, 'events': {}, 'variables': variables, 'callback_in_thread': True, 'quit': False}
x_val = 410# Define the boundary x coordinate value
y_val = 380 # Define the boundary y coordinate value
height = 330 # Define the height of the arm
current_position = None # Variable to store the current position of the arm => no initial value needed since every use the position is called on


# Define action functions responsible for moving the arm to a specified positions
# Function to move to position 1
def action1():
    
    get_current_position()

    global current_position

    if is_within_zone3(current_position):
        print("Passing through zone 2")
        code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height , 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
    
    elif is_within_zone4(current_position):
        print("Passing through zone 3")
        code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        print("Passing through zone 2")
        code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height , 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

    print("Moving to position 1")
    code = arm.set_position(*[x_val, -y_val, height , 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# Function to move to position 2
def action2():
        
    get_current_position()

    global current_position

    if is_within_zone3(current_position):
        print("Passing through zone 2")
        code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height , 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
    
    elif is_within_zone4(current_position):
        print("Passing through zone 3")
        code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        print("Passing through zone 2")
        code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height , 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

    print("Moving to position 2")
    code = arm.set_position(*[x_val/2, -y_val/2, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# Function to move to position 3
def action3():
        
    get_current_position()

    global current_position

    if get_joint0_angle_degrees() > 270:
        action7()
    
    if is_within_zone4(current_position):
        print("Passing through zone 3")
        code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

    print("Moving to position 3")
    code = arm.set_position(*[x_val, y_val, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# Function to move to position 4
def action4():
        
    get_current_position()

    global current_position

    if is_within_zone2(current_position):
        print("Passing through zone 3")
        code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        
    
    elif is_within_zone1(current_position):
        print("Passing through zone 2")
        code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        print("Passing through zone 3")
        code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

    print("Moving to position 4")
    code = arm.set_position(*[-x_val/2, -y_val/2, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# Function to move to position 6
def action6():
        
    get_current_position()

    global current_position

    if is_within_zone4(current_position):
        print("Passing through zone 3")
        code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

    print("Moving to position 6")
    code = arm.set_position(*[x_val/2, y_val/2, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# Function to move to position 7
def action7():
        
    get_current_position()

    global current_position

    if is_within_zone2(current_position):
        print("Passing through zone 3")
        code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        
    
    elif is_within_zone1(current_position):
        print("Passing through zone 2")
        code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        print("Passing through zone 3")
        code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

    print("Moving to position 7")
    code = arm.set_position(*[-x_val, -y_val, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# Function to move to position 8
def action8():
        
    get_current_position()

    global current_position

    if is_within_zone1(current_position):
        print("Passing through zone 2")
        code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

    print("Moving to position 8")
    code = arm.set_position(*[-x_val/2, y_val/2, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# Function to move to position 9
def action9():
        
    get_current_position()

    global current_position

    if is_within_zone1(current_position):
        print("Passing through zone 2")
        code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

    print("Moving to position 9")
    code = arm.set_position(*[-x_val, y_val, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)


# Function to move to position up
# def actionUp():
        
#     get_current_position()

#     global current_position

#     if is_within_zone1(current_position):
#         print("Passing through zone 2")
#         code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
    
#     if is_within_zone2(current_position):
#         print("Passing through zone 3")
#         code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

#     print("Moving to position Up")
#     code = arm.set_position(*[-x_val, 4.0, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# # Function to move to position down
# def actionDown():
        
#     get_current_position()

#     global current_position

#     if is_within_zone3(current_position):
#         print("Passing through zone 2")
#         code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
    
#     elif is_within_zone4(current_position):
#         print("Passing through zone 3")
#         code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
#         print("Passing through zone 2")
#         code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
    
#     print("Moving to position Down")
#     code = arm.set_position(*[x_val, -4.0, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# # Function to move to position left
# def actionLeft():
        
#     get_current_position()

#     global current_position

#     if is_within_zone3(current_position):
#         print("Passing through zone 3")
#         code = arm.set_position(*[(-x_val*3)/4, (-y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        

#     elif is_within_zone2(current_position):
#         print("Passing through zone 3")
#         code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        
    
#     elif is_within_zone1(current_position):
#         print("Passing through zone 2")
#         code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
#         print("Passing through zone 3")
#         code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

#     print("Moving to position Left")
#     code = arm.set_position(*[-4.0, -y_val, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

# # Function to move to position right
# def actionRight():
        
#     get_current_position()

#     global current_position

#     if is_within_zone4(current_position):
#         print("Passing through zone 3")
#         code = arm.set_position(*[(-x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
    
#     elif is_within_zone1(current_position):
#         print("Passing through zone 2")
#         code = arm.set_position(*[(x_val*3)/4, (y_val*3)/4, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
       

#     print("Moving to position Right")
#     code = arm.set_position(*[4.0, y_val, height, 180.0, 0.0, 90.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)

def get_current_position():
    # Retrieve current Cartesian position of the arm
    global current_position

    current_position = arm.get_position()

    print("Current position: ", current_position)

def get_joint0_angle_degrees():
    # Get the current angles of all the joints
    joint_angles_tuple = arm.get_servo_angle()

    # Check if joint_angles_tuple is None
    if joint_angles_tuple is None:
        print("Error: Failed to get joint angles.")
        return None

    # Extract the list of joint angles from the tuple
    joint_angles = joint_angles_tuple[1]

    # Extract the angle of the 0 joint
    joint0_angle_degrees = joint_angles[0]

    print("Joint 0 angle in degrees: ", joint0_angle_degrees)

    return joint0_angle_degrees



# Register callback functions for key press events
keyboard.add_hotkey('1', action1)
keyboard.add_hotkey('2', action2)
keyboard.add_hotkey('3', action3)
keyboard.add_hotkey('4', action4)
keyboard.add_hotkey('6', action6)
keyboard.add_hotkey('7', action7)
keyboard.add_hotkey('8', action8)
keyboard.add_hotkey('9', action9)
# keyboard.add_hotkey('up', actionUp)
# keyboard.add_hotkey('down', actionDown)
# keyboard.add_hotkey('left', actionLeft)
# keyboard.add_hotkey('right', actionRight)


# Function to handle errors and warnings
def error_warn_change_callback(data):
    if data and data['error_code'] != 0:
        params['quit'] = True
        pprint('err={}, quit'.format(data['error_code']))
        arm.release_error_warn_changed_callback(error_warn_change_callback)
arm.register_error_warn_changed_callback(error_warn_change_callback)

# Function to handle state changes
def state_changed_callback(data):
    if data and data['state'] == 4:
        if arm.version_number[0] > 1 or (arm.version_number[0] == 1 and arm.version_number[1] > 1):
            params['quit'] = True
            pprint('state=4, quit')
            arm.release_state_changed_callback(state_changed_callback)
arm.register_state_changed_callback(state_changed_callback)

# Function to handle counter value changes
if hasattr(arm, 'register_count_changed_callback'):
    def count_changed_callback(data):
        if not params['quit']:
            pprint('counter val: {}'.format(data['count']))
    arm.register_count_changed_callback(count_changed_callback)

# Function to handle connection changes
def connect_changed_callback(data):
    if data and not data['connected']:
        params['quit'] = True
        pprint('disconnect, connected={}, reported={}, quit'.format(data['connected'], data['reported']))
        arm.release_connect_changed_callback(error_warn_change_callback)
arm.register_connect_changed_callback(connect_changed_callback)

# Loop to keep the script running and waiting for keyboard input
try:
    while True:
        time.sleep(0.1)  # Adjust the sleep time as needed
except KeyboardInterrupt:
    pass
finally:
    # Release all events
    if hasattr(arm, 'release_count_changed_callback'):
        arm.release_count_changed_callback(count_changed_callback)
    arm.release_error_warn_changed_callback(state_changed_callback)
    arm.release_state_changed_callback(state_changed_callback)
    arm.release_connect_changed_callback(error_warn_change_callback)
