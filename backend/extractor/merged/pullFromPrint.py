import requests
import h5py
import time
import sys
import numpy as np
from datetime import datetime

url='http://143.239.73.224/api/v1/printer'

if __name__=="__main__":
    layer = 0
    print("logging. press ctrl+c to stop")
    
    with h5py.File("extract_info.hdf5", "w") as f:
        #   Create main groups
        preprint_grp = f.create_group('preprint')
        layers_grp = f.create_group('layers')
        screenshots_grp = f.create_group('Screenshots')

        #   Create subgroups in preprint
        preprint_grp.create_group('STL')
        preprint_grp.create_group('Gcode')

        #   Example: adding metadata to preprint
        preprint_grp.attrs['printer_model'] = 'IDK'
        preprint_grp.attrs['material'] = 'Whatever'
        preprint_grp.attrs['layer_height'] =  1 # mm
        preprint_grp.attrs['resolution'] = 'Blue sk7'

        #   Screenshots group could hold images as datasets in future
        screenshots_grp.attrs['format'] = 'JPEG'
        screenshots_grp.attrs['count'] = 0  # To be updated when adding images

        #loop
        try:
            while True:
                layer += 1

                response=requests.get(url)
                if response.status_code==200:
                    data=response.json()

                else:
                    sys.exit("no response from url")

                timestamp = datetime.now().isoformat()
                #   values from json
                bed_current_temp = data["bed"]["temperature"]["current"]
                bed_target_temp = data["bed"]["temperature"]["target"]
                bed_type = data["bed"]["type"]

                head_pos = data["heads"][0]["position"]
                position_xyz = np.array([head_pos["x"], head_pos["y"], head_pos["z"]])

                nozzle_temp = data["heads"][0]["extruders"][0]["hotend"]["temperature"]["current"]
                material_extruded = data["heads"][0]["extruders"][0]["hotend"]["statistics"]["material_extruded"]
                time_spent_hot = data["heads"][0]["extruders"][0]["hotend"]["statistics"]["time_spent_hot"]

                status = data["status"]

            #   making the actual layer with data
                layer_grp = layers_grp.create_group(f'layer: {layer:04d} timestamp: {timestamp}')

            #   Subgroups in each layer
                printer_head = layer_grp.create_group('printer_head')

                printer_head.create_dataset("position", data=position_xyz)
                printer_head.create_dataset("X position", data=head_pos["x"])
                printer_head.create_dataset("Y position", data=head_pos["y"])
                printer_head.create_dataset("Z position", data=head_pos["z"])

                extruder = printer_head.create_group('extruder')
                extruder.create_dataset("nozzle temp", data=nozzle_temp)
                extruder.create_dataset("material extruded", data=material_extruded)

                bedplate = layer_grp.create_group('bedplate')
                bedplate.create_dataset("current temp", data=bed_current_temp)
                bedplate.create_dataset("target temp", data=bed_target_temp)
                bedplate.create_dataset("type", data=bed_type)

                session = layer_grp.create_group("session")
                session.create_dataset("status", data=status)
                session.create_dataset("time spent hot", data=time_spent_hot)

                layer_grp.attrs['print_speed'] = 50 + layer  # mm/s example
                layer_grp.attrs['timestamp'] = f'2025-04-08T12:00:{layer:02d}'

            #   1 second pause before looping again
                print('logged layer: ' + str(layer))
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("logging stopped")

