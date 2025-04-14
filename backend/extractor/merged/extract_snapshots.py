# extract_snapshots.py

import requests
import h5py
import numpy as np
import time
from datetime import datetime

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
            np.ndarray/None. Taking snapshot data as a NumPy array of uint8 or None if the request failed.
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
