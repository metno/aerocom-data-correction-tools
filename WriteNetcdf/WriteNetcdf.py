def WriteNetcdf(c_Filename, d_Dimensions, d_Data):
	# routine to write data to netcdf file
	# The dimensions and the actual data has to be submitted as dictionaries
	#
	# An example for the usage of this routine can be found in the file 
	# CreateStationFile.py in this directory
	#
	####################################################################################
	# Created 201602 by Jan Griesfeller for Met Norway
	#
	# Last update: 20160309	JG	Prepare code for repository
	####################################################################################
	from netCDF4 import Dataset, num2date, date2num, stringtochar, stringtoarr, chartostring
	import numpy as np
	import pdb

	#for time variable
	from datetime import datetime, timedelta

	rootgrp = Dataset(c_Filename, "w", format="NETCDF4")

	#create the dimensions first and keep the resulting opjects for possible later usage
	d_Dims={}
	for Dim in d_Dimensions:
		print('creating dimension ',Dim)
		if d_Dimensions[Dim]['len'] <= 0:
			d_Dims[Dim]= rootgrp.createDimension(Dim, None)
		else:
			d_Dims[Dim]= rootgrp.createDimension(Dim, d_Dimensions[Dim]['len'])

	#rootgrp.sync()
	d_Vars={}

	#create the data vars and keep the resulting objects for possible later usage
	for key in d_Data:
		if key == 'GLOBAL': continue	#that's the global attributes
		print('Writing data var',key)
		dtype=d_Data[key]['data'].dtype
		d_Vars[key]=rootgrp.createVariable(key,dtype, d_Data[key]['DimVars'])
		#print('adding attributes for var', key)
		if 'Attributes' in d_Data[key]:
			for attrib in d_Data[key]['Attributes']:
				print('Attrib:',attrib)
				#pdb.set_trace()
				d_Vars[key].setncattr(attrib,d_Data[key]['Attributes'][attrib])
		else:
			print('No attributes for var ',key,' defined')

		#Some debugging output
		#print('d_Vars[key].shape:',d_Vars[key].shape)
		#print('d_Data[key][data]:',d_Data[key]['data'].shape)
		
		#put the data into the variable
		d_Vars[key][:]=d_Data[key]['data']
	#rootgrp.sync()

	#set the global attributes
	for key in d_Data['GLOBAL']['Attributes']:
		#pdb.set_trace()
		#dummy=rootgrp.setncattr(key,stringtochar(d_Data['GLOBAL']['Attributes'][key]))
		dummy=rootgrp.setncattr(key,d_Data['GLOBAL']['Attributes'][key])

	
	rootgrp.close()	#write the file

#############################################################

