# Turtle Arcade Controller

## Features

- Turtle movement control
  - Forward
  - Backward
  - Rotate left 45°
  - Rotate right 45°
  - Stop

- Turtle reset
  - Stop current movement
  - Clear drawing
  - Remove existing turtle
  - Spawn new turtle at the default position

- Random features
  - Random line color
  - Random turtle
  - Random background color

- Real-time status display
  - X position
  - Y position
  - Direction

- Action logging
  - Store movement and feature actions in MySQL
  - View log history through GUI


## Technology Stack

- Python
- ROS2
- PyQt5
- MySQL
- turtlesim
- Ubuntu / WSL


## Project Structure

```text
turtle_controller/
│
├── README.md
├── package.xml
├── setup.py
│
└── turtle_controller/
    ├── __init__.py
    ├── turtle_controller.py
    ├── movement.py
    ├── random_features.py
    ├── gui.py
    └── db.py
```

# System Architecture

                    ┌─────────────────────┐
                    │      PyQt5 GUI      │
                    │                     │
                    │  Direction Control  │
                    │  Random Features    │
                    │  Log History        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  TurtleController   │
                    │                     │
                    │  ROS2 Node Manager  │
                    └──────┬───────┬──────┘
                           │       │
                ┌──────────┘       └──────────┐
                ▼                             ▼
       ┌─────────────────┐           ┌─────────────────┐
       │ MovementControl │           │ RandomFeatures  │
       │                 │           │                 │
       │ Forward         │           │ Line Color      │
       │ Backward        │           │ Random Turtle   │
       │ Left / Right    │           │ Background     │
       │ Stop            │           │                 │
       └────────┬────────┘           └────────┬────────┘
                │                             │
                └──────────────┬──────────────┘
                               ▼
                       ┌────────────────┐
                       │    Turtlesim   │
                       └────────────────┘

                               │
                               ▼
                       ┌────────────────┐
                       │     MySQL      │
                       │   turtle_log   │
                       └────────────────┘

# ROS2 Communication
## Publisher
/turtle1/cmd_vel

Message:

geometry_msgs/msg/Twist

Used for turtle movement and rotation.

## Subscriber
/turtle1/pose

Message:

turtlesim/msg/Pose

Used to receive the turtle's current position and direction.

## Services
/turtle1/set_pen
/kill
/spawn
/clear
/turtlesim/set_parameters

Used for line color, turtle reset, turtle creation, screen clearing,
and background color changes.

# Database

## Database:

turtle_db

## Table:

turtle_log

## Structure:

Column  Type  Description
id  INT Log ID
x FLOAT Turtle X position
y FLOAT Turtle Y position
theta FLOAT Turtle direction
action  VARCHAR(50) Performed action
created_at  DATETIME  Log creation time


# How to Run
## 1. Build
cd ~/ws

colcon build --packages-select turtle_controller

source install/setup.bash

## 2. Start Turtlesim

Open Terminal 1:

ros2 run turtlesim turtlesim_node

## 3. Start Turtle Controller

Open Terminal 2:

cd ~/ws

source install/setup.bash

ros2 run turtle_controller turtle_controller


# GUI

The application provides:

Direction control
Stop
Reset
Random line color
Random turtle
Random background
Real-time turtle position
Log history
What I Learned