import os
import requests

INVENIO_BASE_URL = os.getenv('INVENIO_BASE_URL', 'http://invenio.university.edu')
INVENIO_API_TOKEN = os.getenv('INVENIO_API_TOKEN', 'YOUR_API_TOKEN')


def create_record(metadata: dict) -> str:
    url = f"{INVENIO_BASE_URL}/api/records"
    headers = {
        'Authorization': f'Bearer {INVENIO_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {'metadata': metadata}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['id']  


def upload_file(record_id: str, file_path: str) -> dict:
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