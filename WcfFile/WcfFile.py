import struct
import numpy as np
from collections import namedtuple
from tqdm import tqdm

class WcfFile:
	def __init__(self,path):
		#open file at given path as binary file
		f=open(path,'rb')
		c=f.read()
		
		#Before trying to parse the data, check if the first bytes contain the "DRI" signature
		if not c[1:4].decode("UTF-8")[::-1]=="DRI":
			raise ValueError(f"The file {path} does not seem to contain the necessary signature. Is it broken?")
		
		#5592 bytes file header, only take first 60 bytes
		fileheaderStructure=[('Signature','4s'),
							('Type','i'),
							('Size','i'),
							('Images','i'),
							('ImagesSize','i'),
							('Version','40s')]
		Fileheader=namedtuple('Fileheader', [x[0] for x in fileheaderStructure])
		self.fileheader=Fileheader._make(struct.Struct(''.join([x[1] for x in fileheaderStructure])).unpack(c[0:60]))
		
		#Number of "Images" blocks of image data. Each block contains a 944 bytes header followed by the raw data (2 bytes/pixel)
		imageheaderStructure=[('Signature','4s'),
							('Type','i'),
							('Index','i'),
							('Beams','i'),
							('Size','i'),
							('Width','i'),
							('Height','i'),
							('CameraUpdateNumber','i'),
							('XpixelSize','d'),
							('YpixelSize','d'),
							('Bits','i'),
							('Key','i'),
							('Peak','i'),
							('Xoffset','i'),
							('Yoffset','i'),
							('Xlimit','i'),
							('Ylimit','i'),
							('OrientationDone','i'),
							('pPeakCenter','d'), #CPoint==double?
							('DefinedFluencePower','d'),
							('pUserCentroid_0','d'),
							('pUserCentroid_1','d'),
							('Centroid_0','d'),
							('Centroid_1','d'),
							('GeoCentroid_0','d'),
							('GeoCentroid_1','d'),
							('Baseline','d'),
							('UserCentroid_0','d'),
							('UserCentroid_1','d'),
							('GeoCenter_0','d'),
							('GeoCenter_1','d'),
							('PeakCentroid_0','d'),
							('PeakCentroid_1','d'),
							('Orientation','d'),
							('Ellipticity','d'),
							('MajorWidth','d'),
							('MinorWidth','d'),
							('MeanWidth','d'),
							('PeakFluencePower','d'),
							('BufferSize','i'),
							('iShutterSetting','i'),
							('sigCentroid_0','d'),
							('sigCentroid_1','d'),
							('IsoXInclusionRegionRadius_um','d'),
							('IsoYInclusionRegionRadius_um','d'),
							('Sigma4Ellip','d'),
							('Sigma4EllipAngle','d'),
							('IsoXWidth_um','d'),
							('IsoYWidth_um','d'),
							('ShutterSetting','d'),
							('BaselineStd','d'),
							('Gamma','d'),
							('MajorWidth_dXX_WinCamD','d'),
							('MinorWidth_dXX_WinCamD','d'),
							('dXX_WinCamD','d'),
							('A_dXX_WinCamD','d'),
							('P_dxx_WinCamD','d'),
							('IXX_WinCamD','d'),
							('Theta_XX_WinCamD','d'),
							('GaussianFit','d'),
							('ImageTemp_C','d'),
							('basic_Centroid_0','d'),
							('basic_Centroid_1','d'),
							('basic_Centroid_2','d'),
							('basic_Centroid_3','d'),
							('basic_Centroid_4','d'),
							('basic_Centroid_5','d'),
							('basic_Centroid_6','d'),
							('basic_Centroid_7','d'),
							('Busy','i'),
							('Minimum','i'),
							('NumberAveraged','i'),
							('UsedInAverage','i'),
							('WasFullResolution','i'),
							('PowerFactor','d'),
							('PowerLabel','20s'),
							('CorrectPower','d'),
							('InitialResult','d'),
							('PowerInDB','d'),
							('UseOldPowerData','i'),
							('LogSaved','i'),
							('MinLevel','i'),
							('AdcPeak','i'),
							('WasLogged','i'),
							('Camera','i'),
							('CaptureTime','q'), #check
							('GammaDone','i'),
							('Was_TwoD_Ssan','i'),
							('PeakToAverage','d'),
							('Ewidth_WinCamD','d'),
							('Was_WinCamDiv','i'),
							('SatPixels','i'),
							('FPS','d'),
							('EffectiveExposure','d'),
							('PowerInCentroidTarget','d'),
							('PlateauUniformity','d'),
							('PixelIntensity','i'),
							('CameraGain','d'),
							('MatrixIndex','i'),
							('PowerShutterSetting','d'),
							('IsM2Data','i'),
							('UcmM2Zlocation','d'),
							('UcamM2SlitToLense','d'),
							('UcmM2LenseToCameraFace','d'),
							('UcmM2LenseFocalLength','d'),
							('UcmM2Wavelength','d'),
							('M2Data','i'),
							('ConnectionType','i'),
							('AdcMinimum','i'),
							('LD','d'),
							('ZoDelta','d'),
							('Mfactor','d'),
							('CameraType','i'),
							('AdcAverage','i'),
							('PeakFound','i'),
							('iBaseline','i'),
							('uFIR_Gain','i'),
							('CTE_State','i'),
							('MeasurePeak','i'),
							('FullResolution','i'),
							('PowerInInclusionRegion','d'),
							('HyperCalGood','i'),
							('IlluminatedPixels','i'),
							('AdcOffset','i'),
							('Temp1','i'),
							('ShutterState','i'),
							('XSampleRate','i'),
							('LineLaserCaptureWidth','i'),
							('IntSpares_0','i'),
							('IntSpares_1','i'),
							('IntSpares_2','i'),
							('IntSpares_3','i'),
							('TotalPower','d'),
							('CentroidType','i'),
							('pCentroid_0','d'),
							('pCentroid_1','d'),
							('pGeoCentroid_0','d'),
							('pGeoCentroid_1','d'),
							('pPeakCentroid_0','d'),
							('pPeakCentroid_1','d'),
							('NewDate','i'),
							('ExtraLine','i')
							]
		Imageheader=namedtuple('Imageheader', [x[0] for x in imageheaderStructure])
		self.images=list()
		for i in tqdm(range(self.fileheader.Images), leave=False, unit='image(s)'):
			imageheader=Imageheader._make(struct.Struct(''.join([x[1] for x in imageheaderStructure])).unpack(c[5592:5592+struct.calcsize(''.join([x[1] for x in imageheaderStructure]))]))
			start=5592+i*(self.fileheader.ImagesSize+944)
			end=5592+i*(self.fileheader.ImagesSize+944)+imageheader.Width*imageheader.Height*2
			flatimage=np.array(struct.Struct(f'{imageheader.Width*imageheader.Height}H').unpack(c[start:end]))
			image=flatimage.reshape(imageheader.Width,imageheader.Height)
			self.images.append({"imageheader":imageheader,"imagedata": image})
		f.close()
			
	def getFileAttributes(self):
		return self.fileheader._asdict()
		
	def getImages(self):
		return self.images
			
	def getAverageImage(self):
		return np.mean(np.stack([x["imagedata"] for x in self.images],axis=0),axis=0)
