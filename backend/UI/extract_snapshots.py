# extract_snapshots.py
import os
import requests
import h5py
import numpy as np
import time
from datetime import datetime


class PrinterSnapshotter:
    """A class for fetching snapshots from a 3D printer camera and saving them in HDF5 file."""

    def __init__(self, url_snapshot, hdf5_file):
        """
        Initializes the PrinterSnapshotter.
        ARGS:
            url_snapshot(str): The URL of the printer camera.
            hdf5_file(str): Path to the HDF5 file where snaps will be stored.
        """
        self.url_snapshot = url_snapshot
        self.hdf5_file = hdf5_file

    def fetch_snapshot(self) -> ndarray | None:
        """
        Fetches a snapshot from the printer's camera via URL

        RETURNS:
            ndarray if the request success | None if the request failed.
        """
        try:
            response = requests.get(self.url_snapshot, timeout=10)
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
            count = hdf.attrs.get('count', 0)
            hdf['images'].resize((current_count + 1,))
            hdf['images'][current_count] = snapshot

            hdf['timestamps'].resize((current_count + 1,))
            hdf['timestamps'][current_count] = datetime.now().isoformat()

            hdf.attrs['count'] = count + 1
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


