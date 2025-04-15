import requests
import h5py
import time
import numpy as np
from datetime import datetime
import concurrent.futures
import os

base_url='http://143.239.73.224/api/v1/printer'

gcode_path = '/Users/sb36/CS3300-Project/backend/extractor/merged/UMS5__3DBenchy.gcode'
stl_path = '/Users/sb36/CS3300-Project/backend/extractor/merged/_3DBenchy.stl'

endpoints = {
    "bed_temp": "/bed/temperature",
    "head_pos":"/heads/0/position",
    "nozzle_temp_current":"/heads/0/extruders/0/hotend/temp/current",
    "nozzle_temp_target":"/heads/0/extruders/0/hotend/temp/target",
    "time_spent_hot":"/heads/0/extruders/0/hotend/statistics/time_spent_hot",
    "material_extruded":"/heads/0/extruders/0/hotend/statistics/material_extruded",
    "led":"/led",
    "status":"/status",
    "jerk":"/heads/0/extruders/0/feeder/jerk",
    "acive_material":"/heads/0/extruders/0/active_material",
    "length_remaining":"/heads/0/extruders/0/active_material/length_remaining",
    "max_speed":"/heads/0/extruders/0/feeder/max_speed"
}

def query( name, path):
    try:
        response = requests.get(base_url + path, timeout=2)
        return name, response.json()
    except Exception as e:
        return name, {"error": str(e)}
    
def convert_to_float(val):
    if isinstance(val, dict):
        for key in ["current", "value"]:
            if key in val:
                try:
                    return float(val[key])
                except:
                    continue
        return 0.0
    try:
        return float(val)
    except:
        return 0.0

