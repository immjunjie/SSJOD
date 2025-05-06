import requests
import h5py
import time
import numpy as np
from datetime import datetime
import concurrent.futures
from filter_endpoints import filterMask


# Global control variable
running = False

# Organized endpoints: priority order (position, temperature, status, others)
def run_logger_with_socket(socketio, hdf5_filename, base_url, interval_time, endpoints, sequence, stl_path, gcode_path):
    run_logger( hdf5_filename, base_url, interval_time, endpoints, sequence, stl_path, gcode_path, socketio)

def query(base_url, name, path):
    """the call function for the printer api. runs for each call"""
    try:
        response = requests.get(base_url + path, timeout=2)
        return name, response.json()
    except Exception as e:
        return name, {"error": str(e)}


def convert_to_float(val):
    """used to convert the numerical outputs from the printer calls to floats"""
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
    """Extracts layer height from G-code file comments."""
    layer_count, min_z, max_z = None, None, None
    print(gcode_path)
    try:
        with open(gcode_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                if ";LAYER_COUNT:" in line:
                    layer_count = int(line.strip().split(":")[1])
                elif ";PRINT.SIZE.MIN.Z:" in line:
                    min_z = float(line.strip().split(":")[1])
                elif ";PRINT.SIZE.MAX.Z:" in line:
                    max_z = float(line.strip().split(":")[1])
                if layer_count and min_z is not None and max_z is not None:
                    break

        if layer_count is not None and min_z is not None and max_z is not None:
            return round((max_z - min_z) / (layer_count - 1), 4)
    except Exception as e:
        print(f"Failed to extract layer height: {e}")
    return None


def store_file_with_metadata(h5_group, file_path, dataset_name, description):
    """Stores a binary file in an HDF5 group with metadata. used for the stl and gcode preprint files"""
    with open(file_path, "rb") as f:
        data = f.read()
        dset = h5_group.create_dataset(dataset_name, data=np.void(data))
        dset.attrs["filesize_bytes"] = len(data)
        dset.attrs["description"] = description


def stop_logger():
    global running
    running = False


def run_logger(hdf5_filename, base_url, interval_time, endpoints, sequence, stl_path, gcode_path, socketio):
    """Main logger: fetches printer data, stores it in structured HDF5 file."""

    global running
    if running:
        print("Logger is already running.")
        return
    running = True

    layer = 0       # int variable for layer number
    scannum = 0     # int variable for scan number
    last_z = 0.0    # the position_z of the previous scan. on each scan, the new z is compared to this to detect if theres a change in layer 

    layer_height = extractLayerHeightgcode(gcode_path)  #gets the layer height from the gcode
    if not layer_height:
        print("Layer height could not be determined.")
        return

    print("Logging started. Press Ctrl+C to stop.")

    with h5py.File(hdf5_filename, "w") as f:
        # Preprint metadata section
        preprint_grp = f.create_group('preprint')
        stl_grp = preprint_grp.create_group('STL')
        gcode_grp = preprint_grp.create_group('Gcode')

        # Store binary files and raw G-code text
        store_file_with_metadata(stl_grp, stl_path, "_3DBenchy.stl", "STL file in binary")
        store_file_with_metadata(gcode_grp, gcode_path, "UMS5_3DBenchy.gcode", "G-code file in binary")

        #gcode file as readable string
        with open(gcode_path, "r") as gcode_file:
            gcode_str = gcode_file.read()
            gcode_grp.create_dataset("full_text", data=gcode_str)

        #attributes for preprint.
        preprint_grp.attrs['layer_height'] = layer_height
        preprint_grp.attrs['resolution'] = 'Ultimaker'

        # Screenshot metadata
        screenshots_grp = f.create_group('Screenshots')
        screenshots_grp.attrs['format'] = 'JPEG'
        screenshots_grp.attrs['count'] = 0

        #layers structure. creates an empty 'layer 0000' first. could be changed later idk.
        layers_grp = f.create_group('layers')
        layer_grp = layers_grp.create_group(f'layer_{layer:04d}')

        #looping through the printer api calls with threading.
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(endpoints))

        try:
            # the main scan loop. runs on repeat until scanning is stopped. 
            while running:
                scannum += 1
                start_time = time.perf_counter()

                # Query all endpoints in parallel
                futures = [executor.submit(query, base_url, name, path) for name, path in endpoints.items()]
                results = {future.result()[0]: future.result()[1] for future in concurrent.futures.as_completed(futures)}
                timestamp = datetime.now().isoformat()

                # Position
                try:
                    pos = results["head_pos"]
                    position_xyz = np.array([float(pos["x"]), float(pos["y"]), float(pos["z"])])
                except Exception:
                    position_xyz = np.array([0.0, 0.0, 0.0])

                # Layer tracking. changes layer if the position_z changes by the layer height. give or take 0.05mm. 
                current_z = position_xyz[2]
                if (current_z >= last_z + (layer_height - 0.05)) and (current_z <= last_z + (layer_height + 0.05)) or last_z == 0:
                    layer += 1
                    layer_grp = layers_grp.create_group(f'layer_{layer:04d}')
                    layer_grp.attrs['timestamp'] = timestamp
                    last_z = current_z
                    print('Layer changed:', layer)

                # creates the folder for this 'scan' that the data would be stored in. 
                scan_grp = layer_grp.create_group(f'scan_{scannum:06d}')
                dt = h5py.string_dtype(encoding='utf-8')

                # stores the data. the if statement checks if the box on the webpage was ticked for that data. 
                if sequence[0] == '1':
                    scan_grp.create_dataset("position", data=position_xyz)
                if sequence[1] == '1':
                    bed_info = results["bed_temp"]
                    scan_grp.create_dataset("bed_current_temp", data=convert_to_float(bed_info.get("current", 0)))
                    scan_grp.create_dataset("bed_target_temp", data=convert_to_float(bed_info.get("target", 0)))
                    scan_grp.create_dataset("bed_type", data=bed_info.get("type", "unknown"), dtype=dt)
                if sequence[2] == '1':
                    scan_grp.create_dataset("current_nozzle_temp", data=convert_to_float(results["nozzle_temp_current"]))
                if sequence[3] == '1':
                    scan_grp.create_dataset("target_nozzle_temp", data=convert_to_float(results["nozzle_temp_target"]))
                if sequence[4] == '1':
                    scan_grp.create_dataset("time_spent_hot", data=convert_to_float(results.get("time_spent_hot", 0)))
                if sequence[5] == '1':
                    scan_grp.create_dataset("printer_status", data=str(results.get("status", {})), dtype=dt)
                if sequence[6] == '1':
                    scan_grp.create_dataset("material_extruded", data=convert_to_float(results.get("material_extruded", 0)))
                if sequence[7] == '1':
                    scan_grp.create_dataset("led_status", data=convert_to_float(results.get("led", 0)))
                if sequence[8] == '1':
                    scan_grp.create_dataset("jerk", data=convert_to_float(results.get("jerk", 0)))
                if sequence[9] == '1':
                    scan_grp.create_dataset("active_material", data=convert_to_float(results.get("active_material", 0)))
                if sequence[10] == '1':
                    scan_grp.create_dataset("length_remaining", data=convert_to_float(results.get("length_remaining", 0)))
                if sequence[11] == '1':
                    scan_grp.create_dataset("max_speed", data=convert_to_float(results.get("max_speed", 0)))

                # === TIMESTAMP ===
                scan_grp.attrs['timestamp'] = timestamp

                # === EMIT VIA SOCKET ===
                if socketio:
                    log_entry = {
                        'scan': scannum,
                        'layer': layer,
                        'position_z': round(current_z, 2),
                        'timestamp': timestamp,
                    }
                    socketio.emit('new_log', log_entry)

                # Handle timing and wait interval
                elapsed = time.perf_counter() - start_time
                #sleep_time = max(0, interval_time - elapsed)
                #time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("Logging stopped.")


if __name__ == "__main__":
    run_logger(
        hdf5_filename='print_details.hdf5',
        base_url='http://143.239.73.224/api/v1/printer',
        interval_time=0.01,
        sequence = filterMask("111111111111"),
        stl_path = 'uploads/_3DBenchy.stl',
        gcode_path = 'uploads/UMS5__3DBenchy.gcode'
    )
