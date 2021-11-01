import os
import re
from abc import abstractmethod
from typing import Callable, List


RAPL_PATH = "/sys/class/powercap/"
DEVICES_PATTERN = re.compile("intel-rapl:.")
ENERGY_FILENAME = "/energy_uj"

class PowerConsumption:

    @abstractmethod
    def measure(self, func: Callable):
        ...

class IntelCPUPowerConsumption(PowerConsumption):
    
    def __init__(self):
        self._devices = []
        self._rapl_devices = []
        self._set_devices()

    def measure(self, func: Callable):
        super().measure(func)
        measure_before_func_call = self.get_measurement_for_each_rapl_device()
        func()
        measure_after_func_call = self.get_measurement_for_each_rapl_device()
        return measure_after_func_call - measure_before_func_call

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

    def _format_rapl_name(self, directory_name: str) -> str:
        if re.match(DEVICES_PATTERN, directory_name):
            return "cpu:" + directory_name[-1]

    def _read_energy_usage(self, directory_name: str) -> str:
        energy_file = f"{RAPL_PATH}{directory_name}{ENERGY_FILENAME}"
        with open(energy_file, "r") as file:
            return int(file.read())

    def get_measurement_for_each_rapl_device(self) -> List[int]:
        measurements = []
        for directory in self._rapl_devices:
            try:
                power_usage = self._read_energy_usage(directory)
                measurements.append(power_usage)
            except FileNotFoundError:
                parts_pattern = re.compile(r"intel-rapl:(\d):(\d)")
                parts = [
                    f for f in os.listdir(os.path.join(RAPL_PATH, directory))
                    if re.match(parts_pattern, f)
                ]
                total_power_usage = 0
                for part in parts:
                    total_power_usage += self._read_energy_usage(part)
                measurements.append(total_power_usage)
                
        return measurements