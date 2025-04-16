# extract_snapshots.py
import os
import requests
import h5py
import numpy as np
import time
from datetime import datetime

from fastapi.encoders import isoformat
from numpy import ndarray

from pullFromPrint import log_printer_data


class PrinterSnapshotter:
    """A class for fetching snapshots from a 3D printer camera and saving them in HDF5 file."""

    def __init__(self, url, hdf5_file):
        """
        Initializes the PrinterSnapshotter.
        ARGS:
            url(str): The URL of the printer camera.
            hdf5_file(str): Path to the HDF5 file where snaps will be stored.
        """
        self.url = url
        self.hdf5_file = hdf5_file

    def fetch_snapshot(self) -> ndarray | None:
        """
        Fetches a snapshot from the printer's camera via URL

        RETURNS:
            ndarray if the request success | None if the request failed.
        """
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                return np.frombuffer(response.content, dtype='uint8')
            else:
                print(f"Failed to fetch image. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Network error fetching snapshot: {e}")
        return None

    def hdf_structure_init(self) -> None:
        with h5py.File(self.hdf5_file, 'a') as hdf:
            if 'images' not in hdf:
                dt = h5py.special_dtype(vlen=np.dtype('uint8'))
                hdf.create_dataset('images', shape=(0,), maxshape=(None,), dtype=dt)
                hdf.create_dataset('timestamps', shape=(0,), maxshape=(None,), dtype=h5py.string_dtype())

    def save_snapshot_hdf(self, hdf, snapshot, current_count):
        """Save the snapshot's data and timestamps to HDF file
        ARGS:
            snapshot(ndarray):
            current_count(int):
        RETURN:
            Bool value. Success | Not success
        """
        try:
            hdf['images'].resize((current_count + 1,))
            hdf['images'][current_count] = snapshot

            hdf['timestamps'].resize((current_count + 1,))
            hdf['timestamps'][current_count] = datetime.now().isoformat()

            hdf.flush()
            return True
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to save snapshot to HDF5: {e}")
            return False

    def save_snapshot_locally(self, snapshot, save_folder, index):
        """Save snapshots as a .jpg file for manual inspection
        ARGS:
            :param snapshot: ndarray
            :param save_folder: str
            :param index: int
        RETURN:
            :return None
        """
        image_path = os.path.join(save_folder, f"snapshot_{index}.jpg")
        try:
            with open(image_path, "wb") as f:
                f.write(snapshot.tobytes())
        except IOError as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to save image locally: {e}")

    def monitor_layer_change(self, hdf, save_folder, current_count, last_recorded_layer):
        """Checking for layer changes and capture
        ARGS:
            :param save_folder: str
            :param current_count: int
            :param last_recorded_layer: int
        RETURN:
            :return None
            """

        while True:
            current_layer = log_printer_data()

            if not isinstance(current_layer, int):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No layer info retrieved. Retrying...")
                time.sleep(1)
                continue

            if current_layer != last_recorded_layer:
                snapshot = self.fetch_snapshot()

                if snapshot is not None:
                    if self.save_snapshot_hdf(hdf, snapshot, current_count):
                        self.save_snapshot_locally(snapshot, save_folder, current_count + 1)
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved image #{current_count + 1}")
                        last_recorded_layer = current_layer
                        current_count += 1
                else:
                    print("Snapshot fetch failed, skipping this layer.")
            time.sleep(1)  # Avoid spamming the printer

    def start_capturing(self, save_folder="printer_images"):
        """

        ARGS:
            :param save_folder: str.  Directory to save local .jpg snapshot fot easier check.
        RETURN
            :return None
        """
        os.makedirs(save_folder, exist_ok=True)
        self.hdf_structure_init()

        try:
            with h5py.File(self.hdf5_file, 'a') as hdf:
                current_count = hdf['images'].shape[0] #
                last_recorded_layer = -1 #Tracks last saved layer
                self.monitor_layer_change(hdf, save_folder, current_count, last_recorded_layer)
        except KeyboardInterrupt:
            print("Stopping snapshot capture")


if __name__ == "__main__":
    #Constructor
    url = "http://143.239.73.224:8080/?action=snapshot"
    output_file = "printer_images.h5"

    #Initialize functions invocation
    snapper = PrinterSnapshotter(url, output_file)
    snapper.start_capturing()
