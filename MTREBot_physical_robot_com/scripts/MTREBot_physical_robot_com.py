#!/usr/bin/env python

import rospy
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Twist
import sys
import tty
import termios

class JointGoalSetter:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('joint_goal_setter', anonymous=True)

        # Initialize MoveIt interface
        self.move_group = MoveGroupCommander("arm")

        # Setup keyboard input
        self.settings = termios.tcgetattr(sys.stdin)

        # Publisher for Twist messages
        self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    def set_joint_goal(self, joint_goal):
        """
        Function to set joint goal and move the arm.
        """
        # Set joint goal
        self.move_group.go(joint_goal, wait=True)

        # Ensure that there is no residual movement
        self.move_group.stop()

    def get_key(self):
        """
        Function to get a single key press from the keyboard.
        """
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def print_joint_values(self, joint_goal):
        """
        Function to print current joint values.
        """
        joint_names = self.move_group.get_active_joints()
        joint_values = self.move_group.get_current_joint_values()

        print("Current Joint Values:")
        for name, value in zip(joint_names, joint_values):
            print(f"{name}: {value:.2f}")
        print("")

    def publish_twist_message(self, linear_x, angular_z):
        """
        Function to publish Twist messages for controlling the rolling robot.
        """
        twist_msg = Twist()
        twist_msg.linear.x = linear_x
        twist_msg.angular.z = angular_z
        self.twist_pub.publish(twist_msg)

    def run(self):
        """
        Function to continuously read keyboard input and update joint angles or publish Twist messages.
        """
        joint_goal = [0, 0, 0, 0]  # Initial joint angles

        while True:
            # Print current joint values
            self.print_joint_values(joint_goal)

            key = self.get_key()

            # Increment or decrement joint angles based on key press
            if key == 'q':
                joint_goal[0] += 0.1
            elif key == 'a':
                joint_goal[0] -= 0.1
            elif key == 'w':
                joint_goal[1] += 0.1
            elif key == 's':
                joint_goal[1] -= 0.1
            elif key == 'e':
                joint_goal[2] += 0.1
            elif key == 'd':
                joint_goal[2] -= 0.1
            elif key == 'r':
                joint_goal[3] += 0.1
            elif key == 'f':
                joint_goal[3] -= 0.1
            # Publish Twist messages for controlling the rolling robot
            elif key == 'i':
                self.publish_twist_message(0.5, 0)
            elif key == 'j':
                self.publish_twist_message(0, 0.5)
            elif key == 'l':
                self.publish_twist_message(0, -0.5)
            elif key == 'k':
                self.publish_twist_message(-0.5, 0)
            # Stop the rolling robot when space bar is pressed
            elif key == ' ':
                self.publish_twist_message(0, 0)
            # Exit the program when 'esc' key is pressed
            elif key == '\x1b':
                break

            # Set the joint goal and move the arm
            self.set_joint_goal(joint_goal)

if __name__ == '__main__':
    try:
        joint_goal_setter = JointGoalSetter()
        joint_goal_setter.run()

    except rospy.ROSInterruptException:
        pass
