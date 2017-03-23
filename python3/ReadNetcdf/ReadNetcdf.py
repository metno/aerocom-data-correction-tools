#!/usr/bin/env python3

################################################################

import pdb
import os
from netCDF4 import Dataset

def ReadNetcdf(InFile, c_VarName=None, VerboseFlag=False, DebugFlag=False):
	# Routine to read a netcdf file entirely or just a list of variables into a nested dictionary.
	# The data is read 'as it is' and is not altered in any way.
	# There is a complementary routine called WriteNetcdf that can write the exact 
	# data structure to a netcdf file again
	#
	####################################################################################
	# Created 201703 by Jan Griesfeller for Met Norway
	#
	# Last update: see git log
	####################################################################################

	NcData = Dataset(InFile, "r")
	#Read the start year from the time attribute

	NetcdfData={}
	#Read global attributes 
	NetcdfData['GLOBAL']={}
	NetcdfData['GLOBAL']['Attributes']=NcData.__dict__
	#pdb.set_trace()
	#if VerboseFlag is True:
		#for GlobAttr in NcData.__dict__:
			#print(GlobAttr+': '+str(NcData.__dict__[GlobAttr]))


	#Read dimensions
	Dims={}
	for Dim in NcData.dimensions.keys():
		Dim=str(Dim)
		Dims[Dim]={}
		Dims[Dim]['isunlimited']=NcData.dimensions[Dim].isunlimited()
		Dims[Dim]['len']=NcData.dimensions[Dim].size

		if VerboseFlag is True:
			print(':'.join([Dim,str(Dims[Dim]['len'])]))

	#Read root variables 
	for Var in NcData.variables:
		if VerboseFlag is True:
			print('Name: '+Var)
		NetcdfData[Var]={}
		NetcdfData[Var]['data']=NcData[Var][:]
		NetcdfData[Var]['DimVars']=NcData[Var].dimensions
		NetcdfData[Var]['Attributes']=NcData[Var].__dict__
		if VerboseFlag is True:
			for Attr in NcData[Var].__dict__:
				print(':'.join([Attr,str(NcData[Var].__dict__[Attr])]))

	#There's some handling of the netcdf groups missing here, but I don't have any netcdf file using groups
	#handy for testing
	if DebugFlag is True:
		pdb.set_trace()
	NcData.close()
	return NetcdfData, Dims



