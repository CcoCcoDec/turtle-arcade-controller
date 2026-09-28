import random

from turtlesim.srv import SetPen
from turtlesim.srv import Kill
from turtlesim.srv import Spawn

from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter
from rcl_interfaces.msg import ParameterValue
from rcl_interfaces.msg import ParameterType


class RandomFeatures:

    def __init__(self, node):

        self.node = node


    # ==================================================
    # Random Line Color
    # ==================================================

    def random_line_color(self):

        r = random.randint(50, 255)
        g = random.randint(50, 255)
        b = random.randint(50, 255)

        if not self.node.pen_client.wait_for_service(
            timeout_sec=1.0
        ):

            self.node.get_logger().warning(
                'SetPen service is not available.'
            )

            return

        request = SetPen.Request()

        request.r = r
        request.g = g
        request.b = b
        request.width = 3
        request.off = 0

        self.node.pen_client.call_async(
            request
        )

        self.node.save_log(
            'RANDOM_LINE_COLOR'
        )


    # ==================================================
    # Random Turtle
    # ==================================================

    def random_turtle(self):

        current_x = self.node.x
        current_y = self.node.y
        current_theta = self.node.theta

        # Stop current movement
        self.node.movement.stop()

        # Check Kill service
        if not self.node.kill_client.wait_for_service(
            timeout_sec=1.0
        ):

            self.node.get_logger().warning(
                'Kill service is not available.'
            )

            return

        # Check Spawn service
        if not self.node.spawn_client.wait_for_service(
            timeout_sec=1.0
        ):

            self.node.get_logger().warning(
                'Spawn service is not available.'
            )

            return

        # Delete current turtle
        kill_request = Kill.Request()

        kill_request.name = 'turtle1'

        kill_future = (
            self.node.kill_client.call_async(
                kill_request
            )
        )

        # Spawn new turtle
        def spawn_new_turtle(future):

            if future.result() is None:

                self.node.get_logger().warning(
                    'Failed to remove turtle1.'
                )

                return

            spawn_request = Spawn.Request()

            spawn_request.x = current_x
            spawn_request.y = current_y
            spawn_request.theta = current_theta
            spawn_request.name = 'turtle1'

            self.node.spawn_client.call_async(
                spawn_request
            )

            self.node.save_log(
                'RANDOM_TURTLE'
            )

        kill_future.add_done_callback(
            spawn_new_turtle
        )


    # ==================================================
    # Random Background
    # ==================================================

    def random_background_color(self):

        if not self.node.parameter_client.wait_for_service(
            timeout_sec=1.0
        ):

            self.node.get_logger().warning(
                'Turtlesim parameter service is not available.'
            )

            return

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        parameters = []

        for name, value in [
            ('background_r', r),
            ('background_g', g),
            ('background_b', b)
        ]:

            parameter = Parameter()

            parameter.name = name

            parameter.value = ParameterValue(
                type=ParameterType.PARAMETER_INTEGER,
                integer_value=value
            )

            parameters.append(
                parameter
            )

        request = SetParameters.Request()

        request.parameters = parameters

        self.node.parameter_client.call_async(
            request
        )

        self.node.save_log(
            'RANDOM_BACKGROUND'
        )