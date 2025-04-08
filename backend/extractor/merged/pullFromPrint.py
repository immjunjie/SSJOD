import requests
import h5py
import time
import sys
from datetime import datetime

url='http://143.239.73.224/api/v1/printer'

if __name__=="__main__":
    count = 0
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
        while True:
            count += 1

            response=requests.get(url)
            if response.status_code==200:
                data=response.json()
                print("loop ran")

            else:
                sys.exit("no response from url")

            timestamp = datetime.now().isoformat()
            #   values from json
            bed_temp = data["bed"]["temperature"]["current"]
            nozzle_temp = data["heads"][0]["extruders"][0]["hotend"]["temperature"]["current"]
            head_pos = data["heads"][0]["position"]

            #   making the actual layer with data
            with h5py.File("extract_info.hdf5", "a") as f:
                #   layer itself
                layer_grp = layers_grp.create_group(f'layer: {count} timestamp: {timestamp}')

                #   Subgroups in each layer
                printer_head = layer_grp.create_group('printer_head')
                printer_head.create_dataset("temperature", data=nozzle_temp)
                
                #printer_head.create_dataset("position", data = head_pos)

                bedplate = layer_grp.create_group('bedplate')
                bedplate.create_dataset("temperature", data=bed_temp)
                
                layer_grp.attrs['print_speed'] = 50 + count  # mm/s example
                layer_grp.attrs['timestamp'] = f'2025-04-08T12:00:{count:02d}'

                #   Subgroups in each layer

            #   1 second pause before looping again
            time.sleep(1)

