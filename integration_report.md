# F-150 PID Integration Report

## Summary

Successfully integrated PIDs from related Ford vehicle JSON files into the F-150's default.json file.

### Integration Results

| Source File | New PIDs Added | Total PIDs in Source |
|-------------|---------------|---------------------|
| ranger.json | 25 | 35 |
| bronco.json | 9 | 17 |
| explorer.json | 0 | 4 |
| explorer-tivct.json | 1 | 2 |
| **TOTAL** | **35** | **58** |

### File Statistics

- **PIDs before integration:** 106
- **PIDs after integration:** 141
- **Total new PIDs added:** 35
- **No duplicate PIDs detected:** ✓
- **All 7E0 headers have rax=7E8:** ✓ (99 PIDs)

## Changes Applied

For each new PID added, the following transformations were applied:

1. ✓ Signal IDs updated from source prefix (RANGER_, BRONCO_, EXPLORER_, Ford_) to F150_ prefix
2. ✓ Set `dbg: true` for all new PIDs
3. ✓ Added `rax: "7E8"` for all PIDs with `hdr: "7E0"` (if not already present)
4. ✓ Assigned reasonable `freq` values based on parameter type:
   - 0.1-0.25: Real-time critical (speed, RPM, throttle)
   - 1: Medium-high frequency (pressure, torque, fuel)
   - 2: Medium frequency (temperature, voltage, current)
   - 5: Low frequency (battery, oil life, distance)
   - 60: Very low frequency (DTCs, warm-ups)
5. ✓ Preserved all `fmt`, `name`, `path`, and `description` fields from source files
6. ✓ Removed `dbgfilter` from new PIDs (to make them active by default)

## New PIDs by Category

### From Ranger (25 PIDs)

**Engine/PCM Parameters:**
- 22:0334 - Cylinder head temperature corrected
- 22:033E - Boost absolute pressure raw value
- 22:0345 - Misfire events detected during latest misfire operation cycle
- 22:0382 - Acceleration of cylinder 1 normalized to misfire monitor threshold
- 22:0388 - Acceleration of cylinder 2 normalized to misfire monitor threshold
- 22:038A - Acceleration of cylinder 3 normalized to misfire monitor threshold
- 22:038B - Acceleration of cylinder 4 normalized to misfire monitor threshold
- 22:038C - Acceleration of cylinder 5 normalized to misfire monitor threshold
- 22:0398 - Acceleration of cylinder 6 normalized to misfire monitor threshold
- 22:03EC - Knock control spark retard
- 22:0415 - Engine oil pressure raw
- 22:0461 - Charge air cooler temperature (b1 s1)
- 22:054B - Engine oil life remaining
- 22:05AC - Cylinder 1 knock/combustion performance counter
- 22:05AD - Cylinder 2 knock/combustion performance counter
- 22:05AE - Cylinder 3 knock/combustion performance counter
- 22:05AF - Cylinder 4 knock/combustion performance counter
- 22:05B0 - Cylinder 5 knock/combustion performance counter
- 22:05B1 - Cylinder 6 knock/combustion performance counter
- 22:05FC - Cylinder head temperature sensor 2 raw
- 22:0604 - A/C refrigerant pressure

**Transmission Parameters:**
- 22:1E19 - Commanded transmission gear ratio
- 22:1E1A - Commanded transmission main line pressure

**Trip/Vehicle Data:**
- 22:4194 - Distance to empty calculated
- 22:4195 - Distance to empty displayed

### From Bronco (9 PIDs)

**AWD System Parameters (hdr: 703):**
- 22:017C - Actuator cam position corrected
- 22:017E - Power transfer unit input shaft speed
- 22:017F - Actuator duty cycle output commanded
- 22:0182 - Power transfer unit requested torque
- 22:0184 - Power transfer unit sump temperature
- 22:0185 - Power transfer unit requested torque capacity inferred
- 22:1E9E - Measured current of clutch A actuator
- 22:3B40 - Foot brake
- 22:D00F - Hydraulic pump motor current

### From Explorer (0 PIDs)

All PIDs from explorer.json were already present in the F-150 default.json.

### From Explorer Ti-VCT (1 PID)

**Drivetrain Parameters:**
- 22:070D - Transfer case fluid temperature

## Conflicts and Issues

**No conflicts encountered:**
- ✓ All new PIDs had unique command codes (22:XXXX)
- ✓ No duplicate PIDs were created
- ✓ All signal ID transformations completed successfully

## Validation

The integrated file was reformatted using:
```bash
python3 tests/schemas/cli.py signalsets/v3/default.json --output signalsets/v3/default.json
```

**Validation checks passed:**
- ✓ JSON syntax valid
- ✓ No duplicate command codes
- ✓ All 7E0 headers have rax=7E8
- ✓ All new PIDs have dbg=true
- ✓ All signal IDs properly prefixed with F150_

## File Location

**Target file:** `/workspaces/Ford-F-150/signalsets/v3/default.json`

## Notes

- PIDs that already existed in default.json were not duplicated
- The integration preserved all existing PIDs in default.json
- New PIDs are marked with `dbg: true` to indicate they are experimental/debug parameters
- Frequency values were intelligently assigned based on parameter characteristics
- All AWD-related PIDs from Bronco were successfully integrated (header 703)
