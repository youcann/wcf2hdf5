#!/usr/bin/env python3
import argparse
from tqdm import tqdm
import h5py

from WcfFile.WcfFile import WcfFile

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [files]...",
        description="Converts .wcf files from DataRay beam profiling cameras to the hdf5 format."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument("-o", "--outputfile")
    parser.add_argument('files', nargs='*')
    parser.add_argument('-a','--avgimage', action=argparse.BooleanOptionalAction,default=True,help="Calculates the averages of all images in a file")
    parser.add_argument('-s','--stdimage', action=argparse.BooleanOptionalAction,default=True,help="Calculates the std's of all images in a file")
    return parser

if __name__ == "__main__":
	parser = init_argparse()
	args = parser.parse_args()
	print(f"{len(args.files)} files selected...")
	if not args.outputfile:
		args.outputfile="output.hdf"
	print(f"Saving output to {args.outputfile}...")
	
	hf = h5py.File(args.outputfile, 'w')
	for filename in tqdm(args.files,unit='file(s)'):
		currentWcf=WcfFile(filename)
		
		#create a group for the current file
		h5group=hf.create_group(filename,track_order=True)
		for attribute in currentWcf.getFileAttributes().items():
			h5group.attrs[attribute[0]]=repr(attribute[1])
		
		#create datasets for all images in the file
		for i,image in enumerate(currentWcf.getImages()):
			imagedset=h5group.create_dataset(f"Image{i}",data=image["imagedata"],track_order=True,dtype='ushort')
			for attribute in image["imageheader"].items():
				imagedset.attrs[attribute[0]]=repr(attribute[1])

		#calculate avg and/or std image for the file
		if args.avgimage:
			h5group.create_dataset("Average", data=currentWcf.getAverageImage(),dtype='ushort')
		if args.avgimage:
			h5group.create_dataset("Standarddeviation", data=currentWcf.getStdImage(),dtype='ushort')
	hf.close()
