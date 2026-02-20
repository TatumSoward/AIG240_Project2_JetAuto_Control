#!/usr/bin/env python3
"""
This code was made using the assistance of Google Gemini Gen AI
"""

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

# Function to get key presses (for ROS1 Indigo/Noetic)
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

#####################Square Sequence (Done by Gemini)#######################
def execute_square_sequence(pub, rate):
    # Speeds
    lin_spd = 0.5
    ang_spd = 0.5
    
    for i in range(2): # Repeat twice
        rospy.loginfo(f"Starting Sequence Loop {i+1}")
        
        # 1. Move forward 1m: (0,0,0) -> (1,0,0)
        # Time = 1m / 0.5m/s = 2s
        move_for_time(pub, rate, x=lin_spd, y=0, z=0, duration=2.0)

        # 2. Move sideways left 1m: (1,0,0) -> (1,1,0)
        # Note: Uses linear.y for strafing
        move_for_time(pub, rate, x=0, y=lin_spd, z=0, duration=2.0)

        # 3. Turn clockwise 90 degrees (1.57 radians)
        # Time = 1.57rad / 0.5rad/s = ~3.14s
        move_for_time(pub, rate, x=0, y=0, z=-ang_spd, duration=3.14)

        # 4. Move sideways right 1m: (1,1,-90) -> (0,1,-90)
        move_for_time(pub, rate, x=0, y=-lin_spd, z=0, duration=2.0)

################### The Drift (Done by Me + Some Gemini Research) ###############
        # 5. Drift: Move forward and turn (0,1,-90) -> (0,0,0)
        drift_duration = 3.0
        start_time = rospy.get_time()

        while not rospy.is_shutdown():
            elapsed = rospy.get_time() - start_time
            if elapsed > drift_duration:
                break 
            
            fraction = elapsed / drift_duration # percentage of time that has passed
            t = Twist()
            t.linear.x = 0.65 * (1 - fraction) # linear speed with acceleration
            t.angular.z = 0.85 * (fraction ** 0.5) # angular speed w/ acceleration
            
            pub.publish(t)
            rate.sleep()

        # Final Stop
        pub.publish(Twist())
########################################################################################
        
        # Stop briefly between loops
        move_for_time(pub, rate, 0, 0, 0, 1.0)

def move_for_time(pub, rate, x, y, z, duration):
    start_time = rospy.get_time()
    while rospy.get_time() - start_time < duration:
        t = Twist()
        t.linear.x = x
        t.linear.y = y
        t.angular.z = z
        pub.publish(t)
        rate.sleep()
    # Stop movement
    pub.publish(Twist())
############################################################################################

def wasd_teleop():
    rospy.init_node('jetauto_control', anonymous=True) # I changed the node name + publisher from turtle sim
    pub = rospy.Publisher('/jetauto_controller/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) # 10 Hz

    # Define movement parameters (adjust as needed)
    linear_speed = 1.0  # Forward/Backward speed
    angular_speed = 1.0 # Turning speed

    while not rospy.is_shutdown():
        ch = getch() # Get a single character input

        twist_msg = Twist() # Create a new Twist message

        if ch == 'w':
            twist_msg.linear.x = linear_speed # Move forward
        elif ch == 's':
            twist_msg.linear.x = -linear_speed # Move backward
        elif ch == 'a':
            twist_msg.angular.z = angular_speed # Turn left (counter-clockwise)
        elif ch == 'd':
            twist_msg.angular.z = -angular_speed # Turn right (clockwise)

############## Adding Diagonal Directional Keys (Done by Me) ##############
        elif ch == 'q':
            twist_msg.linear.x = linear_speed # Move forward then turn left
            twist_msg.angular.z = angular_speed
        elif ch == 'z':
            twist_msg.linear.x = -linear_speed # Move backwards then turn left
            twist_msg.angular.z = angular_speed
        elif ch == 'c':
            twist_msg.linear.x = -linear_speed # Move backwards then turn right
            twist_msg.angular.z = -angular_speed
        elif ch == 'e':
            twist_msg.linear.x = linear_speed # Move forward then turn right
            twist_msg.angular.z = -angular_speed
############################################################################

        elif ch == ' ': # SPACE BAR
            rospy.loginfo("Space bar pressed! Executing autonomous sequence...")
            execute_square_sequence(pub, rate)
            continue # Skip the normal publish at the bottom

        elif ch == 'x': # Quit
            break

        pub.publish(twist_msg) # Publish the command
        rate.sleep() # Sleep for a short duration


if __name__ == '__main__':
    try:
        wasd_teleop()
    except rospy.ROSInterruptException:
        pass

print("This is a test. The code works!")

