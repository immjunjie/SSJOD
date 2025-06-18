import os
import requests

# Configuration: set via environment variables or hardcode for testing
INVENIO_BASE_URL = os.getenv('INVENIO_BASE_URL', 'http://invenio.university.edu')
INVENIO_API_TOKEN = os.getenv('INVENIO_API_TOKEN', 'YOUR_API_TOKEN')


def create_record(metadata: dict) -> str:
    """
    Create a new Invenio record with the given metadata.

    Returns the new record's PID (record ID).
    """
    url = f"{INVENIO_BASE_URL}/api/records"
    headers = {
        'Authorization': f'Bearer {INVENIO_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {'metadata': metadata}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['id']  # or data['pid_value'] depending on setup


def upload_file(record_id: str, file_path: str) -> dict:
    """
    Upload the HDF5 file to the created Invenio record draft and publish it.

    - record_id: the PID returned by create_record
    - file_path: path to the .hdf5 file
    """
    filename = os.path.basename(file_path)
    # Upload file to draft
    files_url = f"{INVENIO_BASE_URL}/api/records/{record_id}/draft/files/{filename}"
    headers = {'Authorization': f'Bearer {INVENIO_API_TOKEN}'}
    with open(file_path, 'rb') as fp:
        files = {'file': (filename, fp, 'application/octet-stream')}
        put_resp = requests.put(files_url, files=files, headers=headers)
    put_resp.raise_for_status()

    # Publish the draft
    publish_url = f"{INVENIO_BASE_URL}/api/records/{record_id}/draft/actions/publish"
    publish_resp = requests.post(publish_url, headers=headers)
    publish_resp.raise_for_status()
    return publish_resp.json()