def extractLayerHeightgcode(gcode_path):
    layer_count = None
    min_z = None
    max_z = None

    try:
        with open(gcode_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                if ";LAYER_COUNT:" in line:
                    layer_count = int(line.strip().split(":")[1])
                    print(f"Found layer count: {layer_count}")
                elif ";PRINT.SIZE.MIN.Z:" in line:
                    min_z = float(line.strip().split(":")[1])
                    print(f"Found min Z: {min_z}")
                elif ";PRINT.SIZE.MAX.Z:" in line:
                    max_z = float(line.strip().split(":")[1])
                    print(f"Found max Z: {max_z}")
                if layer_count is not None and min_z is not None and max_z is not None:
                    break

        if layer_count and min_z is not None and max_z is not None:
            layer_height = round((max_z - min_z) / (layer_count - 1), 4)
            print(f"Calculated layer height: {layer_height}")
            return layer_height
        else:
            print("Missing one or more required values in G-code.")
    except Exception as e:
        print(f"Failed to extract layer height: {e}")

    return None

def store_file_with_metadata(h5_group, file_path, dataset_name, description):
    # Read binary content
    with open(file_path, "rb") as f:
        data = f.read()
        # Store binary blob
        dset = h5_group.create_dataset(dataset_name, data=np.void(data))

    dset.attrs["filesize_bytes"] = len(data)
    dset.attrs["description"] = description

if __name__=="__main__":
    
    layer = 0
    scannum = 0
    last_z = 0.0
    lasttime = 0

    print("logging. press ctrl+c to stop")
    with h5py.File("extract_info.hdf5", "w") as f:
        #   Create main groups
        preprint_grp = f.create_group('preprint')
        layers_grp = f.create_group('layers')
        screenshots_grp = f.create_group('Screenshots')

        #   Create subgroups in preprint
        stl_grp = preprint_grp.create_group('STL')
        Gcode_grp = preprint_grp.create_group('Gcode')

        #add full gCode as string
        with open(gcode_path, "r") as gcode_file:
            gcode_str = gcode_file.read()
            Gcode_grp.create_dataset("full_text", data=gcode_str)

        #   Example: adding metadata to preprint
        stl_des = 'the stl file stored as binary'
        gcode_des = 'the gcode file stored as binary'
        store_file_with_metadata(stl_grp, stl_path, "_3DBenchy.stl", stl_des)
        store_file_with_metadata(Gcode_grp, gcode_path, "UMS5_3DBenchy.gcode", gcode_des)

        #   getting layerheight from gcode
        layer_height = extractLayerHeightgcode(gcode_path)
        preprint_grp.attrs['layer_height'] = layer_height if layer_height else "unknown"
        print(f"Layer height: {layer_height} mm")

        preprint_grp.attrs['resolution'] = 'Blue sk7'

        #   Screenshots group could hold images as datasets in future
        screenshots_grp.attrs['format'] = 'JPEG'
        screenshots_grp.attrs['count'] = 0  # To be updated when adding images

        layer_grp = layers_grp.create_group(f'layer: {layer:04d}')

        #loop
        try:
            while True:
                scannum += 1

                #threading queries
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(query, name, path) for name, path in endpoints.items()]
                    results = {}
                    for future in concurrent.futures.as_completed(futures):
                        name, data = future.result()
                        results[name] = data

                # Check that each endpoint returned data
                required = ["bed_temp", "head_pos", "nozzle_temp_current", "nozzle_temp_target", "time_spent_hot", "material_extruded"]

                # Timestamp for this scan
                timestamp = datetime.now().isoformat()

                # Extract and convert values
                # For bed_temp, it might be an object with "current" and "target"
                bed_info = results["bed_temp"]
                if isinstance(bed_info, dict):
                    bed_current_temp = convert_to_float(bed_info.get("current", 0))
                    bed_target_temp = convert_to_float(bed_info.get("target", 0))
                else:
                    bed_current_temp = convert_to_float(bed_info)
                    bed_target_temp = 0.0

                # Head position should be a dict with x, y, z
                head_pos = results["head_pos"]
                try:
                    position_xyz = np.array([float(head_pos["x"]), float(head_pos["y"]), float(head_pos["z"])])
                except Exception as e:
                    position_xyz = np.array([0.0, 0.0, 0.0])
                current_z = float(position_xyz[2])

                # layer change check
                if current_z >= (last_z + (layer_height - 0.05)) and current_z <= (last_z + (layer_height + 0.05)) or last_z == 0:
                    layer += 1
                    layer_grp = layers_grp.create_group(f'layer_{layer}_timestamp_{timestamp}')
                    print('layer change')
                    last_z = current_z


                nozzle_temp_current = convert_to_float(results["nozzle_temp_current"])
                nozzle_temp_target = convert_to_float(results["nozzle_temp_target"])
                time_spent_hot = convert_to_float(results["time_spent_hot"])
                material_extruded = convert_to_float(results["material_extruded"])

                led_status = convert_to_float(results.get("led", 0))
                printer_status = results.get("status", {})
                jerk = convert_to_float(results.get("jerk", 0))
                active_material = convert_to_float(results.get("acive_material", 0))
                length_remaining = convert_to_float(results.get("length_remaining", 0))
                max_speed = convert_to_float(results.get("max_speed", 0))

                scan_grp = layer_grp.create_group(f'scan_{scannum:06d}_timestamp_{timestamp}')

                # Create subgroup for printer head data
                printer_head = scan_grp.create_group('printer_head')
                printer_head.create_dataset("position", data=position_xyz)
                printer_head.create_dataset("X_position", data=position_xyz[0])
                printer_head.create_dataset("Y_position", data=position_xyz[1])
                printer_head.create_dataset("Z_position", data=position_xyz[2])

                # Extruder data
                extruder_grp = printer_head.create_group('extruder')
                extruder_grp.create_dataset("current_nozzle_temp", data=nozzle_temp_current)
                extruder_grp.create_dataset("target_nozzle_temp", data=nozzle_temp_target)
                extruder_grp.create_dataset("material_extruded", data=material_extruded)

                # Bedplate data
                bedplate_grp = scan_grp.create_group('bedplate')
                bedplate_grp.create_dataset("current_temp", data=bed_current_temp)
                bedplate_grp.create_dataset("target_temp", data=bed_target_temp)
                dt = h5py.string_dtype(encoding='utf-8')
                bedplate_grp.create_dataset("type", data=bed_info.get("type", "unknown"), dtype=dt)

                # Session metadata
                session_grp = scan_grp.create_group("session")
                session_grp.create_dataset("status", data="printing", dtype=dt)
                session_grp.create_dataset("time_spent_hot", data=time_spent_hot)

                # Add the new endpoint data into scan
                scan_grp.create_dataset("led_status", data=led_status)
                scan_grp.create_dataset("printer_status", data=str(printer_status), dtype=dt)  # Store as string
                scan_grp.create_dataset("jerk", data=jerk)
                scan_grp.create_dataset("active_material", data=active_material)
                scan_grp.create_dataset("length_remaining", data=length_remaining)
                scan_grp.create_dataset("max_speed", data=max_speed)

                # Set additional attributes for this scan group
                scan_grp.attrs['position_Z'] = position_xyz[2] # example value
                scan_grp.attrs['timestamp'] = timestamp

                
                now = time.perf_counter()
                timestamp = now - lasttime
                lasttime = now

            #   1 second pause before looping again
                print('did scan: ' + str(scannum) + '  time: ' + f'{timestamp:.3f}' + '  position: ' + f'{position_xyz}' + '   layer: ' + f'{layer}' + '   last_z: ' + f'{last_z}')
                
        except KeyboardInterrupt:
            print("       logging stopped")