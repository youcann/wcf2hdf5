#!/usr/bin/env python3
import argparse
from tqdm import tqdm
import h5py

from WcfFile.WcfFile import WcfFile

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
		
		#create a group for the current file
		h5group=hf.create_group(filename)
		for attribute in currentWcf.getFileAttributes().items():
			h5group.attrs[attribute[0]]=repr(attribute[1])
		
		#create datasets for all images in the file
		for i,image in enumerate(currentWcf.getImages()):
			imagedset=h5group.create_dataset(f"Image{i}",data=image["imagedata"])
			for attribute in image["imageheader"]._asdict().items():
				imagedset.attrs[attribute[0]]=repr(attribute[1])

		#add a dataset containing the average image
		avgdset=h5group.create_dataset("Average", data=currentWcf.getAverageImage())
	hf.close()
