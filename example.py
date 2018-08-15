import argparse

import argparse_to_valohai_yaml as av

ap = argparse.ArgumentParser()
ap.add_argument('--fibble', type=float, help='model fibble', default=0.6)
ap.add_argument('--wabble', type=float, help='model wabble', default=0.2)
ap.add_argument('--check', type=bool, help='check model?')

print(av.dump_parameter_defs(ap))
