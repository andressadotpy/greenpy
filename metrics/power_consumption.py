import os
import re
from abc import abstractmethod
from typing import Callable


RAPL_PATH = "/sys/class/powercap/"
DEVICES_PATTERN = re.compile("intel-rapl:.")
ENERGY_FILENAME = "/energy_uj"

class PowerConsumption:

    @abstractmethod
    def measure(self, func: Callable):
        ...

class IntelCPUPowerConsumption:
    
    def __init__(self):
        self._devices = []
        self._rapl_devices = []
        self._set_devices()

    def _set_devices(self):
        rapl_directories = list(filter(lambda x: ':' in x, os.listdir(RAPL_PATH)))

        for directory in rapl_directories:
            if re.fullmatch(DEVICES_PATTERN, directory):
                with open(os.path.join(RAPL_PATH, directory, "name"), "r") as file:
                    name = file.read().strip()
                if name != "psys":
                    self._rapl_devices.append(directory)
                    self._devices.append(
                        self._format_rapl_name(directory)
                    )

    def _format_rapl_name(self, directory_name):
        if re.match(DEVICES_PATTERN, directory_name):
            return "cpu:" + directory_name[-1]

    def _read_usage(self, directory_name):
        energy_file = f"{RAPL_PATH}{directory_name}{ENERGY_FILENAME}"
        with open(energy_file, "r") as file:
            return file.read