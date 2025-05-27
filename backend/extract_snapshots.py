import requests
import h5py
import numpy as np
from datetime import datetime
import threading
import os
CAMERA_TIMEOUT = float(os.getenv("CAMERA_TIMEOUT"))


class PrinterSnapshotter:
    """A class for fetching snapshots from a 3D printer camera and saving them in HDF5 file."""


    def __init__(self, camera_url, hdf5_filename):
        """
        Initializes the PrinterSnapshotter.
        Args:
            camera_url(str): The URL of the printer camera.
            hdf5_filename(str): Path to the HDF5 file where snaps will be stored.
        """
        self.camera_url = camera_url
        self.hdf5_filename = hdf5_filename
        self._lock = threading.Lock()  # Thread safety lock for HDF5 access

    def fetch_snapshot(self) -> None:
        """
        Fetches a snapshot from the printer's camera via URL

        Returns:
            bytes: upload raw image data if successful, None otherwise
        """
        try:
            response = requests.get(self.camera_url, timeout=CAMERA_TIMEOUT)
            if response.status_code == 200:
                return response.content
            else:
                print(f"Failed to fetch image. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Network error fetching snapshot: {e}")
        return None

    def capture_layer_snapshot(self, layer_number):
        """
        Captures a snapshot for a specific layer and saves it to the HDF5 file.
        This function should be called when a layer change is detected.

        Args:
            layer_number (int): The layer number for which to capture a snapshot
        """
        # Start snapshot capture in a separate thread to avoid blocking
        thread = threading.Thread(
            target=self._capture_and_save_snapshot,
            args=(layer_number,)
        )
        thread.daemon = True  # Make thread terminate when main program exits
        thread.start()

    def _capture_and_save_snapshot(self, layer_number):
        """
        Internal method to capture and save a snapshot for a specific layer.
        Args:
            layer_number (int): The layer number for this snapshot
        """
        # Fetch the snapshot
        snapshot_data = self.fetch_snapshot()
        if snapshot_data is None:
            print(f"Failed to capture snapshot for layer {layer_number}")
            return

        # Format layer number for consistent naming
        formatted_layer = f"{layer_number:04d}"

        # Save to HDF5 file with thread safety
        with self._lock:
            try:
                with h5py.File(self.hdf5_filename, 'a') as f:
                    # Make sure screenshots group exists
                    if 'Screenshots' not in f:
                        screenshots_grp = f.create_group('Screenshots')
                        screenshots_grp.attrs['format'] = 'JPEG'
                        screenshots_grp.attrs['count'] = 0
                    else:
                        screenshots_grp = f['Screenshots']

                    # Create dataset for this layer's snapshot
                    snap_name = f"screenshot_{formatted_layer}"
                    dset = screenshots_grp.create_dataset(
                        snap_name,
                        data=np.frombuffer(snapshot_data, dtype=np.uint8)
                    )

                    # Add metadata
                    dset.attrs['timestamp'] = datetime.now().isoformat()
                    dset.attrs['layer_number'] = layer_number

                    # Update count
                    count = screenshots_grp.attrs['count']
                    screenshots_grp.attrs['count'] = count + 1

                    print(f"Saved snapshot for layer {layer_number}")
            except Exception as e:
                print(f"Error saving snapshot to HDF5: {e}")