#!/usr/bin/env python3

################################################################

import pdb
import sys
import os
import WriteNetcdf
import ReadNetcdf

"""
Module to calculate total optical depth from the AOD of the components.
At this point the following components are considered and
just summed up, if they are found:

od550ss
od550dust
od550so4
od550pom
od550bc
od550no3
od550bcpom
od550oa

###########################################################
Created 20170830 by Jan Griesfeller for Met Norway

last changed: see got log
###########################################################
"""



####################################################################

def CalcTotAOD(InData, OutVar='od550aer',DebugFlag=False, VerboseFlag=False):
	"""
	Routine to calculate total AOD from the components

	Parameters:
		InData:	dict of dicts containing the netcdf file date

	ReturnValue:
		OutData: dict with output data to be written to a netcdf file
		Error value (0: OK)
	"""

	#create output dict
	#use 1st input doct as template
	FirstVar=list(InData)[0]
	OutData=InData[FirstVar].copy()
	del OutData[FirstVar]
	if DebugFlag is True:
		pdb.set_trace()
	OutData[OutVar]={}
	OutData[OutVar]['DimVars']=InData[FirstVar][FirstVar]['DimVars']

	OutData[OutVar]['data']=InData[FirstVar][FirstVar]['data']
	OutData[OutVar]['Attributes']={}
	OutData[OutVar]['Attributes']['standard_name']='atmosphere_optical_thickness_due_to_ambient_aerosol_particles'
	OutData[OutVar]['Attributes']['units']='1'
	OutData[OutVar]['Attributes']['comment']='calculated by the aerocom-data-correction-tools from the variables '+','.join(InData.keys())

	for VarData in InData:	#variable loop
		if VarData == FirstVar: 
			continue
		OutData[OutVar]['data']=OutData[OutVar]['data']+InData[VarData][VarData]['data']

	if DebugFlag is True:
		pdb.set_trace()

	return OutData, 0

######################################################################################

