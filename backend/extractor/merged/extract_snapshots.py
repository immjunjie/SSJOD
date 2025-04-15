# extract_snapshots.py
import os

import requests
import h5py
import numpy as np
import time
from datetime import datetime
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

    def fetch_snapshot(self):
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

    def hdf_structure_init(self):
        with h5py.File(self.hdf5_file, 'a') as hdf:
            if 'images' not in hdf:
                dt = h5py.special_dtype(vlen=np.dtype('uint8'))
                hdf.create_dataset('images', shape=(0,), maxshape=(None,), dtype=dt)
                hdf.create_dataset('timestamps', shape=(0,), maxshape=(None,), dtype=h5py.string_dtype())

    def start_capturing(self, interval_range=(3,5), max_images=5, save_folder="printer_images"):
        """
        ///TEST version of the function with interval range to take snapshots when the printer in idle state
        /// and implemented method to store these snapshots in both ways (HDF5 and local in the same folder
        /// by creating a new folder printer_images

        Captures snapshots until max_images is reached.

        ARGS:
            to be continued...
        """
        os.makedirs(save_folder)
        self.hdf_structure_init()

        with h5py.File(self.hdf5_file, 'a') as hdf:
            count = hdf['images'].shape[0]

            while count < max_images:
                snapshot = self.fetch_snapshot()
                if snapshot is not None:
                    hdf['images'].resize((count + 1,))
                    hdf['images'][count] = snapshot

                    hdf['timestamps'].resize((count + 1,))
                    hdf['timestamps'][count] = datetime.now().isoformat()

                    # Save as .jpg for testing store snapshots
                    image_path = os.path.join(save_folder, f"snapshot_{count + 1}.jpg")
                    with open(image_path, 'wb') as f:
                        f.write(snapshot.tobytes())

                    hdf.flush() # If the program crashes - the data is saved up to the last successful snap.
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved image #{count + 1}")
                    count += 1

                else:
                    print("Skipping save due to fetch error.")

                time.sleep(np.random.uniform(*interval_range))


if __name__ == "__main__":
    #Constructor
    url = "http://143.239.73.224:8080/?action=snapshot"
    output_file = "printer_images.h5"

    #Initialize functions invocation
    snapper = PrinterSnapshotter(url, output_file)
    snapper.start_capturing()