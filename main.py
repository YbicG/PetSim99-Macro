"""
Made by YbicG (@ybicg)
©️ 2024 All Rights Reserved. Unauthorized redistribution or modification of this program is illegal and can have legal consequences.
"""
import sys
import os
import configparser
import macro
import threading
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton, QStackedWidget
from QSwitchControl import SwitchControl

config = configparser.ConfigParser()
config.optionxform = str 
config.read('config.ini')

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Clan Macro")
        self.setStyleSheet("""
        QWidget {
            background-color: #222222;
            color: #ffffff;
            font-size: 16px;
            font-family: Arial;
        }
        QLabel {
            margin-right: 10px;
        }
        QPushButton {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 3px 10px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #555555;
        }
        QPushButton:pressed {
            background-color: #777777;
        }
        """)

        self.stacked_widget = QStackedWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

        enabled_disabled_layout = QVBoxLayout()
        for section in config.sections():
            if section.startswith("Enabled/Disabled"):
                for option, value in config.items(section):
                    switch = SwitchControl(bg_color="#777777", circle_color="#DDD", active_color="#aa00ff", animation_duration=300, checked=config.getboolean(section, option, fallback=False), change_cursor=True)
                    label = QLabel(option.replace("_", " ").title().replace("Iv", "IV").replace("Xp", "XP"))
                    hbox = QHBoxLayout()
                    hbox.addWidget(label)
                    hbox.addStretch(1)
                    hbox.addWidget(switch)
                    enabled_disabled_layout.addLayout(hbox)
                    switch.stateChanged.connect(lambda state, sec=section, opt=option: self.on_switch_changed(sec, opt, state))
                break

        other_layout = QVBoxLayout()
        for section in config.sections():
            if not section.startswith("Enabled/Disabled"):
                group_label = QLabel(section.replace("_", " ").title().replace("Iv", "IV").replace("Xp", "XP"))
                group_label.setStyleSheet("font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
                other_layout.addWidget(group_label)

                for option, value in config.items(section):
                    label = QLabel(option.replace("_", " ").title().replace("Iv", "IV").replace("Xp", "XP"))
                    edit_line = QLineEdit(value)
                    edit_line.setPlaceholderText("Enter value...")
                    edit_line.setStyleSheet("background-color: #333333; color: #ffffff; border: 1px solid #555555; padding: 3px;")
                    edit_line.textChanged.connect(lambda text, sec=section, opt=option: self.on_value_changed(sec, opt, text))
                    
                    hbox = QHBoxLayout()
                    hbox.addWidget(label)
                    hbox.addWidget(edit_line)
                    other_layout.addLayout(hbox)

        enabled_disabled_widget = QWidget()
        enabled_disabled_widget.setLayout(enabled_disabled_layout)
        self.stacked_widget.addWidget(enabled_disabled_widget)

        other_widget = QWidget()
        other_widget.setLayout(other_layout)
        self.stacked_widget.addWidget(other_widget)

        self.current_page_index = 0

        self.prev_button = QPushButton("< Prev")
        self.prev_button.clicked.connect(self.show_previous_page)
        self.next_button = QPushButton("Next >")
        self.next_button.clicked.connect(self.show_next_page)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.next_button)
        
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("""
        QPushButton {
            background-color: #4CAF50;  /* Green */
            color: #ffffff;
            border: 1px solid #555555;
            padding: 3px 10px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #66BB6A;  /* Lighter green on hover */
        }
        QPushButton:pressed {
            background-color: #388E3C;  /* Darker green when pressed */
        }
        QPushButton:disabled {
                background-color: #888888;  /* Grayed out */
        }
        """)

        self.stop_button = QPushButton  ("Stop")  
        self.stop_button.setStyleSheet("""
        QPushButton {
            background-color: #f44336;  /* Red */
            color: #ffffff;
            border: 1px solid #555555;
            padding: 3px 10px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #EF5350;  /* Lighter red on hover */
        }
        QPushButton:pressed {
            background-color: #D32F2F;  /* Darker red when pressed */
        }
        QPushButton:disabled {
                background-color: #888888;  /* Grayed out */
        }
        """)


        self.start_button.clicked.connect(self.on_start_clicked)
        self.stop_button.clicked.connect(self.on_stop_clicked)

        self.enable_start_stop_buttons(True)
        
        button_layout_below = QHBoxLayout()
        button_layout_below.addWidget(self.start_button)
        button_layout_below.addWidget(self.stop_button)

        self.layout.addLayout(button_layout_below)
        self.layout.addLayout(button_layout)

        self.show()

    def show_previous_page(self):
        self.current_page_index = (self.current_page_index - 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(self.current_page_index)

    def show_next_page(self):
        self.current_page_index = (self.current_page_index + 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(self.current_page_index)

    def on_switch_changed(self, section, option, state):
        state = True if state == 2 else False
        config.set(section, option, str(state))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
    def on_value_changed(self, section, option, value):
        config.set(section, option, value)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
    def enable_start_stop_buttons(self, enabled):
        self.start_button.setEnabled(enabled)
        self.stop_button.setEnabled(not enabled)
        
        config.set("Developer (Do Not Modify)", "MACRO_ENABLED", str(not enabled))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
    def on_start_clicked(self):
        self.enable_start_stop_buttons(False)

    def on_stop_clicked(self):
        self.enable_start_stop_buttons(True)

macro_thread = threading.Thread(target=macro.main, name="Macro Thread")

macro_thread.start()


app = QApplication(sys.argv)
icon = QIcon(os.path.join(os.path.dirname(__file__), "ui", "clanlogo.ico"))
app.setWindowIcon(icon)
form = Form()
sys.exit(app.exec_())