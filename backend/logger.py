# /backend/logger
import requests  # HTTP client
import h5py  # HDF5 file handling
import time  # Timing loops
import numpy as np  # Numerical arrays
from datetime import datetime  # Timestamps
import concurrent.futures  # Thread pool for parallel queries
from backend.extract_snapshots import PrinterSnapshotter


# Global control flag for the logger loop
running = False


# Helper to query a single endpoint
def query(base_url, name, path):
    try:
        response = requests.get(base_url + path, timeout=2)
        return name, response.json()
    except Exception as e:
        return name, {"error": str(e)}

# Normalize values to float for storage
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

# Parse G-code comments to estimate layer height
def extractLayerHeightgcode(gcode_path):
    layer_count, min_z, max_z = None, None, None
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
            # Calculate consistent layer height from range / (count-1)
            return round((max_z - min_z) / (layer_count - 1), 4)
    except Exception as e:
        print(f"Failed to extract layer height: {e}")
    return None

# Embed binary files into HDF5 with metadata
def store_file_with_metadata(h5_group, file_path, dataset_name, description):
    with open(file_path, "rb") as f:
        data = f.read()
        dset = h5_group.create_dataset(dataset_name, data=np.void(data))
        dset.attrs["filesize_bytes"] = len(data)
        dset.attrs["description"] = description

# Signal loop to stop
def stop_logger():
    global running
    running = False


def run_logger_with_socket(socketio, hdf5_filename, base_url, camera_url, endpoints, sequence, stl_path, gcode_path, max_duration=None):
    global running
    if running:
        print("Logger is already running.")
        return
    running = True

    layer = 0
    scannum = 0
    last_z = 0.0

    # Initialize snapshotter if camera URL is provided
    snapshotter = None
    screenshots_enabled = sequence[-1] == '1' if len(sequence) >= 12 else False
    if camera_url and screenshots_enabled:
        snapshotter = PrinterSnapshotter(camera_url, hdf5_filename)
        print(f"Snapshotter initialized with camera URL: {camera_url}")

    layer_height = extractLayerHeightgcode(gcode_path)  #gets the layer height from the gcode
    if not layer_height:
        print("Layer height could not be determined.")
        return

    print("Logging started. Press Ctrl+C to stop.")

    with h5py.File(hdf5_filename, "w") as f:
        # Store preprint metadata: STL and G-code files
        preprint_grp = f.create_group('preprint')
        stl_grp = preprint_grp.create_group('STL')
        gcode_grp = preprint_grp.create_group('Gcode')

        store_file_with_metadata(stl_grp, stl_path, "_3DBenchy.stl", "STL file in binary")
        store_file_with_metadata(gcode_grp, gcode_path, "UMS5_3DBenchy.gcode", "G-code file in binary")

        # Also store full G-code text for debugging
        with open(gcode_path, "r") as gcode_file:
            gcode_str = gcode_file.read()
            gcode_grp.create_dataset("full_text", data=gcode_str)

        preprint_grp.attrs['layer_height'] = layer_height
        preprint_grp.attrs['resolution'] = 'Ultimaker'

        # Prepare screenshot group and layer storage
        screenshots_grp = f.create_group('Screenshots')
        screenshots_grp.attrs['format'] = 'JPEG'
        screenshots_grp.attrs['count'] = 0

        layers_grp = f.create_group('layers')

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(endpoints))

        start_time = time.time()

        first_scan = True
        try:
            while running:
                if max_duration is not None and (time.time() - start_time) >= max_duration:
                    print(f"Logging stopped after {max_duration} seconds.")
                    break
                scannum += 1

                # Query all enabled endpoints concurrently
                futures = [executor.submit(query, base_url, name, path) for name, path in endpoints.items()]
                results = {future.result()[0]: future.result()[1] for future in concurrent.futures.as_completed(futures)}
                timestamp = datetime.now().isoformat()

                # Compute current head Z and detect layer changes
                try:
                    pos = results["head_pos"]
                    position_xyz = np.array([float(pos["x"]), float(pos["y"]), float(pos["z"])])
                except Exception:
                    position_xyz = np.array([0.0, 0.0, 0.0])

                current_z = position_xyz[2]

                if first_scan:
                    layer = int(round(current_z / layer_height))
                    layer_grp = layers_grp.create_group(f'layer_{layer:04d}')
                    layer_grp.attrs['timestamp'] = timestamp
                    last_z = current_z
                    first_scan = False
                    print(f"Starting at layer {layer} (Z={current_z:.3f} mm)")

                elif (current_z >= last_z + (layer_height - 0.05) and current_z <= last_z + (layer_height + 0.05)) or last_z == 0: #BRACKETS
                    layer += 1
                    layer_grp = layers_grp.create_group(f'layer_{layer:04d}')
                    layer_grp.attrs['timestamp'] = timestamp
                    last_z = current_z
                    print('Layer changed:', layer)

                    # Capture snapshot for this layer if snapshotter is initialized
                    if snapshotter:  # Skip layer 0
                        print(f"Capturing snapshot for layer {layer}")
                        snapshotter.capture_layer_snapshot(layer)

                # Create dataset for this scan
                scan_grp = layer_grp.create_group(f'scan_{scannum:06d}')
                dt = h5py.string_dtype(encoding='utf-8')

                # Conditionally store each telemetry value
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


                # Always store timestamp and emit via WebSocket
                scan_grp.attrs['timestamp'] = timestamp
                if socketio:
                    endpoint_data = {}

                    if sequence[0] == '1':
                        endpoint_data["X"] = round(position_xyz[0], 3)
                        endpoint_data["Y"] = round(position_xyz[1], 3)
                        endpoint_data["Z"] = round(position_xyz[2], 3)

                    if sequence[1] == '1':
                        bed_info = results.get("bed_temp", {})
                        endpoint_data["Bed Temp"] = convert_to_float(bed_info.get("current", 0))

                    if sequence[2] == '1':
                        endpoint_data["currentTemp"] = convert_to_float(results.get("nozzle_temp_current", 0))

                    if sequence[8] == '1':
                        endpoint_data["Jerk"] = convert_to_float(results.get("jerk", 0))

                    if sequence[9] == '1':
                        endpoint_data["ActiveMaterial"] = convert_to_float(results.get("active_material", 0))

                    log_entry = {
                        'scan': scannum,
                        'layer': layer,
                        'timestamp': timestamp,
                        'endpoint_data': endpoint_data
                    }
                    socketio.emit('new_log', log_entry)

                # Loop timing control can be added here (commented out)
        except KeyboardInterrupt:
            print("Logging stopped.")