import requests
from dotenv import load_dotenv
load_dotenv() 

ACCESS_TOKEN = 'your_zenodo_token_here'
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# 1. Create a new deposition
res = requests.post("https://zenodo.org/api/deposit/depositions", json={}, headers=headers)
bucket_url = res.json()["links"]["bucket"]

# 2. Upload file to bucket
with open("your_file.hdf5", "rb") as f:
    res = requests.put(
        f"{bucket_url}/your_file.hdf5",
        data=f,
        headers=headers
    )

# 3. Add metadata and publish
metadata = {
    "metadata": {
        "title": "3D Printer Scan Data",
        "upload_type": "dataset",
        "description": "High-resolution scan logs from an Ultimaker 3D printer",
        "creators": [{"name": "Your Name"}]
    }
}
deposition_id = res.json()["id"]
res = requests.put(f"https://zenodo.org/api/deposit/depositions/{deposition_id}",
                   json=metadata,
                   headers=headers)

# 4. Publish
res = requests.post(f"https://zenodo.org/api/deposit/depositions/{deposition_id}/actions/publish",
                    headers=headers)