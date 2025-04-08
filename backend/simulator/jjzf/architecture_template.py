import h5py
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

total_layers = 10

with h5py.File('3d_print_template', 'w') as f:

    #   Create main groups
    preprint_grp = f.create_group('preprint')
    layers_grp = f.create_group('layers')
    screenshots_grp = f.create_group('Screenshots')

    #   Create subgroups in preprint
    preprint_grp.create_group('STL')
    preprint_grp.create_group('Gcode')

    #   Example: adding metadata to preprint
    preprint_grp.attrs['printer_model'] = 'Ultimaker'
    preprint_grp.attrs['material'] = 'Whatever'
    preprint_grp.attrs['layer_height'] =  1 # mm
    preprint_grp.attrs['resolution'] = 'xxx'

    #   Add metadata to layers group
    layers_grp.attrs['total_layers'] = total_layers

    #   Create dynamic layer groups
    for layer_num in range(1, total_layers + 1):
        layer_grp = layers_grp.create_group(f'layer {layer_num}')
        layer_grp.attrs['timestamp'] = current_time 

        #   Subgroups in each layer
        layer_grp.create_group('printer_head')
        layer_grp.create_group('bedplate')

    #   Screenshots group could hold images as datasets in future
    screenshots_grp.attrs['format'] = 'JPEG'
    screenshots_grp.attrs['count'] = 0  # To be updated when adding images

print("HDF5 file created successfully!")