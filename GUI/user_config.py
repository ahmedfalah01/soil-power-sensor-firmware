"""
@brief GUI App code for user configurations

This module provides a PyQt5-based graphical user interface for configuring user settings.
It includes fields for Logger ID, Cell ID, WiFi SSID, WiFi Password, API Endpoint URL,
Voltage Slope, Voltage Offset, Current Slope, and Current Offset. The settings can be
saved by clicking the save button.

@file user_config.py
@author Ahmed Hassan Falah <ahmed.falah600@gmail.com>
@date 2024-06-10
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os
import sys
import base64
import serial
#library used to validate url input
import re

sys.path.append('/home/ahmedfalah/Github/soil-power-sensor-firmware/proto/python/src')
from soil_power_sensor_protobuf import encode_user_configuration, decode_user_configuration

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        """
        @brief Sets up the user interface components.

        This method initializes the main window, creates the layout, adds group boxes
        for different configuration sections, and sets up the Save button.
        
        @param MainWindow: The main window object.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Group boxes
        self.setupGroupBoxes()
        
        # Save Button
        self.setupSaveButton()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "User Configuration"))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setupGroupBoxes(self):
        """
        @brief Sets up the group boxes for different configuration sections.

        This method creates group boxes for Logger and Cell ID, WiFi configuration,
        and API and Calibration settings, and adds them to the main layout.
        """
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        # Logger and Cell ID group
        self.loggerCellGroupBox = QtWidgets.QGroupBox("Logger and Cell Configuration", self.centralwidget)
        self.loggerCellLayout = QtWidgets.QGridLayout(self.loggerCellGroupBox)

        self.Logger_ID = self.createLabel("Logger ID", font)
        self.lineEdit_Logger_ID = self.createLineEdit("Enter Logger ID (positive integer)")
        self.loggerCellLayout.addWidget(self.Logger_ID, 0, 0)
        self.loggerCellLayout.addWidget(self.lineEdit_Logger_ID, 0, 1)

        self.Cell_ID = self.createLabel("Cell ID", font)
        self.lineEdit_Cell_ID = self.createLineEdit("Enter Cell ID (positive integer)")
        self.loggerCellLayout.addWidget(self.Cell_ID, 1, 0)
        self.loggerCellLayout.addWidget(self.lineEdit_Cell_ID, 1, 1)

        self.layout.addWidget(self.loggerCellGroupBox)

        # WiFi configuration group
        self.wifiGroupBox = QtWidgets.QGroupBox("WiFi Configuration", self.centralwidget)
        self.wifiLayout = QtWidgets.QGridLayout(self.wifiGroupBox)

        self.WiFi_SSID = self.createLabel("WiFi SSID", font)
        self.lineEdit_WiFi_SSID = self.createLineEdit("Enter WiFi SSID")
        self.wifiLayout.addWidget(self.WiFi_SSID, 0, 0)
        self.wifiLayout.addWidget(self.lineEdit_WiFi_SSID, 0, 1)

        self.WiFi_Password = self.createLabel("WiFi Password", font)
        self.lineEdit_WiFi_Password = self.createLineEdit("Enter WiFi Password")
        self.lineEdit_WiFi_Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.wifiLayout.addWidget(self.WiFi_Password, 1, 0)
        self.wifiLayout.addWidget(self.lineEdit_WiFi_Password, 1, 1)

        self.layout.addWidget(self.wifiGroupBox)

        # API and Calibration group
        self.apiCalibrationGroupBox = QtWidgets.QGroupBox("API and Calibration", self.centralwidget)
        self.apiCalibrationLayout = QtWidgets.QGridLayout(self.apiCalibrationGroupBox)

        self.API_URL = self.createLabel("API Endpoint URL", font)
        self.lineEdit_API_URL = self.createLineEdit("Enter API URL (start with http:// or https://)")
        self.apiCalibrationLayout.addWidget(self.API_URL, 0, 0)
        self.apiCalibrationLayout.addWidget(self.lineEdit_API_URL, 0, 1)

        self.Voltage_Slope = self.createLabel("Voltage Slope", font)
        self.lineEdit_Voltage_Slope = self.createLineEdit("Enter Voltage Slope (floating-point)")
        self.apiCalibrationLayout.addWidget(self.Voltage_Slope, 1, 0)
        self.apiCalibrationLayout.addWidget(self.lineEdit_Voltage_Slope, 1, 1)

        self.Voltage_Offset = self.createLabel("Voltage Offset", font)
        self.lineEdit_Voltage_Offset = self.createLineEdit("Enter Voltage Offset (integer)")
        self.apiCalibrationLayout.addWidget(self.Voltage_Offset, 2, 0)
        self.apiCalibrationLayout.addWidget(self.lineEdit_Voltage_Offset, 2, 1)

        self.Current_Slope = self.createLabel("Current Slope", font)
        self.lineEdit_Current_Slope = self.createLineEdit("Enter Current Slope (floating-point)")
        self.apiCalibrationLayout.addWidget(self.Current_Slope, 3, 0)
        self.apiCalibrationLayout.addWidget(self.lineEdit_Current_Slope, 3, 1)

        self.Current_Offset = self.createLabel("Current Offset", font)
        self.lineEdit_Current_Offset = self.createLineEdit("Enter Current Offset (integer)")
        self.apiCalibrationLayout.addWidget(self.Current_Offset, 4, 0)
        self.apiCalibrationLayout.addWidget(self.lineEdit_Current_Offset, 4, 1)

        self.layout.addWidget(self.apiCalibrationGroupBox)

    def setupSaveButton(self):
        """
        @brief Sets up the Save button.

        This method creates the Save button, connects its click event to the
        saveConfigurations method, and adds it to the main layout.
        """
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.SaveBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.SaveBox.setFont(font)
        self.SaveBox.setOrientation(QtCore.Qt.Horizontal)
        self.SaveBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save)
        self.SaveBox.setCenterButtons(True)
        self.SaveBox.setObjectName("SaveBox")
        self.layout.addWidget(self.SaveBox)
        self.SaveBox.accepted.connect(self.saveConfigurations)

    def createLabel(self, text, font):
        """
        @brief Creates a QLabel with the given text and font.

        @param text: The text of the label.
        @param font: The font of the label.

        @return: The created QLabel object.
        """
        label = QtWidgets.QLabel(self.centralwidget)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignLeft)
        label.setObjectName(text.replace(" ", "_"))
        label.setText(text)
        return label

    def createLineEdit(self, placeholder=""):
        """
        @brief Creates a QLineEdit with the given placeholder text.

        @param placeholder: The placeholder text for the line edit.

        @return: The created QLineEdit object.
        """
        lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        lineEdit.setObjectName(f"lineEdit_{placeholder.replace(' ', '_')}")
        lineEdit.setPlaceholderText(placeholder)
        return lineEdit

    def saveConfigurations(self):
        """
        @brief Saves the user configurations to a JSON file.

        This method collects the user input from the line edits, validates the input,
        encodes the configurations using the encode function, and saves the encoded
        configurations to a JSON file named 'config.json'. It displays a message box
        to indicate success or failure.
        """
        config_data = {
            "Logger_ID": self.lineEdit_Logger_ID.text(),
            "Cell_ID": self.lineEdit_Cell_ID.text(),
            "WiFi_SSID": self.lineEdit_WiFi_SSID.text(),
            "WiFi_Password": self.lineEdit_WiFi_Password.text(),
            "API_URL": self.lineEdit_API_URL.text(),
            "Voltage_Slope": self.lineEdit_Voltage_Slope.text(),
            "Voltage_Offset": self.lineEdit_Voltage_Offset.text(),
            "Current_Slope": self.lineEdit_Current_Slope.text(),
            "Current_Offset": self.lineEdit_Current_Offset.text()
        }

        if not self.validateInput(config_data):
            return

        encoded_data = encode_user_configuration(
            int(config_data["Cell_ID"]),
            int(config_data["Logger_ID"]),
            config_data["WiFi_SSID"],
            config_data["WiFi_Password"],
            config_data["API_URL"],
            float(config_data["Voltage_Slope"]),
            int(config_data["Voltage_Offset"]),
            float(config_data["Current_Slope"]),
            int(config_data["Current_Offset"])
        )
        print(encoded_data)
        encoded_data_base64 = base64.b64encode(encoded_data).decode('utf-8')
        json_data = {
            "encoded_data": encoded_data_base64
        }

        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'w') as f:
                json.dump(json_data, f, indent=4)

            QtWidgets.QMessageBox.information(self.centralwidget, "Success", "Configurations saved successfully.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.centralwidget, "Error", f"Failed to save configurations: {e}")

    def validateInput(self, config_data):
        """
        @brief Validates the user input for each configuration field.

        This method checks if each field has valid input according to the specified
        constraints. It returns True if all inputs are valid, otherwise False.
        
        @param config_data: A dictionary containing the user configuration data.

        @return: True if all inputs are valid, otherwise False.
        """
        if not config_data["Logger_ID"].isdigit():
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "Logger ID must be a positive integer.")
            return False
        if not config_data["Cell_ID"].isdigit():
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "Cell ID must be a positive integer.")
            return False
        if not config_data["WiFi_SSID"]:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "WiFi SSID cannot be empty.")
            return False
        if not config_data["WiFi_Password"]:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "WiFi Password cannot be empty.")
            return False
        if not re.match(r'^https?://', config_data["API_URL"]):
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "API Endpoint URL must be a valid URL starting with http:// or https://.")
            return False
        try:
            float(config_data["Voltage_Slope"])
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "Voltage Slope must be a floating-point number.")
            return False
        if not config_data["Voltage_Offset"].isdigit():
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "Voltage Offset must be an integer.")
            return False
        try:
            float(config_data["Current_Slope"])
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "Current Slope must be a floating-point number.")
            return False
        if not config_data["Current_Offset"].isdigit():
            QtWidgets.QMessageBox.warning(None, "Invalid Input", "Current Offset must be an integer.")
            return False
        return True

def print_bytes_c(data : bytes) -> str:
    """Formats serialized data into c bytes array"""

    # format data string
    data_str = "uint8_t data[] = {"
    hex_str = [hex(d) for d in data]
    data_str += ", ".join(hex_str) 
    data_str += "};"

    # print data string
    print(data_str)
    
    # print length of data string
    print(f'size_t data_len = {len(hex_str)};')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
