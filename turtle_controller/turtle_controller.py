import sys

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from turtlesim.srv import SetPen
from turtlesim.srv import Kill
from turtlesim.srv import Spawn

from std_srvs.srv import Empty

from rcl_interfaces.srv import SetParameters

from PyQt5.QtWidgets import QApplication

from .db import Database
from .movement import MovementController
from .random_features import RandomFeatures
from .gui import TurtleGUI


class TurtleController(Node):

    def __init__(self):

        super().__init__(
            'turtle_controller'
        )

        # ==================================================
        # Database
        # ==================================================

        self.db = Database()

        # ==================================================
        # Turtle state
        # ==================================================

        self.x = 5.54
        self.y = 5.54
        self.theta = 0.0

        # ==================================================
        # ROS Publisher
        # ==================================================

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # ==================================================
        # ROS Subscriber
        # ==================================================

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # ==================================================
        # ROS Services
        # ==================================================

        self.pen_client = self.create_client(
            SetPen,
            '/turtle1/set_pen'
        )

        self.kill_client = self.create_client(
            Kill,
            '/kill'
        )

        self.spawn_client = self.create_client(
            Spawn,
            '/spawn'
        )

        self.clear_client = self.create_client(
            Empty,
            '/clear'
        )

        self.parameter_client = self.create_client(
            SetParameters,
            '/turtlesim/set_parameters'
        )

        # ==================================================
        # Controllers
        # ==================================================

        self.movement = MovementController(
            self
        )

        self.random_features = RandomFeatures(
            self
        )


    # ======================================================
    # Pose Callback
    # ======================================================

    def pose_callback(self, msg):

        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta


    # ======================================================
    # Save Log
    # ======================================================

    def save_log(self, action):

        self.db.insert_log(
            self.x,
            self.y,
            self.theta,
            action
        )


    # ======================================================
    # Reset
    # ======================================================

        # ======================================================
    # Reset
    # ======================================================

    def reset(self):

        # ==================================================
        # Stop movement
        # ==================================================

        self.movement.stop()

        # ==================================================
        # Clear screen
        # ==================================================

        if not self.clear_client.wait_for_service(
            timeout_sec=1.0
        ):

            self.get_logger().warning(
                'Clear service is not available.'
            )

            return

        clear_request = Empty.Request()

        self.clear_client.call_async(
            clear_request
        )

        # ==================================================
        # Kill current turtle
        # ==================================================

        if not self.kill_client.wait_for_service(
            timeout_sec=1.0
        ):

            self.get_logger().warning(
                'Kill service is not available.'
            )

            return

        kill_request = Kill.Request()

        kill_request.name = 'turtle1'

        kill_future = self.kill_client.call_async(
            kill_request
        )

        # ==================================================
        # Spawn after Kill
        # ==================================================

        def spawn_new_turtle(future):

            try:

                future.result()

            except Exception as e:

                self.get_logger().warning(
                    f'Kill failed: {e}'
                )

                return

            # ----------------------------------------------
            # Spawn new turtle
            # ----------------------------------------------

            if not self.spawn_client.wait_for_service(
                timeout_sec=1.0
            ):

                self.get_logger().warning(
                    'Spawn service is not available.'
                )

                return

            spawn_request = Spawn.Request()

            spawn_request.x = 5.54
            spawn_request.y = 5.54
            spawn_request.theta = 0.0
            spawn_request.name = 'turtle1'

            spawn_future = self.spawn_client.call_async(
                spawn_request
            )

            # ----------------------------------------------
            # Spawn complete
            # ----------------------------------------------

            def spawn_complete(spawn_future):

                try:

                    spawn_future.result()

                    self.x = 5.54
                    self.y = 5.54
                    self.theta = 0.0

                    self.save_log(
                        'RESET'
                    )

                except Exception as e:

                    self.get_logger().warning(
                        f'Spawn failed: {e}'
                    )

            spawn_future.add_done_callback(
                spawn_complete
            )

        kill_future.add_done_callback(
            spawn_new_turtle
        )
    


# ==========================================================
# Main
# ==========================================================

def main(args=None):

    rclpy.init(
        args=args
    )

    app = QApplication(
        sys.argv
    )

    controller = TurtleController()

    window = TurtleGUI(
        controller
    )

    window.show()

    exit_code = app.exec_()

    controller.destroy_node()

    rclpy.shutdown()

    sys.exit(
        exit_code
    )


if __name__ == '__main__':

    main()