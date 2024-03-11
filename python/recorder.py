#!/usr/bin/env python

"""Data recorder for Soil Power Sensor

The recorder controls the SPS firmware and a Keithley 2400 Source
Measurement Unit (SMU). Ideally the script should work with any microcontrollre
flashed with the firmware and any source measurement unit that supports
Standard Commands for Programable Instruments (SCPI). The units listed are the
ones that the script was developed and tested on. It allows to step through
a range of output voltages on the Keithley and measure the voltage and current
from both the SMU and the Soil Power Sensor (SPS).

Example
-------
The following examples shows how to collect data on voltage ranges 0-3.3V
increasing the voltage by 0.1V every step. The SPS is connected to
``/dev/ttyACM0`` and the SMu is connected to ``/dev/ttyUSB0``.::

    $ python recorder.py 0 3.3 0.1 /dev/ttyACM0 /dev/ttyACM0

To see a list of all CLI parameters:::

    $ python recorder.py -h
"""

import pdb

import time
import argparse
import serial
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import Tuple
from soil_power_sensor_protobuf import encode, decode


class SerialController:
    """Generic serial controller that will open and close serial connections"""

    # Serial port
    ser = None

    def __init__(self, port):
        """Constructor

        Initialises connection to serial port.

        Parameters
        ----------
        port : str
            Serial port of device
        """

        self.ser = serial.Serial(port, timeout=1)

    def __del__(self):
        """Destructor

        Closes connection to serial port.
        """

        self.ser.close()


class SoilPowerSensorController(SerialController):
    """Controller used to read values from the SPS"""

    def __init__(self, port):
        """Constructor

        Opens serial connection and checks functionality

        Parameters
        ----------
        port : str
            Serial port of device
        """
        super().__init__(port)
        self.check()

    def get_power(self) -> Tuple[float, float]:
        """Measure voltage from SPS

        Returns
        -------
        tuple[float, float]
            voltage, current
        """
        self.ser.write(b"0\n") # send a command to the SPS to send a power measurment
        reply = self.ser.readline() # read said measurment
        reply = reply.decode() # turn it into a regular python string and strip it
        reply = reply.strip("\r\n")

        meas_dict = decode(reply) # decode using protobuf
        voltage_value = meas_dict["data"]["voltage"]
        current_value = meas_dict["data"]["current"]

        return float(voltage_value), float(current_value)

    def check(self):
        """Performs a check of the connection to the board

        Raises
        ------
        RuntimeError
            Checks that SPS replies "ok" when sent "check"
        """
        self.ser.write(b"check\n")
        reply = self.ser.readline()
        reply = reply.decode()
        reply = reply.strip("\r\n")
        if (reply != "ok"):
            raise RuntimeError("SPS check failed")


class SMUController(SerialController):
    """Controller for the Keithley 2400 SMU used to supply known voltage to the
    SPS

    Uses SCPI (Standard Control of Programmable Instruments) to control the SMU
    through its RS232 port. Written for the Keithley 2400 SMU, but should work
    for any other SMU that uses SCPI.
    """

    class VoltageIterator:
        """VoltageIterator Class

        Implements a iterator for looping through voltage output values
        """

        def __init__(self, ser, start, stop, step):
            """Constructor

            Parameters
            ----------
            ser : serial.Serial
                Initialised serial connection
            start : float
                Starting voltage
            stop : float
                End voltage
            step : float
                Voltage step
            """

            self.ser = ser
            self.start = start
            self.stop = stop
            self.step = step


        def __iter__(self):
            """Iterator

            Sets current value to start
            """

            self.v = None
            self.ser.write(b':OUTP ON\n')
            return self


        def __next__(self):
            """Next

            Steps to next voltage level, stopping once stop is reached

            Raises
            ------
            StopIteration
                When the next step exceeds the stop level
            """

            if self.v is None:
                return self.set_voltage(self.start)

            v_next = self.v + self.step

            if (v_next <= self.stop):
                return self.set_voltage(v_next)
            else:
                raise StopIteration


        def set_voltage(self, v):
            """Sets the voltage output"""

            self.v = v
            cmd = f":SOUR:VOLT:LEV {v}\n"
            self.ser.write(bytes(cmd, 'ascii'))
            return self.v


    def __init__(self, port):
        """Constructor

        Opens serial port, restore to known defaults

        Parameters
        ----------
        port : str
            Serial port of device
        """

        super().__init__(port)
        # Reset settings
        self.ser.write(b'*RST\n')
        # Voltage source
        self.ser.write(b':SOUR:FUNC VOLT\n')
        self.ser.write(b':SOUR:VOLT:MODE FIXED\n')
        # 1mA compliance
        self.ser.write(b':SENS:CURR:PROT 10e-3\n')
        # Sensing functions
        self.ser.write(b':SENS:CURR:RANGE:AUTO ON\n')
        self.ser.write(b':SENS:FUNC:OFF:ALL\n')
        self.ser.write(b':SENS:FUNC:ON "VOLT"\n')
        self.ser.write(b':SENS:FUNC:ON "CURR"\n')


    def __del__(self):
        """Destructor

        Turns off output
        """

        self.ser.write(b':OUTP OFF\n')


    def vrange(self, start, stop, step) -> VoltageIterator:
        """Gets iterator to range of voltages

        Parameters
        ----------
        start : float
            Starting voltage
        stop : float
            End voltage
        step : float
            Voltage step
        """

        return self.VoltageIterator(self.ser, start, stop, step)


    def get_voltage(self) -> float:
        """Measure voltage supplied to the SPS from SMU

        Returns
        -------
        float
            Measured voltage
        """

        self.ser.write(b':FORM:ELEM VOLT\n')
        self.ser.write(b':READ?\n')
        reply = self.ser.readline().decode()
        reply = reply.strip("\r")
        return float(reply)


    def get_current(self) -> float:
        """Measure current supplied to the SPS from SMU

        Returns
        -------
        float
            Measured current
        """

        self.ser.write(b':FORM:ELEM CURR\n') # replace with serial.write with socket.write commands, std library aviable, lots of example code
        self.ser.write(b':READ?\n')
        reply = self.ser.readline().decode()
        reply = reply.strip("\r")
        return float(reply)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Automated data recorder
        for Soil Power Sensor board using serial to control Keithley 2400 SMU""")

    parser.add_argument(
        "--samples",
        type=int,
        default=10,
        help="Number of samples to takeat each voltage level"
    )

    parser.add_argument("start", type=float, help="Start voltage in V")
    parser.add_argument("stop", type=float, help="End voltage in V")
    parser.add_argument("step", type=float, help="Step between voltages in V")
    parser.add_argument("smu_port", type=str, help="SMU serial port")
    parser.add_argument("sps_port", type=str, help="SPS serial port")
    parser.add_argument("data_file", type=str, help="Path to store data file")

    args = parser.parse_args()


    sps = SoilPowerSensorController(args.sps_port) 
    smu = SMUController(args.smu_port)

    data = {
        "V": [],
        "V_in": [],
        "I_in": [],
        "V_i": [],
        "V_2x": [],
    }

    for v in tqdm(smu.vrange(args.start, args.stop, args.step)):
        for _ in range(args.samples):
            data["V"].append(v)

            measured_voltage, measured_current = sps.get_power()

            # get smu values
            data["V_in"].append(smu.get_voltage())
            data["I_in"].append(smu.get_current())

            # get sps  values
            data["V_2x"].append(measured_voltage)
            data["V_i"].append(measured_current)

    data_df = pd.DataFrame(data)
    print(data_df)
    data_df.to_csv(args.data_file, index=False)
