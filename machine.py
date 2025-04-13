import platform
import subprocess
import json
from datetime import datetime

def get_system_info():
    try:
        # Initialize an empty dictionary to store the system info
        system_info = {}

        # Get basic system information using the platform module
        system_info['system'] = platform.system()
        system_info['node'] = platform.node()
        system_info['release'] = platform.release()
        system_info['version'] = platform.version()
        system_info['machine'] = platform.machine()
        system_info['processor'] = platform.processor()

        # Get the current date and time
        system_info['executed_time'] = datetime.now().isoformat()

        # Get more detailed system information based on the platform
        if platform.system() == "Windows":
            # Execute the systeminfo command and capture the output
            output = subprocess.check_output(['systeminfo'], stderr=subprocess.STDOUT, text=True)
            system_info['systeminfo'] = output.strip()
        elif platform.system() == "Linux":
            # Get detailed hardware information using lshw
            output = subprocess.check_output(['lshw'], stderr=subprocess.STDOUT, text=True)
            system_info['lshw'] = output.strip()
            # Get detailed system information using uname
            output = subprocess.check_output(['uname', '-a'], stderr=subprocess.STDOUT, text=True)
            system_info['uname'] = output.strip()
        elif platform.system() == "Darwin":  # Darwin is the internal name for macOS
            # Get macOS version using sw_vers
            output = subprocess.check_output(['sw_vers'], stderr=subprocess.STDOUT, text=True)
            system_info['sw_vers'] = output.strip()
            # Get detailed system information using system_profiler
            output = subprocess.check_output(['system_profiler', 'SPHardwareDataType'], stderr=subprocess.STDOUT, text=True)
            # system_info['system_profiler'] = output.strip()

        # Convert the dictionary to a JSON string
        json_info = json.dumps(system_info, indent=4)

        # Print the JSON string
        print(json_info)

    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during the command execution
        print(f"An error occurred while running the command: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")

# Call the function to get and print system info
get_system_info()