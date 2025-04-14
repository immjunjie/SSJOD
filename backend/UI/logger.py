import requests
import h5py
import time
import numpy as np
from datetime import datetime
import concurrent.futures

running = False

base_url = 'http://143.239.73.224/api/v1/printer'
gcode_path = '/Users/op5/Desktop/Repo/CS3300-Project/backend/extractor/merged/UMS5__3DBenchy.gcode'

endpoints = {
    "bed_temp": "/bed/temperature",
    "head_pos": "/heads/0/position",
    "nozzle_temp_current": "/heads/0/extruders/0/hotend/temp/current",
    "nozzle_temp_target": "/heads/0/extruders/0/hotend/temp/target",
    "time_spent_hot": "/heads/0/extruders/0/hotend/statistics/time_spent_hot",
    "material_extruded": "/heads/0/extruders/0/hotend/statistics/material_extruded",
    "led": "/led",
    "status": "/status",
    "jerk": "/heads/0/extruders/0/feeder/jerk",
    "active_material": "/heads/0/extruders/0/active_material",
    "length_remaining": "/heads/0/extruders/0/active_material/length_remaining",
    "max_speed": "/heads/0/extruders/0/feeder/max_speed"
}


def query(name, path):
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
                elif ";PRINT.SIZE.MIN.Z:" in line:
                    min_z = float(line.strip().split(":")[1])
                elif ";PRINT.SIZE.MAX.Z:" in line:
                    max_z = float(line.strip().split(":")[1])
                if layer_count is not None and min_z is not None and max_z is not None:
                    break

        if layer_count and min_z is not None and max_z is not None:
            return round((max_z - min_z) / (layer_count - 1), 4)
    except Exception as e:
        print(f"Failed to extract layer height: {e}")
    return None

def stop_logger():
    global running
    running = False


def run_logger(hdf5_filename="extract_info.hdf5"):
    global running
    if running:
        print("Logger is already running.")
        return
    running = True
    layer = 0
    scannum = 0
    last_z = 0.0
    lasttime = time.perf_counter()

    layer_height = extractLayerHeightgcode(gcode_path)
    if not layer_height:
        print("Layer height could not be determined.")
        return

    print("logging started. press ctrl+c to stop")

    with h5py.File(hdf5_filename, "w") as f:
        preprint_grp = f.create_group('preprint')
        layers_grp = f.create_group('layers')
        screenshots_grp = f.create_group('Screenshots')

        preprint_grp.create_group('STL')
        gcode_grp = preprint_grp.create_group('Gcode')

        with open(gcode_path, "r") as gcode_file:
            gcode_str = gcode_file.read()
            gcode_grp.create_dataset("full_text", data=gcode_str)

        preprint_grp.attrs['layer_height'] = layer_height
        preprint_grp.attrs['resolution'] = 'Ultimaker'
        screenshots_grp.attrs['format'] = 'JPEG'
        screenshots_grp.attrs['count'] = 0

        layer_grp = layers_grp.create_group(f'layer_{layer:04d}')

        try:
            running = True
            while running:
                scannum += 1
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(query, name, path) for name, path in endpoints.items()]
                    results = {future.result()[0]: future.result()[1] for future in concurrent.futures.as_completed(futures)}

                timestamp = datetime.now().isoformat()
                bed_info = results["bed_temp"]
                bed_current_temp = convert_to_float(bed_info.get("current", 0))
                bed_target_temp = convert_to_float(bed_info.get("target", 0))

                head_pos = results["head_pos"]
                try:
                    position_xyz = np.array([float(head_pos["x"]), float(head_pos["y"]), float(head_pos["z"])])
                except Exception:
                    position_xyz = np.array([0.0, 0.0, 0.0])

                current_z = position_xyz[2]
                if current_z >= (last_z + (layer_height - 0.05)) and current_z <= (last_z + (layer_height + 0.05)) or last_z == 0:
                    layer += 1
                    layer_grp = layers_grp.create_group(f'layer_{layer:04d}')
                    layer_grp.attrs['timestamp'] = timestamp
                    last_z = current_z
                    print('Layer changed:', layer)

                scan_grp = layer_grp.create_group(f'scan_{scannum:06d}')

                printer_head = scan_grp.create_group('printer_head')
                printer_head.create_dataset("position", data=position_xyz)

                extruder_grp = printer_head.create_group('extruder')
                extruder_grp.create_dataset("current_nozzle_temp", data=convert_to_float(results["nozzle_temp_current"]))
                extruder_grp.create_dataset("target_nozzle_temp", data=convert_to_float(results["nozzle_temp_target"]))
                extruder_grp.create_dataset("material_extruded", data=convert_to_float(results["material_extruded"]))

                bedplate_grp = scan_grp.create_group('bedplate')
                bedplate_grp.create_dataset("current_temp", data=bed_current_temp)
                bedplate_grp.create_dataset("target_temp", data=bed_target_temp)
                dt = h5py.string_dtype(encoding='utf-8')
                bedplate_grp.create_dataset("type", data=bed_info.get("type", "unknown"), dtype=dt)

                session_grp = scan_grp.create_group("session")
                session_grp.create_dataset("status", data="printing", dtype=dt)
                session_grp.create_dataset("time_spent_hot", data=convert_to_float(results["time_spent_hot"]))

                scan_grp.create_dataset("led_status", data=convert_to_float(results.get("led", 0)))
                scan_grp.create_dataset("printer_status", data=str(results.get("status", {})), dtype=dt)
                scan_grp.create_dataset("jerk", data=convert_to_float(results.get("jerk", 0)))
                scan_grp.create_dataset("active_material", data=convert_to_float(results.get("active_material", 0)))
                scan_grp.create_dataset("length_remaining", data=convert_to_float(results.get("length_remaining", 0)))
                scan_grp.create_dataset("max_speed", data=convert_to_float(results.get("max_speed", 0)))

                scan_grp.attrs['position_Z'] = current_z
                scan_grp.attrs['timestamp'] = timestamp

                now = time.perf_counter()
                elapsed = now - lasttime
                lasttime = now

                print(f'did scan: {scannum}  time: {elapsed:.3f} sec  position: {position_xyz}   layer: {layer}   last_z: {last_z}')
                # time.sleep(1)

        except KeyboardInterrupt:
            print("Logging stopped.")


if __name__ == "__main__":
    run_logger()