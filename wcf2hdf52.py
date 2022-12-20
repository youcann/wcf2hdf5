#!/usr/bin/env python3
import argparse
from tqdm import tqdm
import h5py

from WcfFile import WcfFile

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [files]...",
        description="Converts binary .wcf files from DataRay cameras to hdf5"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument("-o", "--outputfile")
    parser.add_argument('files', nargs='*')
    return parser


if __name__ == "__main__":
	parser = init_argparse()
	args = parser.parse_args()
	print(f"{len(args.files)} files selected.")
	if not args.outputfile:
		args.outputfile="output.hdf"
	print(f"Saving to {args.outputfile}")
	
	
	hf = h5py.File(args.outputfile, 'w')
	for filename in tqdm(args.files,unit='files'):
		currentWcf=WcfFile(filename)
		hf.create_dataset(filename, data=currentWcf.getAverageImage())
	hf.close()
	
	
	#from IPython import embed
	#embed()
