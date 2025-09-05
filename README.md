# 3D-Print Data System with HDF5

## Table of Contents

- [1. Introduction](#1-introduction)
  - [1.1 Summary](#11-summary)
  - [1.2 Features](#12-features)
- [2. Getting Started](#2-getting-started)
  - [2.1 Requirements](#21-requirements)
  - [2.2 Configuration](#22-configuration)
  - [2.3 Installation](#23-installation)
  - [2.4 Usage](#24-usage)
- [3. Development](#3-development)
  - [3.1 System Architecture](#31-system-architecture)
    - [3.1.1 System Architecture Diagram](#311-system-architecture-diagram)
  - [3.2 Key Components](#32-key-components)
    - [3.2.1 First Component](#321-first-component)
- [4. Documentation](#4-documentation)
- [5. Release Planning](#5-release-planning)
- [6. Contributors](#6-contributors)
- [7. License](#7-license)
- [8. Status](#8-status)

## 1. Introduction

This project is a real-time telemetry extraction and logging tool for the Ultimaker S5 3D printer. It continuously polls the printer’s REST API to capture user-selected operational metrics—such as head position, bed temperature, nozzle temperatures, extrusion amount, and more—and organizes the data into a hierarchical HDF5 file for downstream analysis, visualization, or machine learning.

It requests various user-selected endpoints (head position, bed temperature, nozzle temps, material extruded, length remaining, etc.) and can optionally capture a camera snapshot at the start of each new layer. Data is organized into three main sections:

- /preprint: Stores metadata and embedded STL/G-code files
- /layers: Groups per layer (identified by layer height and extrusion stats), each containing time-series scans
- /Screenshots: JPEG datasets captured per layer

Users simply specify the printer’s IP, upload the STL and G-code, select desired endpoints, and start logging. The extractor thread segments data by layer, embeds raw files, and writes everything into one HDF5 archive.

If you’re unfamiliar with HDF5, it’s a binary, hierarchical format designed to store large datasets efficiently—see https://www.hdfgroup.org/solutions/hdf5/.

### 1.1 Summary

- Web/desktop UI for uploading STL and G-code
- Toggle capture of up to 12 telemetry endpoints
- Multi-threaded REST API polling for real-time data
- Automatic layer detection via extrusion Z-statistics
- Optional per-layer camera snapshots
- Hierarchical HDF5 output with raw file embedding
- Live log streaming via WebSocket

### 1.2 Features

- Endpoint Bitmask: Flexible toggling of metrics
- Threaded Polling: Maximizing API throughput
- Layer Segmentation: Accurate grouping of scans by print layer
- Embedded Files: Full STL/G-code in HDF5 for reproducibility
- Live on-page Log: WebSocket updates in browser or PyWebView window
- Standalone Desktop: Bundled via PyInstaller for one-click launch

## 2. Getting Started

### 2.1 Requirements

- Python 3.8+ (see requirements.txt):

  - Flask, Flask-SocketIO
  - requests, h5py, numpy
  - pywebview (desktop app)
- Git
- Ultimaker S5 on the same LAN with REST API enabled
- Web browser or desktop environment for PyWebView

### 2.2 Configuration

1. Clone the repository:

   - git clone https://github.com/immjunjie/CS3300-Project.git
   - cd CS3300-Project
2. Install dependencies:

   - pip install -r requirements.txt
3. Ensure these folders exist under backend:

   - uploads/ for STL/G-code uploads
   - Print_details_folder/ for saving HDF5 files
4. (Optional) Set app.secret_key in backend/app.py for secure sessions.

### 2.3 Installation

*screenshots or a video tutorial is recommended.*

### 2.4 Usage

*Note: Explain how to start using the project. Screenshots or a video tutorial are highly recommended.*

## 3. Development

*Note: Include documentation on how the project was developed, such as APIs, compatibility details, etc.*

### 3.1 System Architecture

*Note: Describe the overall system design and structure.*

#### 3.1.1 System Architecture Diagram

*Note: Include a visual representation of the system architecture, ideally with a diagram or screenshot.*

### 3.2 Key Components

#### 3.2.1 app.py

- Configuration & Initialization: Sets up the Flask application, static and template folders, secret key, and ensures upload/detail directories exist.
- Session & State Management: Stores uploaded file paths, printer IP, endpoint bitmask, and logging status across user sessions.
- Background Extraction Bridge: _bridge_extraction wraps run_extraction in a try/finally block and emits logging_stopped over Socket.IO when done.
- Flask Routes:

  - / (index): Renders the main UI, passing session state, file lists, and configuration to the template.
  - /set-printer: Validates connectivity to the specified printer IP and saves it to the session.
  - /start: Reads form inputs (files, duration, endpoints), assembles parameters, spawns the extractor thread, and updates remaining time.
  - /stop: Signals the extractor to stop, joins the thread, and resets logging state.
  - /upload (save files), /uploaded-files (list uploads), /delete-file/`<filename>` (remove uploads).
  - /download: Sends a selected HDF5 file as an attachment with a custom name.
- WebSocket Integration: Uses Flask-SocketIO to emit live telemetry events (new_log) and final status (logging_stopped).

#### 3.2.2 extractor.py

- convert_to_float(val)

  - Normalizes API‐returned values (numbers or small dicts) into floats for easy storage.
- extract_layer_height(gcode_path)

  - Parses the G-code comments (;LAYER_COUNT:, ;PRINT.SIZE.MIN.Z:, ;PRINT.SIZE.MAX.Z:) to compute the physical layer height.
- store_file_with_metadata(h5_group, file_path, dataset_name, description)

  - Embeds raw STL or G-code binaries into HDF5 with attributes for filesize and description.
- query(base_url, name, path)

  - Wraps a single REST call, returning (name, json); used by the thread pool to parallelize endpoint polling.
- run_extraction(printer_ip: str, stl_path: str, gcode_path: str, output_hdf5: str, sequence_bits: str, max_duration: float = None, delay_sec: float = 0.0, socketio=None)

  - Main extractor function.

    - Builds the HDF5 hierarchy (preprint, layers, Screenshots)
    - Uses a ThreadPoolExecutor to poll selected endpoints concurrently
    - Detects new layers by comparing current Z from head_pos to last Z + layer height
    - Creates per-layer groups (layer_XXXX) and per-scan subgroups (scan_YYYYYY) with datasets for each metric
    - Optionally captures camera snapshots via PrinterSnapshotter
    - Emits new_log events over Socket.IO for the live UI
    - follows the duration limit and inter-scan delay

#### 3.2.3 extract_snapshots.py

- PrinterSnapshotter class:

  - fetch_snapshot(): Pulls raw JPEG bytes from printer camera
  - capture_layer_snapshot(layer_number): Spawns a thread to fetch and save the snapshot
  - _capture_and_save_snapshot(...): Thread-safe write of image data into /Screenshots group with metadata

#### 3.2.4 filter_endpoints.py

filterMask(bit_sequence): Interprets a bitmask string where each bit controls whether a corresponding printer endpoint is included.

endpoints dictionary: Defines a mapping from descriptive keys (e.g., head_pos, bed_temp) to specific REST API paths.

Bitmask validation: (Commented out) logic verifies that the bit sequence length matches the number of available endpoints.

Filtering logic: Enumerates over endpoint keys, selecting only those with a '1' in the bit sequence, returning a dict of active endpoints.

#### 3.2.5 Simulator v2 Docker

Build image:

```bash
docker build -t sim-v2:dev -f simulator/v2/Dockerfile .
```

Run container (default maps host 8000 -> container 8000):

```bash
docker run -d --rm -p 8000:8000 --name simv2 sim-v2:dev
```

If 8000 is occupied, use another host port (e.g., 8001):

```bash
docker run -d --rm -p 8001:8000 --name simv2 sim-v2:dev
```

Health check:

```bash
curl -sS http://127.0.0.1:8000/api/v1/printer | jq .
```


## 4. Documentation

*Note: Provide additional detailed documentation.*

## 5. Release Planning

*Note: Outline the future direction and plans for the project.*

## 6. Contributors

- Immjunjie
- makapaka122333
- obudon
- SbZiggy123
- ScootBot

## 7. License

licensed under the MIT License. See LICENSE for details.

## 8. Status

Active development.
