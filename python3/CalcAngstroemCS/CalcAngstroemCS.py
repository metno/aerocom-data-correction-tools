#!/usr/bin/env python3

################################################################

import pdb
import sys
import os
import WriteNetcdf
import ReadNetcdf
from CalcAngstroem import CalcAngstroemLL

####################################################################

def CalcAngstroemLLCS(AODLow, AODHigh, LambdaLow, LambdaHigh, DebugFlag=False):
	"""
	 low level routine  to calculate the angstroem exponent from optical depths at different wavelengths
	 using the formula (using 440nm and 870nm here)
	 f_ANG4487_AER=np.log(f_OD440_AER/f_OD870_AER)/np.log(0.87/.44)
	 which is the same this one
	 -1.0d*np.log(f_OD440_AER/f_OD870_AER)/np.log(0.44/.870)

	Parameters:
		AODLow:     numpy array with optical depths at the low vawelength
		AODHigh:    numpy array with optical depths at the high wavelength
		LambdaLow:  scalar with the low wavelength in nm
		LambdaHigh: scalar with the high wavelength in nm

	Return value:
		numpy array with the same length as AODLow containing the angstroem exponent
	
	"""
	import numpy as np

	AngstroemExponent=np.log(AODLow/AODHigh)/np.log(LambdaHigh/LambdaLow)
	if DebugFlag is True:
		pdb.set_trace()

	return AngstroemExponent

######################################################################################

def CalcAngstroemCS(InData, DebugFlag=False, VerboseFlag=False):
	"""
	Routine to select the appropriate low wavelength and high wavelength AODs to calculate 
	the Angstroem exponent using the low level routine CalcAngstroemLL

	Parameters:
		InData:	list of dictionaries containing data from different netcdf files

	ReturnValue:
		OutData: Low AOD InData elelemt with a key named ang447aer added.
					and the low aod dictionary element removed
		Error value (0: OK, 1, low AOD not found, 2: high AOD not found)
	"""

	#Maybe add a check if InData is a list, or not
	LambdaLow=-1
	LambdaHigh=-1
	for dict_Data in InData:
		#determine the low wavelength aod's name
		if LambdaLow < 0.:
			if 'od550csaer' in dict_Data.keys():
				AODLow=dict_Data['od550csaer']
				OutData=dict_Data
				del OutData['od550csaer']
				LambdaLow=.55
				VarLowStr='od550csaer'
			elif 'od440csaer' in dict_Data.keys():
				AODLow=dict_Data['od440csaer']
				OutData=dict_Data
				del OutData['od440csaer']
				LambdaLow=.44
				VarLowStr='od440csaer'
			if LambdaLow > 0. and VerboseFlag is True:
				print('Found low data')


		#determine the high wavelength aod's name
		if LambdaHigh < 0.:
			if 'od825csaer' in dict_Data.keys():
				AODHigh=dict_Data['od825csaer']
				del dict_Data['od825csaer']
				LambdaHigh=.825
				VarHighStr='od825csaer'
			elif 'od865csaer' in dict_Data.keys():
				AODHigh=dict_Data['od865csaer']
				del dict_Data['od865csaer']
				LambdaHigh=.865
				VarHighStr='od865csaer'
			elif 'od870csaer' in dict_Data.keys():
				AODHigh=dict_Data['od870csaer']
				del dict_Data['od870csaer']
				LambdaHigh=.87
				VarHighStr='od870csaer'
			if LambdaHigh > 0. and VerboseFlag is True:
				print('Found high data')
			
		if LambdaLow > 0. and LambdaHigh > 0:
			break

	if LambdaLow > 0. and LambdaHigh > 0:
		OutData['ang4487csaer']={}
		OutData['ang4487csaer']['DimVars']=AODLow['DimVars']

		OutData['ang4487csaer']['data']=CalcAngstroemLL(AODLow['data'], AODHigh['data'], LambdaLow, LambdaHigh)
		OutData['ang4487csaer']['Attributes']={}
		OutData['ang4487csaer']['Attributes']['standard_name']='angstrom_exponent_of_ambient_aerosol_in_air'
		OutData['ang4487csaer']['Attributes']['units']='1'
		OutData['ang4487csaer']['Attributes']['comment']='calculated by the aerocom-data-correction-tools from the variables '+VarLowStr+' and '+VarHighStr

		if DebugFlag is True:
			pdb.set_trace()

		return OutData, 0
	else:
		return None, 1

######################################################################################

