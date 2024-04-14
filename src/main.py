"""
Made by YbicG (@ybicg)
©️ 2024 All Rights Reserved. Unauthorized redistribution or modification of this program is illegal and can have legal consequences.
"""
import hashlib
import sys
import os
import requests
import configparser
import functions.macro as macro
import keyboard
import atexit
import threading
import config as cfg
import functions.log_handler as log_handler; print = log_handler.init()
from config import AutoConfig
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton, QStackedWidget, QMessageBox, QDialog
from QSwitchControl import SwitchControl

config = configparser.ConfigParser()
config.optionxform = str 
config.read('config.ini')

Config = AutoConfig(cfg.config_path)
    
Config.SYSTEM_RUNNING = True
    
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
                border: 2px solid #555555;
                border-radius: 5px;
                padding: 8px 16px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
                border-color: #777777;
            }
            QPushButton:pressed {
                background-color: #777777;
                border-color: #999999;
            }
            QLineEdit {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
            QStackedWidget {
                background-color: #1e1e1e;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
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
            if not section.startswith("Enabled/Disabled") and not section.startswith("Spawn Delays (in Seconds)"):
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
        
        delays_layout = QVBoxLayout()
        for section in config.sections():
            if section.startswith("Spawn Delays (in Seconds)"):
                group_label = QLabel(section.replace("_", " ").title().replace("Iv", "IV").replace("Xp", "XP"))
                group_label.setStyleSheet("font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
                delays_layout.addWidget(group_label)
                
                for option, value in config.items(section):
                    label = QLabel(option.replace("_", " ").title().replace("Iv", "IV").replace("Xp", "XP"))
                    edit_line = QLineEdit(value)
                    edit_line.setPlaceholderText("Enter value...")
                    edit_line.setStyleSheet("background-color: #333333; color: #ffffff; border: 1px solid #555555; padding: 3px;")
                    edit_line.textChanged.connect(lambda text, sec=section, opt=option: self.on_value_changed(sec, opt, text))
                    
                    hbox = QHBoxLayout()
                    hbox.addWidget(label)
                    hbox.addWidget(edit_line)
                    delays_layout.addLayout(hbox)
                
                delays_layout.addStretch()

        enabled_disabled_widget = QWidget()
        enabled_disabled_widget.setLayout(enabled_disabled_layout)
        self.stacked_widget.addWidget(enabled_disabled_widget)

        other_widget = QWidget()
        other_widget.setLayout(other_layout)
        self.stacked_widget.addWidget(other_widget)
        
        delay_widget = QWidget()
        delay_widget.setLayout(delays_layout)
        self.stacked_widget.addWidget(delay_widget)

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
            padding: 5px 10px;
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
            padding: 5px 10px;
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
        self.raise_()

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
    
    def closeEvent(self, event):
        print("Shutting down systems...")
        Config.MACRO_ENABLED = False
        Config.SYSTEM_RUNNING = False
        keyboard.unhook_all()
        event.accept()
        os._exit(os.EX_OK)
class PasswordForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ricohash = requests.get("https://ybicg.com/macros/clan-quests/9300f7223a8ca140c7e8ccabd4f72fcd/8380e83f3856b368f2a909c357f1a3ef.txt").text.strip()

    def initUI(self):
        self.setWindowTitle("Enter Password")
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
                border: 2px solid #555555;
                border-radius: 5px;
                padding: 8px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
                border-color: #777777;
            }
            QPushButton:pressed {
                background-color: #777777;
                border-color: #999999;
            }
            QLineEdit {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.layout = QVBoxLayout()
        self.password_label = QLabel("Enter Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.check_password)

        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_edit)
        self.layout.addWidget(self.submit_button)
        self.setLayout(self.layout)

    def check_password(self):
        entered_password = self.password_edit.text()
        stored_password = self.ricohash
        encrypted_entered_password = hashlib.sha256(entered_password.encode()).hexdigest()

        if encrypted_entered_password == stored_password:
            main_form = Form()
            main_form.show()
            self.destroy()
        else:
            QMessageBox.warning(self, "Incorrect Password", "The entered password is incorrect.")

def onClose():
    print("Shutting down systems...")
    Config.MACRO_ENABLED = False
    Config.SYSTEM_RUNNING = False
    keyboard.unhook_all()

atexit.register(onClose)

macro_thread = threading.Thread(target=macro.main, name="Macro Thread")
macro_thread.daemon = True
macro_thread.start()
    
app = QApplication(sys.argv)
icon = QIcon(os.path.join(os.path.dirname(__file__), "lib", "clanlogo.ico"))
app.setWindowIcon(icon)

password_form = PasswordForm()
password_form.show()
password_form.raise_()

sys.exit(app.exec_())