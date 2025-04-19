from classes.URARM import URARM
from classes.Gripper import Gripper
from classes.VisionSystem import VisionSystem
import time
import math
import socket

def main():
    # Define IP addresses for the robot and the vision system
    robot_ip = '10.10.0.14'
    vs_ip = '10.10.1.10'

    # Initialize the robot, gripper, conveyor belt, and vision system
    robot = URARM(robot_ip)
    gripper = Gripper(robot_ip)
    vision = VisionSystem(vs_ip)

    # Move the robot to the home position
    robot.move_home()

    # Initialize the connection with conveyor belt
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.bind(('0.0.0.0', 2002))
    c.listen(1)
    print("Conveyor belt socket is listening")
    conv, addr = c.accept()
    print(f"Connected by {addr}")
    # Activate the conveyor belt
    conv.sendall(b'activate,tcp\n')
    time.sleep(1)
    conv.sendall(b'pwr_on,conv,0\n')
    time.sleep(1)
    conv.sendall(b'set_vel,conv,30\n')
    time.sleep(1)
    conv.sendall(b'jog_fwd,conv,0\n')

    # Get and process the x, y coordinates and orientation of the object from the vision system
    x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2 = vision.receive_data()
    degree, x_coor, y_coor = vision.find_coords(x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2)
    x_coor_rel, y_coor_rel = vision.offset_camera(x_coor, y_coor)
    print(f"Degree: {degree}, x_coor: {x_coor_rel}, y_coor: {y_coor_rel}")

    # Move the robot to the object location and pick up the object
    robot.grab_after_t(x_rel=x_coor_rel, y_rel=y_coor_rel, rz=-degree, t1=0.7, t2=0.7, t3=0.7, t4=0.7)
    gripper.control_gripper(True)
    robot.move_home()

    # Stop the conveyor belt
    conv.sendall(b'jog_stop,conv,0\n')
    time.sleep(1)

# Move the robot to the home position
def home():
    # Define IP addresses for the robot, vision system, and conveyor belt
    robot_ip = '10.10.0.14'


    # Initialize the robot, gripper, conveyor belt, and vision system
    robot = URARM(robot_ip)


    # Move the robot to the home position
    robot.move_home()

if __name__ == '__main__':
    main()
    # home()
