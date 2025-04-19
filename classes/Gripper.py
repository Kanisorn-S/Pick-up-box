import socket
import time

class Gripper:
    def __init__(self, robot_ip: str, gripper_port: int = 63352):
        # Initialize the gripper connection
        self.g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.g.connect((robot_ip, gripper_port))
        self.g.sendall(b'GET POS\n')
        g_recv = str(self.g.recv(10), 'UTF-8')
        # Check for gripper response
        if g_recv:
            # If the gripper connection is established, initialize the gripper
            self.g.send(b'SET ACT 1\n')
            self.g.recv(10)
            time.sleep(3)
            self.g.send(b'SET GTO 1\n')
            # Set the speed and force of the gripper to max
            self.g.send(b'SET SPE 255\n')
            self.g.send(b'SET FOR 255\n')
            print('Gripper Activated')

    # Control the gripper to open or close
    def control_gripper(self, activate: bool):
        self.g.send(f"SET POS {255 if activate else 0}\n".encode("UTF-8"))
        time.sleep(0.2)
