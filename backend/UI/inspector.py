import os
import sqlite3
import h5py
import sys

# Determine project root relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))

# Folder containing HDF5 files
details_folder = os.path.join(PROJECT_ROOT, 'Print_details_folder')
# Folder to store generated DBs
dbs_folder = os.path.join(PROJECT_ROOT, 'dbs')

# Table creation SQL
table_sql = '''
CREATE TABLE IF NOT EXISTS scans (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    layer                INTEGER,
    scan_num             INTEGER,
    timestamp            TEXT,
    position_x           REAL,
    position_y           REAL,
    position_z           REAL,
    bed_current_temp     REAL,
    bed_target_temp      REAL,
    bed_type             TEXT,
    current_nozzle_temp  REAL,
    target_nozzle_temp   REAL,
    time_spent_hot       REAL,
    printer_status       TEXT,
    material_extruded    REAL,
    led_status           REAL,
    jerk                 REAL,
    active_material      REAL,
    length_remaining     REAL,
    max_speed            REAL
);
'''

def decode_ds(ds):
    """Read a dataset, decode bytes to str if needed, else return numeric or array."""
    data = ds[()]
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data


def create_db(db_path):
    # Remove existing DB if present and recreate directory
    if not os.path.isdir(dbs_folder):
        os.makedirs(dbs_folder, exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(table_sql)
    conn.commit()
    return conn, cursor




def main():
    # Prompt for HDF5 filename
    hdf5_file = input("Enter HDF5 file to inspect (e.g. print_details_1.hdf5): ").strip()
    hdf5_path = os.path.join(details_folder, hdf5_file)
    if not os.path.isfile(hdf5_path):
        print(f"Error: '{hdf5_file}' not found in {details_folder}.")
        sys.exit(1)

    # Derive DB name: remove extension and prepend 'db_'
    base = os.path.splitext(hdf5_file)[0]
    db_name = f"db_{base}.db"
    db_path = os.path.join(dbs_folder, db_name)

    print(f"Creating database: {db_path}")
    conn, cursor = create_db(db_path)

    # Open HDF5 and insert scans
    with h5py.File(hdf5_path, 'r') as f:

        layers = f.get('layers')
        if layers is None:
            print("No 'layers' group found. Exiting.")
            conn.close()
            return

        for layer_name, layer_grp in layers.items():
            try:
                layer_idx = int(layer_name.split('_',1)[1])
            except:
                continue

            for scan_name, scan_grp in layer_grp.items():
                try:
                    scan_idx = int(scan_name.split('_',1)[1])
                except:
                    continue

                row = {
                    'layer': layer_idx,
                    'scan_num': scan_idx,
                    'timestamp': scan_grp.attrs.get('timestamp', '')
                }
                for ds_name, ds in scan_grp.items():
                    val = decode_ds(ds)
                    if ds_name == 'position':
                        x,y,z = (float(v) for v in (val if hasattr(val, '__len__') else [0,0,0]))
                        row['position_x'], row['position_y'], row['position_z'] = x,y,z
                    else:
                        if hasattr(val, '__len__') and len(val)==1:
                            val = val[0]
                        row[ds_name] = val


                cols = ', '.join(row.keys())
                placeholders = ', '.join('?' for _ in row)
                cursor.execute(f"INSERT INTO scans ({cols}) VALUES ({placeholders})", tuple(row.values()))

    conn.commit()
    conn.close()
    print(f"Import complete. Database saved at {db_path}")

if __name__ == '__main__':
    main()



