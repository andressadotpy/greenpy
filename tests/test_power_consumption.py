import pytest

from metrics.power_consumption import PowerConsumption, IntelCPUPowerConsumption


#def test_power_consumption():
#    def fibonacci(n=30):
#        if n <= 1:
#            return n
#        else:
#            return(fibonacci(n-1) + fibonacci(n-2))

#    fibonacci_power_consumption = PowerConsumption.measure(fibonacci)

#    assert isinstance(fibonacci_power_consumption, float)

def test_formatter_get_matching_device():
    intel = IntelCPUPowerConsumption()
    valid_device = "intel-rapl:0"

    expacted_format = "cpu:0"
    formatted = intel._format_rapl_name(valid_device)
    assert expacted_format == formatted

def test_formatter_dont_get_not_matching_device():
    intel = IntelCPUPowerConsumption()
    invalid_device = "intel-rapl"

    formatted = intel._format_rapl_name(invalid_device)

    assert formatted == None

def test_read_usage_file():
    intel = IntelCPUPowerConsumption()
    directory_name = "intel-rapl:0"
    usage = intel._read_energy_usage(directory_name)

    assert usage is not None

def test_measuring_power():
    intel = IntelCPUPowerConsumption()
    measurements = intel.get_measurement_for_each_rapl_device()

    assert isinstance(measurements, list)
    assert len(measurements) != 0