def CalcAngstroemCSForDir(ModelDir, Outdir=None, DebugFlag=False, VerboseFlag=False):
	"""
	Routine to calculate the clear sky angstroem exponent from the data 
	present in a given model directory
	The model directory is searched for different time step sizes
	('daily','monthly','3hourly','hourly') and if data for a low and a high
	wavelength is found the angstroem exponent is calculated.

	Parameters:
		ModelDir:	model directory (directory where the data files reside).
		Outdir:		Optional output directory. If not given, model dir is used.


	Needs also parts from the aerocom-tool-automation package!
	"""
	import GetModelVars
	import GetModelYears
	import collections
	import glob
	import re
	import itertools

	TimeStepStringsToWorkOn=['daily','monthly','3hourly','hourly']
	FilesWritten=[]
	OutVar='ang4487csaer'
	#get variables in data files of ModelDir
	Vars=GetModelVars.GetModelVars(ModelDir)
	#Now check if the necessary variables are in general in the model dir
	#Does not include matching years
	LambdaLowFlag=False
	LambdaHighFlag=False
	VarsToUseArr=[]
	#determine the low wavelength aod's name
	if LambdaLowFlag is False:
		if 'od440csaer' in Vars:
			LambdaLowFlag=True
			VarsToUseArr.append('od440csaer')
		elif 'od550csaer' in Vars:
			LambdaLowFlag=True
			VarsToUseArr.append('od550csaer')
		if LambdaLowFlag is True and VerboseFlag is True:
			print('Found low data')

	#determine the high wavelength aod's name
	if LambdaHighFlag is False:
		if 'od870csaer' in Vars:
			LambdaHighFlag=True
			VarsToUseArr.append('od870csaer')
		elif 'od865csaer' in Vars:
			LambdaHighFlag=True
			VarsToUseArr.append('od865csaer')
		elif 'od825csaer' in Vars:
			LambdaHighFlag=True
			VarsToUseArr.append('od825csaer')
		if LambdaHighFlag is True and VerboseFlag is True:
			print('Found high data')
			
	#Error if no vars were found
	if LambdaLowFlag is False or LambdaHighFlag is False:
		print('Error: model directory did not contain data for all necessary input variables')
		return FilesWritten, 1

	#Check for years
	dict_VarYears={}
	for VarToCheck in VarsToUseArr:
		dict_VarYears[VarToCheck]=GetModelYears.GetModelYears(ModelDir, Variable=VarToCheck)

	#now find the common elements
	CommonYears=list(set(dict_VarYears[VarsToUseArr[0]]).intersection(dict_VarYears[VarsToUseArr[1]]))

	#Now find the files for the different time step sizes, read them and calculate the Angstroem exponent
	for Year in CommonYears:
		for TSName in TimeStepStringsToWorkOn:
			FilesFound=[]
			for Variable in VarsToUseArr:
				#1st try phase 3 file naming scheme
				#aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc
				FilesFoundOfVar=glob.glob(ModelDir+'/*'+'_'.join([Variable,'*',Year, TSName])+'*.nc')
				#and then phase 2
				#aerocom.AATSR_ensemble.v2.6.daily.od550aer.2012.nc
				if len(FilesFoundOfVar) == 0:
					FilesFoundOfVar=glob.glob(ModelDir+'/*'+'.'.join([TSName,Variable,Year])+'*.nc')

				if len(FilesFoundOfVar) > 0:
					FilesFound.append(FilesFoundOfVar)
				else:
					break
					
			#because glob.glob returns a list, FilesFound is a list of lists now
			#flatten it to a simple list using itertools
			FilesFound = list(itertools.chain.from_iterable(FilesFound))

			#we expect at least two files, one for the low and the high wavelength AOD
			InData=[]
			Dims=[]
			if len(FilesFound) >= 2:
				if VerboseFlag is True:
					print('Reading netcdf files...')
				for FileToLoad in FilesFound:
					if VerboseFlag is True:
						print(FileToLoad)
					InDataTemp, DimsTemp=ReadNetcdf.ReadNetcdf(FileToLoad, VerboseFlag=False)
					InData.append(InDataTemp)
					Dims.append(DimsTemp)
					InDataTemp=None
					DimsTemp=None

				#Calculate Angstroem exponent 
				if VerboseFlag is True:
					print('reading of netcdf files done')
					print('calculating '+OutVar+'...')
				OutData, ReturnFlag=CalcAngstroemCS(InData, DebugFlag=False, VerboseFlag=False)
				if ReturnFlag == 0:
					OutFileName=FilesFound[0].replace(VarsToUseArr[0], OutVar)
					if Outdir is not None:
						#change outdir
						OutFileName=os.path.join(Outdir,os.path.basename(OutFileName))
					if VerboseFlag is True:
						print('Writing netcdf file '+OutFileName)
					WriteNetcdf.WriteNetcdf(OutFileName, Dims[0], OutData)
					FilesWritten.append(OutFileName)
			else:
				if VerboseFlag is True:
					print('INFO: No files for the combo '+','.join([Variable,Year, TSName])+' found.')

	if DebugFlag is True:
		pdb.set_trace()

	return FilesWritten, 0

######################################################################################

if __name__ == '__main__':
	import argparse

	dict_Param={}
	parser = argparse.ArgumentParser(description='CalcAngstroemCS: Calculate clear sky angstroem exponent and save it into a new netcdf file\n\n')
	#epilog='RI#eturns some general statistics')
	parser.add_argument("modeldir", help="model directory to make the ang4487aer calculation with")
	#parser.add_argument("infilehigh", help="infile")
#
	#parser.add_argument("outfile", help="outfile")
	parser.add_argument("-v","--info", help="print some info since the operations may take some time", action='store_true')
	parser.add_argument("-d","--debug", help="debug mode; stop into python debug mode after the data reading", action='store_true')
	parser.add_argument("-o","--outdir", help="put the written files in this directory. For simpler debugging.")
	#parser.add_argument("-l", help="")

	args = parser.parse_args()

	if args.debug:
		dict_Param['debug']=args.debug
	else:
		dict_Param['debug']=False

	if args.info:
		dict_Param['info']=args.info
	else:
		dict_Param['info']=False

	if args.modeldir:
		dict_Param['modeldir']=args.modeldir
	else:
		dict_Param['modeldir']=False

	if args.outdir:
		if os.path.isdir(args.outdir) is False:
			sys.stderr.write('Error: outdir does not exist. Exiting.')
			sys.exit(1)
		dict_Param['outdir']=args.outdir
	else:
		dict_Param['outdir']=False

	FilesWritten=CalcAngstroemCSForDir(dict_Param['modeldir'], Outdir=dict_Param['outdir'], DebugFlag=dict_Param['debug'], VerboseFlag=dict_Param['info'])




