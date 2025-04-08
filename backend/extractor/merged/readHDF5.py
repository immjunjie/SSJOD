import h5py
import sys

file = sys.argv[1] if len(sys.argv) > 1 else "extract_info.hdf5" #<---- file name here

with h5py.File(file, "r") as f:
    def print_structure(g, indent=0):
        for key in g:
            if isinstance(g[key], h5py.Group):
                print(" " * indent + f"{key}/")
                print_structure(g[key], indent + 1)
            else:
                value = g[key][()]
                print(" " * indent + f"{key}: {value}")

    print_structure(f)