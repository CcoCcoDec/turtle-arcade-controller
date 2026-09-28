import math

from geometry_msgs.msg import Twist

from PyQt5.QtCore import QTimer


class MovementController:

    def __init__(self, node):

        self.node = node

        self.angular_speed = 1.0

        self.rotation_time = (
            (math.pi / 4)
            / self.angular_speed
        )

        self.rotation_timer = None


    # ==================================================
    # Forward
    # ==================================================

    def move_forward(self):

        msg = Twist()

        msg.linear.x = 2.0
        msg.angular.z = 0.0

        self.node.publisher.publish(msg)

        self.node.save_log(
            'MOVE_FORWARD'
        )


    # ==================================================
    # Backward
    # ==================================================

    def move_backward(self):

        msg = Twist()

        msg.linear.x = -2.0
        msg.angular.z = 0.0

        self.node.publisher.publish(msg)

        self.node.save_log(
            'MOVE_BACKWARD'
        )


    # ==================================================
    # Left
    # ==================================================

    def rotate_left(self):

        self.rotate_45(1)


    # ==================================================
    # Right
    # ==================================================

    def rotate_right(self):

        self.rotate_45(-1)


    # ==================================================
    # Rotate 45 degrees
    # ==================================================

    def rotate_45(self, direction):

        if self.rotation_timer is not None:

            self.rotation_timer.stop()
            self.rotation_timer = None

        msg = Twist()

        msg.angular.z = (
            self.angular_speed
            * direction
        )

        self.node.publisher.publish(msg)

        if direction > 0:

            self.node.save_log(
                'ROTATE_LEFT'
            )

        else:

            self.node.save_log(
                'ROTATE_RIGHT'
            )

        self.rotation_timer = QTimer()

        self.rotation_timer.setSingleShot(
            True
        )

        self.rotation_timer.timeout.connect(
            self.stop
        )

        self.rotation_timer.start(
            int(self.rotation_time * 1000)
        )


    # ==================================================
    # Stop
    # ==================================================

    def stop(self):

        msg = Twist()

        msg.linear.x = 0.0
        msg.angular.z = 0.0

        self.node.publisher.publish(msg)

        if self.rotation_timer is not None:

            self.rotation_timer.stop()
            self.rotation_timer = None