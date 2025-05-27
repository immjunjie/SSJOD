# /backend/extractor.py

import os
import time
import h5py
import requests
import numpy as np
import concurrent.futures
from datetime import datetime
from .filter_endpoints import filterMask
from .extract_snapshots import PrinterSnapshotter

PRINTER_API_TIMEOUT = float(os.getenv("PRINTER_API_TIMEOUT"))


from threading import Event
cancel_event = Event()

def stop_extraction():
    cancel_event.set()

def convert_to_float(val):
    if isinstance(val, dict):
        for key in ("current", "value"):
            if key in val:
                try:
                    return float(val[key])
                except:
                    pass
        return 0.0
    try:
        return float(val)
    except:
        return 0.0

def extract_layer_height(gcode_path):
    layer_count = min_z = max_z = None
    try:
        with open(gcode_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if ";LAYER_COUNT:" in line:
                    layer_count = int(line.split(":",1)[1])
                elif ";PRINT.SIZE.MIN.Z:" in line:
                    min_z = float(line.split(":",1)[1])
                elif ";PRINT.SIZE.MAX.Z:" in line:
                    max_z = float(line.split(":",1)[1])
                if layer_count is not None and min_z is not None and max_z is not None:
                    break
        if layer_count and min_z is not None and max_z is not None:
            return round((max_z - min_z) / (layer_count - 1), 4)
    except Exception as e:
        print("Failed to extract layer height:", e)
    return None

def store_file_with_metadata(h5_group, file_path, dataset_name, description):
    with open(file_path, "rb") as f:
        data = f.read()
    dset = h5_group.create_dataset(dataset_name, data=np.void(data))
    dset.attrs["filesize_bytes"] = len(data)
    dset.attrs["description"] = description

def query(base_url, name, path):
    try:
        r = requests.get(base_url + path, timeout=PRINTER_API_TIMEOUT)
        return name, r.json()
    except Exception as e:
        return name, {"error": str(e)}

def run_extraction(
    printer_ip: str,
    stl_path: str,
    gcode_path: str,
    output_hdf5: str,
    sequence_bits: str,
    max_duration: float = None,
    delay_sec: float = 0.0,
    socketio=None
 ):
    
    # reset any previous cancellation
    cancel_event.clear()
    """
    Poll the printer API, write an HDF5 at output_hdf5, then exit.
    """
    base_url  = f"http://{printer_ip}/api/v1/printer"
    cam_url   = f"http://{printer_ip}/api/v1/camera"
    endpoints = filterMask(sequence_bits)

    layer_height = extract_layer_height(gcode_path)
    if layer_height is None:
        raise RuntimeError("Cannot determine layer height from G-code")

    # set up snapshotter if requested
    snapshotter = None
    if sequence_bits[-1] == "1":
        snapshotter = PrinterSnapshotter(cam_url, output_hdf5)
        print("Snapshotter enabled on camera URL:", cam_url)

    # open HDF5 file
    with h5py.File(output_hdf5, "w") as f:
        # preprint metadata
        preprint = f.create_group("preprint")
        stl_grp  = preprint.create_group("STL")
        gc_grp   = preprint.create_group("Gcode")
        store_file_with_metadata(stl_grp, stl_path, os.path.basename(stl_path), "STL binary")
        store_file_with_metadata(gc_grp,  gcode_path, os.path.basename(gcode_path), "G-code binary")
        # store full text for debugging
        with open(gcode_path, "r") as gf:
            gc_grp.create_dataset("full_text", data=gf.read())
        preprint.attrs["layer_height"] = layer_height
        preprint.attrs["resolution"]   = "Ultimaker"

        # screenshots group
        shots = f.create_group("Screenshots")
        shots.attrs["format"] = "JPEG"
        shots.attrs["count"]  = 0

        # layers container
        layers_grp = f.create_group("layers")

        # executor for parallel queries
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(endpoints))

        start_time = time.time()
        scan_num   = 0
        layer      = 0
        last_z     = 0.0
        first      = True

        print("Beginning extraction…")
        while not cancel_event.is_set():
            # respect max_duration
            if max_duration and (time.time() - start_time) >= max_duration:
                print("Reached max_duration—stopping.")
                break

            scan_num += 1
            # fetch endpoints
            futures = [
                executor.submit(query, base_url, name, path)
                for name, path in endpoints.items()
            ]
            results = {
                fut.result()[0]: fut.result()[1]
                for fut in concurrent.futures.as_completed(futures)
            }
            timestamp = datetime.now().isoformat()

            # compute position
            try:
                pos = results["head_pos"]
                xyz = np.array([float(pos["x"]), float(pos["y"]), float(pos["z"])])
            except:
                xyz = np.array([0.0, 0.0, 0.0])
            current_z = xyz[2]

            # decide layer group
            if first:
                layer = int(round(current_z / layer_height))
                grp   = layers_grp.create_group(f"layer_{layer:04d}")
                grp.attrs["timestamp"] = timestamp
                last_z  = current_z
                first   = False
                print(f"Starting at layer {layer}, Z={current_z:.3f}")
            elif abs(current_z - (last_z + layer_height)) < 0.05:
                layer += 1
                grp   = layers_grp.create_group(f"layer_{layer:04d}")
                grp.attrs["timestamp"] = timestamp
                last_z  = current_z
                print("Layer changed →", layer)
                if snapshotter:
                    snapshotter.capture_layer_snapshot(layer)

            # write scan group
            scan_grp = grp.create_group(f"scan_{scan_num:06d}")
            scan_grp.attrs["timestamp"] = timestamp
            dt = h5py.string_dtype(encoding="utf-8")

            # position
            if sequence_bits[0] == "1":
                scan_grp.create_dataset("position", data=xyz)
            # bed temp
            if sequence_bits[1] == "1":
                bed = results.get("bed_temp", {})
                scan_grp.create_dataset("bed_current_temp", data=convert_to_float(bed.get("current",0)))
                scan_grp.create_dataset("bed_target_temp",  data=convert_to_float(bed.get("target",0)))
                scan_grp.create_dataset("bed_type",         data=bed.get("type",""), dtype=dt)
            # nozzle current
            if sequence_bits[2] == "1":
                scan_grp.create_dataset("current_nozzle_temp", data=convert_to_float(results.get("nozzle_temp_current",0)))
            # nozzle target
            if sequence_bits[3] == "1":
                scan_grp.create_dataset("target_nozzle_temp",  data=convert_to_float(results.get("nozzle_temp_target",0)))
            # time_spent_hot
            if sequence_bits[4] == "1":
                scan_grp.create_dataset("time_spent_hot", data=convert_to_float(results.get("time_spent_hot",0)))
            # status
            if sequence_bits[5] == "1":
                scan_grp.create_dataset("printer_status", data=str(results.get("status",{})), dtype=dt)
            # material_extruded
            if sequence_bits[6] == "1":
                scan_grp.create_dataset("material_extruded", data=convert_to_float(results.get("material_extruded",0)))
            # led
            if sequence_bits[7] == "1":
                scan_grp.create_dataset("led_status", data=convert_to_float(results.get("led",0)))
            # jerk
            if sequence_bits[8] == "1":
                scan_grp.create_dataset("jerk", data=convert_to_float(results.get("jerk",0)))
            # active_material
            if sequence_bits[9] == "1":
                scan_grp.create_dataset("active_material", data=convert_to_float(results.get("active_material",0)))
            # length_remaining
            if sequence_bits[10] == "1":
                scan_grp.create_dataset("length_remaining", data=convert_to_float(results.get("length_remaining",0)))
            # max_speed
            if sequence_bits[11] == "1":
                scan_grp.create_dataset("max_speed", data=convert_to_float(results.get("max_speed",0)))

            # delay
            if delay_sec:
                # sleep in small increments so we can respond to cancel_event quickly
                slept = 0.0
                while slept < delay_sec and not cancel_event.is_set():
                    time.sleep(min(0.1, delay_sec - slept))
                    slept += min(0.1, delay_sec - slept)

            if socketio:
                endpoint_data = {}
                if sequence_bits[0] == '1':
                    endpoint_data["X"] = round(xyz[0], 3)
                    endpoint_data["Y"] = round(xyz[1], 3)
                    endpoint_data["Z"] = round(xyz[2], 3)
                if sequence_bits[1] == '1':
                    bed_info = results.get("bed_temp", {})
                    endpoint_data["Bed Temp"] = convert_to_float(bed_info.get("current", 0))
                # build the same payload your UI expects:
                payload = {
                    "scan": scan_num,
                    "layer": layer,
                    "timestamp": timestamp,
                    "endpoint_data": endpoint_data
                }
                socketio.emit("new_log", payload)

    print("Extraction complete:", output_hdf5)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Standalone 3D-printer HDF5 extractor")
    parser.add_argument("printer_ip", help="IP (and optional port) of the printer")
    parser.add_argument("stl_path",   help="Path to the STL file")
    parser.add_argument("gcode_path", help="Path to the GCODE file")
    parser.add_argument("output_hdf5",help="Where to write the .hdf5")
    parser.add_argument("--sequence",
                        default="1"*12,
                        help="12-bit string to enable endpoints (e.g. 11110000...)")
    parser.add_argument("--duration",
                        type=float,
                        default=None,
                        help="Max logging time in seconds")
    parser.add_argument("--delay",
                        dest="delay_sec",
                        type=float,
                        default=0.0,
                        help="Inter-scan delay in seconds (float allowed)")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_hdf5), exist_ok=True)
    run_extraction(
        args.printer_ip,
        args.stl_path,
        args.gcode_path,
        args.output_hdf5,
        args.sequence,
        args.duration,
        args.delay_sec
    )