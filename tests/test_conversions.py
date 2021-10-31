from metrics.conversions import watt_to_kW, kW_to_watt


def test_1_watt_to_kW():
    kW = watt_to_kW(1)

    assert kW == 0.001

def test_1_kW_to_watt():
    watt = kW_to_watt(1)

    assert watt == 1000