def CalcTotAODForDir(ModelDir, Outdir=None, DebugFlag=False, VerboseFlag=False,OverwriteFlag=False):
	"""
	Routine to calculate the total aod from the AOD of the components
	present in a given model directory
	The model directory is searched for different time step sizes
	('daily','monthly','3hourly','hourly') and if data for the components 
	is found the total AOD is calculated.

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
	OutVar='od550aer'
	#use the following dict to tell if the Var was found in the model dir
	dict_InVars={}
	dict_InVars['od550ss']=''
	dict_InVars['od550dust']=''
	dict_InVars['od550so4']=''
	dict_InVars['od550pom']=''
	dict_InVars['od550bc']=''
	dict_InVars['od550no3']=''
	dict_InVars['od550bcpom']=''
	dict_InVars['od550oa']=''
	
	#minimum number of components to find before we calculate total oad
	MinNumberOfComponentsToFind=2

	#get variables in data files of ModelDir
	Vars=GetModelVars.GetModelVars(ModelDir)
	#Now check if the necessary variables are in general in the model dir
	#Does not include matching years
	VarsFound=0
	VarsToUseArr=[]
	for Var in dict_InVars:
		if Var in Vars:
			#dict_InVars[Var]=True
			VarsFound+=1
			VarsToUseArr.append(Var)
		
	#Error if no vars were found
	if VarsFound < MinNumberOfComponentsToFind:
		print('Error: model directory did not contain enough data to calculate total aod.')
		return FilesWritten, 1

	#Check for years
	dict_VarYears={}
	for VarToCheck in VarsToUseArr:
		dict_VarYears[VarToCheck]=GetModelYears.GetModelYears(ModelDir, Variable=VarToCheck)

	#now find the common elements
	CommonYears=list(set(dict_VarYears[VarsToUseArr[0]]).intersection(dict_VarYears[VarsToUseArr[1]]))
	for index in range(2,len(VarsToUseArr)):
		CommonYears=list(set(CommonYears).intersection(dict_VarYears[VarsToUseArr[index]]))

	#Now find the files for the different time step sizes, read them and calculate the total AOD
	for Year in CommonYears:
		for TSName in TimeStepStringsToWorkOn:
			FilesFound=[]
			dict_FilesFound={}
			for Variable in VarsToUseArr:
				#1st try phase 3 file naming scheme
				#aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc
				FilesFoundOfVar=glob.glob(ModelDir+'/*'+'_'.join([Variable,'*',Year, TSName])+'*.nc')
				#and then phase 2
				#aerocom.AATSR_ensemble.v2.6.daily.od550aer.2012.nc
				if len(FilesFoundOfVar) == 0:
					FilesFoundOfVar=glob.glob(ModelDir+'/*'+'.'.join([TSName,Variable,Year])+'*.nc')
				if len(FilesFoundOfVar) == 1:
					FilesFound.append(FilesFoundOfVar)
					dict_FilesFound[Variable]=FilesFoundOfVar[0]
				elif len(FilesFoundOfVar) > 1:
					print('Error: more than one matching file found.')
					pdb.set_trace()
				else:
					break
					
			#because glob.glob returns a list, FilesFound is a list of lists now
			#flatten it to a simple list using itertools
			FilesFound = list(itertools.chain.from_iterable(FilesFound))

			#we expect at least two files
			InData={}
			Dims={}
			if len(dict_FilesFound) >= MinNumberOfComponentsToFind:
				if VerboseFlag is True:
					print('Reading netcdf files...')
				for FileVar in dict_FilesFound:
					if VerboseFlag is True:
						print(dict_FilesFound[FileVar])
					InDataTemp, DimsTemp=ReadNetcdf.ReadNetcdf(dict_FilesFound[FileVar], VerboseFlag=VerboseFlag)
					InData[FileVar]=InDataTemp
					Dims[FileVar]=DimsTemp
					InDataTemp=None
					DimsTemp=None

				#Calculate total AOD
				if VerboseFlag is True:
					print('reading of netcdf files done')
					print('calculating '+OutVar+'...')
				OutData, ReturnFlag=CalcTotAOD(InData, DebugFlag=DebugFlag, VerboseFlag=VerboseFlag)
				#pdb.set_trace()
				if ReturnFlag == 0:
					OutFileName=FilesFound[0].replace(VarsToUseArr[0], OutVar)
					if Outdir is not None:
						#change outdir
						OutFileName=os.path.join(Outdir,os.path.basename(OutFileName))
					if VerboseFlag is True:
						print('Writing netcdf file '+OutFileName)
					if os.path.exists(OutFileName):
						if OverwriteFlag is False:
							print('Error: File exists and OverwriteFlag is not given: '+OutFileName)
							pdb.set_trace()
							continue
					print('Writing netcdf file '+OutFileName)
					WriteNetcdf.WriteNetcdf(OutFileName, Dims[list(dict_FilesFound)[0]], OutData)
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
	parser = argparse.ArgumentParser(description='CalcOd550: Calculate total AOD from components and save it into a new netcdf file. Done when at least one of the following component is found in the model directory: od550ss, od550dust, od550so4, od550pom, od550bc, od550bc, od550no3, od550bcpom.\n\n')
	#epilog='RI#eturns some general statistics')
	parser.add_argument("modeldir", help="model directory")
	#parser.add_argument("infilehigh", help="infile")
#
	#parser.add_argument("outfile", help="outfile")
	parser.add_argument("-v","--info", help="print some info since the operations may take some time", action='store_true')
	parser.add_argument("-d","--debug", help="debug mode; stop into python debug mode after the data reading", action='store_true')
	parser.add_argument("-o","--outdir", help="put the written files in this directory.")
	parser.add_argument("-O","--overwrite", help="overwrite exiting file. default is not to overwrite any file.",action='store_true')

	#parser.add_argument("-l", help="")

	args = parser.parse_args()

	if args.debug:
		dict_Param['debug']=args.debug
	else:
		dict_Param['debug']=False

	if args.overwrite:
		dict_Param['overwrite']=args.overwrite
	else:
		dict_Param['overwrite']=False

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

	FilesWritten=CalcTotAODForDir(dict_Param['modeldir'], Outdir=dict_Param['outdir'], DebugFlag=dict_Param['debug'], VerboseFlag=dict_Param['info'],OverwriteFlag=dict_Param['overwrite'])




