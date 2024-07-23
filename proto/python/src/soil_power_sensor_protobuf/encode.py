"""Module to encode soil power sensor protobuf messages

Encoding a response can be performed with

    encode_response()

Each type of measurement has a corresponding encoding function as follows:

    PowerMeasurement -> encode_power_measurement()
    Teros12Measurement -> encode_teros12_measurement()
"""

from .soil_power_sensor_pb2 import Measurement, Response, UserConfiguration


def encode_response(success: bool = True) -> bytes:
    """Encodes a Response message

    The response indicates there was a successful upload, otherwise indicates an
    error.

    Args:
        success: Specifies whether to encode a success or failure.

    Returns:
        Byte string of response message.
    """

    # format response
    response = Response()
    if success:
        response.resp = Response.ResponseType.SUCCESS
    else:
        response.resp = Response.ResponseType.ERROR

    # return encode message
    return response.SerializeToString()


def encode_power_measurement(
    ts: int, cell_id: int, logger_id: int, voltage: float, current: float
) -> bytes:
    """Encodes a PowerMeasurement within the Measurement message

    Args:
        ts: Timestamp in unix epochs
        cell_id: Cell Id from Dirtviz
        logger_id: Logger Id from Dirtviz
        voltage: Voltage in V (Volts)
        current: Current in A (Amps)

    Returns:
        Serialized Power measurement
    """

    meas = Measurement()

    # metadata
    meas.meta.ts = ts
    meas.meta.cell_id = cell_id
    meas.meta.logger_id = logger_id

    # power
    meas.power.voltage = voltage
    meas.power.current = current

    return meas.SerializeToString()


def encode_teros12_measurement(
    ts: int,
    cell_id: int,
    logger_id: int,
    vwc_raw: float,
    vwc_adj: float,
    temp: float,
    ec: int,
) -> bytes:
    """Encodes a Teros12Measurment within the Measurement message

    Args:
        ts: Timestamp in unix epochs
        cell_id: Cell Id from Dirtviz
        logger_id: Logger Id from Dirtviz
        vwc_raw: Raw volumetric water content from Teros12
        vwc_adj: Volumetric water content from Teros12 with calibration applied
        temp: Temperature in C
        ec: Electrical conductivity

    Returns:
        Serialized Teros12 measurement
    """

    meas = Measurement()

    # metadata
    meas.meta.ts = ts
    meas.meta.cell_id = cell_id
    meas.meta.logger_id = logger_id

    # teros12
    meas.teros12.vwc_raw = vwc_raw
    meas.teros12.vwc_adj = vwc_adj
    meas.teros12.temp = temp
    meas.teros12.ec = ec

    return meas.SerializeToString()


def encode_phytos31_measurement(
    ts: int, cell_id: int, logger_id: int, voltage: float, leaf_wetness: float
) -> bytes:
    """Encodes a Phytos31Measurement within the Measurement message

    Args:
        ts: Timestamp in unix epochs
        cell_id: Cell Id from Dirtviz
        logger_id: Logger Id from Dirtviz
        voltage: Raw voltage reading
        leaf_wetness: Calibrated leaf wetness

    Returns:
        Serialized Phytos31 measurement
    """

    meas = Measurement()

    # metadata
    meas.meta.ts = ts
    meas.meta.cell_id = cell_id
    meas.meta.logger_id = logger_id

    # phytos31
    meas.phytos31.voltage = voltage
    meas.phytos31.leaf_wetness = leaf_wetness

    return meas.SerializeToString()


def encode_user_configuration(
    cell_id: int,
    logger_id: int,
    WiFi_SSID: str,
    WiFi_Password: str,
    API_URL: str,
    Voltage_Slope: float,
    Voltage_Offset: int,
    Current_Slope: float,
    Current_Offset: int
) -> bytes:
    """Encodes a UserConfiguration message

    Args:
        cell_id: ID of the cell.
        logger_id: ID of the logger.
        WiFi_SSID: WiFi SSID.
        WiFi_Password: WiFi password.
        API_URL: API endpoint URL.
        Voltage_Slope: Calibration slope for voltage.
        Voltage_Offset: Calibration offset for voltage.
        Current_Slope: Calibration slope for current.
        Current_Offset: Calibration offset for current.

    Returns:
        Serialized UserConfiguration message
    """

    user_config = UserConfiguration()

    user_config.cell_id = cell_id
    user_config.logger_id = logger_id
    user_config.WiFi_SSID = WiFi_SSID
    user_config.WiFi_Password = WiFi_Password
    user_config.API_URL = API_URL
    user_config.Voltage_Slope = Voltage_Slope
    user_config.Voltage_Offset = Voltage_Offset
    user_config.Current_Slope = Current_Slope
    user_config.Current_Offset = Current_Offset

    return user_config.SerializeToString()