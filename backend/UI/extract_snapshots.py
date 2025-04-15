# extract_snapshots.py
import os
from typing import Any

import requests
import h5py
import numpy as np
import time
from datetime import datetime

from numpy import ndarray, dtype

######## from pullFromPrint import log_printer_data


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

    def fetch_snapshot(self) -> ndarray[tuple[int, ...], dtype[Any]] | None:
        """
        Fetches a snapshot from the printer's camera via URL

        RETURNS:
            np.ndarray/None. Taking snapshot data as a NumPy array of uint8 or
            None if the request failed.
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

    def start_capturing(self, save_folder="printer_images"):
        """
        ///TEST version of the function with interval range to take snapshots when the printer in idle state
        /// and implemented method to store these snapshots in both ways (HDF5 and local in the same folder
        /// by creating a new folder printer_images

        Captures snapshots until max_images is reached.

        ARGS:
            save_folder(str): Directory to save local .jpg snapshot fot easier check.
        RETURN
            :rtype: object
        """
        os.makedirs(save_folder)
        self.hdf_structure_init()

        with h5py.File(self.hdf5_file, 'a') as hdf:
            count = hdf['images'].shape[0] #
            last_recorded_layer = -1 #Tracks last saved layer

            while True:
                #Query the printer's current layer
                current_layer = log_printer_data()

                #If no valid layer
                if not isinstance(current_layer, int):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] No layer info retrieved. Retrying...")
                    time.sleep(1)
                    continue

                #If layer is changed invoke a function to take a snapshot
                if current_layer != last_recorded_layer:
                    snapshot = self.fetch_snapshot()

                    if snapshot is not None:
                        #Add the snapshot to HDF5
                        hdf['images'].resize((count + 1,))
                        hdf['images'][count] = snapshot
                        #Save timestamps
                        hdf['timestamps'].resize((count + 1,))
                        hdf['timestamps'][count] = datetime.now().isoformat()

                        # Save snapshots as .jpg for manual inspection
                        image_path = os.path.join(save_folder, f"snapshot_{count + 1}.jpg")
                        with open(image_path, 'wb') as f:
                            f.write(snapshot.tobytes())

                        # If the program crashes - the data is saved up to the last successful snap.
                        try:
                            hdf.flush()
                        except Exception as e:
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to flush HDF5 data: {e}")

                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved image #{count + 1}")

                        last_recorded_layer = current_layer
                        count += 1

                    else:
                        print("Snapshot fetch failed, skipping this layer.")

                #Prevent of spamming the printer with requests
                time.sleep(1)


if __name__ == "__main__":
    #Constructor
    url = "http://143.239.73.224:8080/?action=snapshot"
    output_file = "printer_images.h5"

    #Initialize functions invocation
    snapper = PrinterSnapshotter(url, output_file)
    snapper.start_capturing()
