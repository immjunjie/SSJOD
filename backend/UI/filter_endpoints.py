def filterMask(bit_sequence):
    endpoints = {
        "head_pos": "/heads/0/position",
        "bed_temp": "/bed/temperature",
        "nozzle_temp_current": "/heads/0/extruders/0/hotend/temp/current",
        "nozzle_temp_target": "/heads/0/extruders/0/hotend/temp/target",
        "time_spent_hot": "/heads/0/extruders/0/hotend/statistics/time_spent_hot",
        "status": "/status",
        "material_extruded": "/heads/0/extruders/0/hotend/statistics/material_extruded",
        "led": "/led",
        "jerk": "/heads/0/extruders/0/feeder/jerk",
        "active_material": "/heads/0/extruders/0/active_material",
        "length_remaining": "/heads/0/extruders/0/active_material/length_remaining",
        "max_speed": "/heads/0/extruders/0/feeder/max_speed"
    }

    # Ensure the bit sequence is valid
    #if len(bit_sequence) != len(endpoints):
    #   raise ValueError("Bit sequence must be 12 bits long.")

    keys = list(endpoints.keys())
    filtered = {
        key: endpoints[key]
        for i, key in enumerate(keys)
        if bit_sequence[i] == '1'
    }

    return filtered