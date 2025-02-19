import pytest
import os
import json
from pathlib import Path
from typing import Dict, Any

# These will be imported from the schemas repository
from schemas.python.signals_testing import obd_testrunner
from schemas.python.can_frame import CANIDFormat

REPO_ROOT = Path(__file__).parent.parent.absolute()

TEST_CASES = [
    # 2024 model year
    {
        "model_year": "2024",
        "signalset": "default.json",
        "tests": [
            # Gear: 3
            ("7E804621E1203", {"F150_CC_TGT_VSS": -61.2}),
        ]
    },
    # 2022 model year
    {
        "model_year": "2022",
        "signalset": "default.json",
        "tests": [
            # Gear: 3
            ("7E804621E1246", {"F150_CC_TGT_VSS": -61.2}),
        ]
    },
    # 2021 model year
    {
        "model_year": "2021",
        "signalset": "default.json",
        "tests": [
            # Target vehicle speed - -61.2 km/h
            ("76C0562A224FF56", {"F150_CC_TGT_VSS": -61.2}),
        ]
    },
    # 2019 model year
    {
        "model_year": "2019",
        "signalset": "default.json",
        "tests": [
            # Tire pressures
            ("72E05622813028C", {"F150_TP_FL": 32.6}),
            ("72E056228140273", {"F150_TP_FR": 31.35}),
            ("72E056228150291", {"F150_TP_RRO": 32.85}),
            ("72E05622816026E", {"F150_TP_RLO": 31.1}),
            ("72E056228170000", {"F150_TP_RRI": 0.0}),
            ("72E056228180000", {"F150_TP_RLI": 0.0}),
        ]
    },
    # 2012 model year
    {
        "model_year": "2012",
        "signalset": "0000-2015.json",
        "tests": [
            # Odometer - 234652.4 km
            ("7280662404C23CE1D", {"F150_ODO": 234652.4}),
            # Fuel level - 49.02%
            ("7E80462F42F7D", {"F150_FLI": 49.01960784313726}),
            # Steering angle - 555.7 degrees
            ("76805623201AB6A", {"F150_STEER_ANGLE": 555.6999999999998}),
            # Transmission oil temp - 68.31 C
            ("7E805621E1C0445", {"F150_TOT": 68.3125}),
        ]
    }
]

def load_signalset(filename: str) -> str:
    """Load a signalset JSON file from the standard location."""
    signalset_path = REPO_ROOT / "signalsets" / "v3" / filename
    with open(signalset_path) as f:
        return f.read()

@pytest.mark.parametrize("test_group", TEST_CASES)
def test_ford_f150_signals(test_group: Dict[str, Any]):
    """Test Ford F-150 signal decoding against known responses."""
    signalset_json = load_signalset(test_group["signalset"])

    # Run each test case in the group
    for response_hex, expected_values in test_group["tests"]:
        try:
            obd_testrunner(
                signalset_json,
                response_hex,
                expected_values,
                can_id_format=CANIDFormat.ELEVEN_BIT
            )
        except Exception as e:
            pytest.fail(
                f"Failed on response {response_hex} "
                f"(Model Year: {test_group['model_year']}, "
                f"Signalset: {test_group['signalset']}): {e}"
            )

if __name__ == '__main__':
    pytest.main([__file__])
