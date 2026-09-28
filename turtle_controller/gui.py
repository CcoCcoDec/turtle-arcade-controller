import math

import rclpy

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from PyQt5.QtCore import QTimer, Qt


class TurtleGUI(QWidget):

    def __init__(self, controller):

        super().__init__()

        self.controller = controller

        self.setWindowTitle(
            'TURTLE ARCADE CONTROLLER'
        )

        self.resize(
            420,
            620
        )

        self.create_ui()

        # ==================================================
        # GUI update timer
        # ==================================================

        self.gui_timer = QTimer()

        self.gui_timer.timeout.connect(
            self.update_gui
        )

        self.gui_timer.start(
            100
        )


    # ======================================================
    # UI
    # ======================================================

    def create_ui(self):

        # ==================================================
        # Main window style
        # ==================================================

        self.setStyleSheet("""
            QWidget {
                background-color: #151515;
                color: #F5F5F5;
                font-family: Arial;
            }

            QLabel#title {
                color: #FFD93D;
                font-size: 26px;
                font-weight: bold;
                padding: 8px;
            }

            QLabel#status {
                background-color: #050505;
                color: #39FF14;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 14px;
                font-family: Consolas;
                font-size: 16px;
            }

            QPushButton {
                border: 2px solid #444444;
                border-radius: 12px;
                background-color: #292929;
                color: white;
                font-size: 17px;
                font-weight: bold;
                padding: 12px;
            }

            QPushButton:hover {
                background-color: #3A3A3A;
                border: 2px solid #777777;
            }

            QPushButton:pressed {
                background-color: #111111;
            }

            QPushButton#direction {
                background-color: #333333;
                border: 3px solid #666666;
                font-size: 30px;
                min-width: 80px;
                min-height: 65px;
            }

            QPushButton#direction:hover {
                background-color: #454545;
                border: 3px solid #FFD93D;
            }

            QPushButton#stop {
                background-color: #B91C1C;
                border: 3px solid #EF4444;
                font-size: 18px;
                min-width: 80px;
                min-height: 65px;
            }

            QPushButton#stop:hover {
                background-color: #DC2626;
            }

            QPushButton#reset {
                background-color: #1D4ED8;
                border: 2px solid #3B82F6;
            }

            QPushButton#reset:hover {
                background-color: #2563EB;
            }

            QPushButton#function {
                background-color: #242424;
                border: 2px solid #555555;
            }

            QPushButton#function:hover {
                background-color: #333333;
                border: 2px solid #FFD93D;
            }

            QFrame#panel {
                background-color: #202020;
                border: 2px solid #383838;
                border-radius: 15px;
                padding: 10px;
            }
        """)

        # ==================================================
        # Main layout
        # ==================================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            20,
            15,
            20,
            20
        )

        main_layout.setSpacing(
            12
        )

        # ==================================================
        # Title
        # ==================================================

        title = QLabel(
            'TURTLE ARCADE'
        )

        title.setObjectName(
            'title'
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(
            title
        )

        # ==================================================
        # Status
        # ==================================================

        self.position_label = QLabel(
            'X : 5.54\n'
            'Y : 5.54\n'
            'Direction : 0.00 deg'
        )

        self.position_label.setObjectName(
            'status'
        )

        self.position_label.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(
            self.position_label
        )

        # ==================================================
        # Control panel
        # ==================================================

        control_panel = QFrame()

        control_panel.setObjectName(
            'panel'
        )

        control_layout = QGridLayout()

        control_layout.setSpacing(
            10
        )

        # --------------------------------------------------
        # UP
        # --------------------------------------------------

        self.up_button = QPushButton(
            '↑'
        )

        self.up_button.setObjectName(
            'direction'
        )

        self.up_button.clicked.connect(
            self.controller.movement.move_forward
        )

        # --------------------------------------------------
        # LEFT
        # --------------------------------------------------

        self.left_button = QPushButton(
            '←'
        )

        self.left_button.setObjectName(
            'direction'
        )

        self.left_button.clicked.connect(
            self.controller.movement.rotate_left
        )

        # --------------------------------------------------
        # STOP
        # --------------------------------------------------

        self.stop_button = QPushButton(
            'STOP'
        )

        self.stop_button.setObjectName(
            'stop'
        )

        self.stop_button.clicked.connect(
            self.controller.movement.stop
        )

        # --------------------------------------------------
        # RIGHT
        # --------------------------------------------------

        self.right_button = QPushButton(
            '→'
        )

        self.right_button.setObjectName(
            'direction'
        )

        self.right_button.clicked.connect(
            self.controller.movement.rotate_right
        )

        # --------------------------------------------------
        # DOWN
        # --------------------------------------------------

        self.down_button = QPushButton(
            '↓'
        )

        self.down_button.setObjectName(
            'direction'
        )

        self.down_button.clicked.connect(
            self.controller.movement.move_backward
        )

        # --------------------------------------------------
        # Arrange buttons
        # --------------------------------------------------

        control_layout.addWidget(
            self.up_button,
            0,
            1
        )

        control_layout.addWidget(
            self.left_button,
            1,
            0
        )

        control_layout.addWidget(
            self.stop_button,
            1,
            1
        )

        control_layout.addWidget(
            self.right_button,
            1,
            2
        )

        control_layout.addWidget(
            self.down_button,
            2,
            1
        )

        control_panel.setLayout(
            control_layout
        )

        main_layout.addWidget(
            control_panel
        )

        # ==================================================
        # Reset
        # ==================================================

        self.reset_button = QPushButton(
            'RESET'
        )

        self.log_button = QPushButton(
            'LOG HISTORY'
        )

        self.log_button.setObjectName(
            'function'
        )

        self.log_button.clicked.connect(
            self.show_log_history
        )

        main_layout.addWidget(
            self.log_button
        )

        self.reset_button.setObjectName(
            'reset'
        )

        self.reset_button.clicked.connect(
            self.controller.reset
        )

        main_layout.addWidget(
            self.reset_button
        )

        # ==================================================
        # Random functions
        # ==================================================

        function_layout = QHBoxLayout()

        function_layout.setSpacing(
            10
        )

        self.line_color_button = QPushButton(
            'RANDOM LINE COLOR'
        )

        self.line_color_button.setObjectName(
            'function'
        )

        self.line_color_button.clicked.connect(
            self.controller.random_features.random_line_color
        )

        self.turtle_button = QPushButton(
            'RANDOM TURTLE'
        )

        self.turtle_button.setObjectName(
            'function'
        )

        self.turtle_button.clicked.connect(
            self.controller.random_features.random_turtle
        )

        self.background_button = QPushButton(
            'BACKGROUND'
        )

        self.background_button.setObjectName(
            'function'
        )

        self.background_button.clicked.connect(
            self.controller.random_features.random_background_color
        )

        function_layout.addWidget(
            self.line_color_button
        )

        function_layout.addWidget(
            self.turtle_button
        )

        function_layout.addWidget(
            self.background_button
        )

        main_layout.addLayout(
            function_layout
        )

        self.setLayout(
            main_layout
        )


    # ======================================================
    # Update GUI
    # ======================================================

    def update_gui(self):

        rclpy.spin_once(
            self.controller,
            timeout_sec=0
        )

        degree = math.degrees(
            self.controller.theta
        )

        self.position_label.setText(
            f'X : {self.controller.x:.2f}\n'
            f'Y : {self.controller.y:.2f}\n'
            f'Direction : {degree:.2f} deg'
        )

    # ======================================================
    # Log History
    # ======================================================

    def show_log_history(self):

        logs = self.controller.db.get_logs()

        self.log_window = QWidget()

        self.log_window.setWindowTitle(
            'TURTLE LOG HISTORY'
        )

        self.log_window.resize(
            850,
            500
        )

        layout = QVBoxLayout()

        table = QTableWidget()

        table.setColumnCount(
            6
        )

        table.setHorizontalHeaderLabels([
            'ID',
            'X',
            'Y',
            'Theta',
            'Action',
            'Created At'
        ])

        table.setRowCount(
            len(logs)
        )

        # --------------------------------------------------
        # Insert data
        # --------------------------------------------------

        for row, log in enumerate(logs):

            for column, value in enumerate(log):

                item = QTableWidgetItem(
                    str(value)
                )

                table.setItem(
                    row,
                    column,
                    item
                )

        # --------------------------------------------------
        # Table settings
        # --------------------------------------------------

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        layout.addWidget(
            table
        )

        self.log_window.setLayout(
            layout
        )

        self.log_window.show()