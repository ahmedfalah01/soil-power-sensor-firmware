import base64
import json
import os
import sys

# Add the path to the protobuf generated Python code to the system path
sys.path.append('../proto/python/src')
from soil_power_sensor_protobuf import decode_user_configuration

def read_json_and_decode(file_path):
    """
    Reads a JSON file containing base64 encoded data, decodes the data,
    and then decodes the protobuf UserConfiguration message.

    Args:
        file_path (str): The path to the JSON file.

    Raises:
        Exception: If any error occurs during reading, decoding, or processing.
    """
    try:
        # Open and read the JSON file
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            # Get the base64 encoded data from the JSON
            encoded_data_base64 = json_data.get('encoded_data', None)
            print(json_data)  # Print the JSON data for debugging
            print("----------------------------------------")
            print(encoded_data_base64)  # Print the base64 encoded data for debugging
            if encoded_data_base64:
                # Decode the base64 encoded data to bytes
                encoded_data = base64.b64decode(encoded_data_base64)
                print("----------------------------------------")
                print("encoded_data:")
                print(encoded_data)  # Print the decoded bytes for debugging
                # Decode the UserConfiguration protobuf message
                decoded_data = decode_user_configuration(encoded_data)
                print("Decoded User Configurations:")
                print(decoded_data)  # Print the final decoded user configurations
            else:
                print("Error: 'encoded_data' not found in JSON file.")
    except Exception as e:
        print(f"Error: {e}")  # Print any error that occurs during the process

if __name__ == "__main__":
    # Ensure correct file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the JSON file
    json_file_path = os.path.join(current_dir, 'config.json')
    # Call the function to read and decode the JSON file
    read_json_and_decode(json_file_path)
