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
            ("7E804621E1203", {"F150_GEAR": "3"}),
        ]
    },
    # 2022 model year
    {
        "model_year": "2022",
        "signalset": "default.json",
        "tests": [
            ("7E804621E1201", {"F150_GEAR": "1"}),
            ("7E804621E1202", {"F150_GEAR": "2"}),
            ("7E804621E1203", {"F150_GEAR": "3"}),
            ("7E804621E1204", {"F150_GEAR": "4"}),
            ("7E804621E1205", {"F150_GEAR": "5"}),
            ("7E804621E1206", {"F150_GEAR": "6"}),
            ("7E804621E1207", {"F150_GEAR": "7"}),
            ("7E804621E1208", {"F150_GEAR": "8"}),
            ("7E804621E1209", {"F150_GEAR": "9"}),
            ("7E804621E120A", {"F150_GEAR": "10"}),
            ("7E804621E232E", {"F150_GEAR_SHFT": "DRIVE"}),
            ("7E804621E2346", {"F150_GEAR_SHFT": "PARK"}),
        ]
    },
    # 2021 model year
    {
        "model_year": "2021",
        "signalset": "default.json",
        "tests": [
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
            ("7280662404C23CE1D", {"F150_ODO": 234652.4}),
            ("7E80462F42F7D", {"F150_FLI": 49.01960784313726}),
            ("76805623201AB6A", {"F150_STEER_ANGLE": 555.6999999999998}),
            ("7E805621E1C0445", {"F150_TOT": 68.3125}),

            ("7E804621E1201", {"F150_GEAR": "1"}),
            ("7E804621E1202", {"F150_GEAR": "2"}),
            ("7E804621E1203", {"F150_GEAR": "3"}),
            ("7E804621E1204", {"F150_GEAR": "4"}),
            ("7E804621E1205", {"F150_GEAR": "5"}),
            ("7E804621E1206", {"F150_GEAR": "6"}),
            ("7E804621E1207", {"F150_GEAR": "7"}),
            ("7E804621E1208", {"F150_GEAR": "8"}),
            ("7E804621E1209", {"F150_GEAR": "9"}),
            ("7E804621E120A", {"F150_GEAR": "10"}),
            ("7E804621E232E", {"F150_GEAR_SHFT": "DRIVE"}),
            ("7E804621E2346", {"F150_GEAR_SHFT": "PARK"}),
        ]
    }
]

def load_signalset(filename: str) -> str:
    """Load a signalset JSON file from the standard location."""
    signalset_path = REPO_ROOT / "signalsets" / "v3" / filename
    with open(signalset_path) as f:
        return f.read()

@pytest.mark.parametrize(
    "test_group",
    TEST_CASES,
    ids=lambda test_case: f"MY{test_case['model_year']}"
)
def test_signals(test_group: Dict[str, Any]):
    """Test signal decoding against known responses."""
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
