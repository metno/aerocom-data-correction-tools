def WriteNetcdf(c_Filename, d_Dimensions, d_Data, VerboseFlag=False):
	"""
routine to write data to netcdf file

The dimensions and the actual data has to be submitted as dictionaries, 
Setting VerboseFlag adds some verbosity to the operations

An example for usage is below:


import WriteNetcdf
import numpy as np
from datetime import datetime, timedelta 
from netCDF4 import num2date, date2num

filename="test.nc"
ntime=1
nstat=1
ncharlen1=30
NetcdfData={}
NetcdfData['lat']={}
NetcdfData['lat']['data']=np.zeros((nstat),dtype='f4') 
NetcdfData['lat']['DimVars']=(['station'])
NetcdfData['lat']['Attributes']={}
NetcdfData['lat']['Attributes']['standard_name']='latitude'
NetcdfData['lat']['Attributes']['long_name']='latitude'
NetcdfData['lat']['Attributes']['units']='degrees_north'
NetcdfData['lat']['Attributes']['valid_range']=np.array([-90.,90.])
NetcdfData['lat']['Attributes']['axis']='Y'

NetcdfData['lon']={}
NetcdfData['lon']['data']=np.zeros((nstat),dtype='f4') 
NetcdfData['lon']['DimVars']=(['station'])
NetcdfData['lon']['Attributes']={}
NetcdfData['lon']['Attributes']['standard_name']='longitude'
NetcdfData['lon']['Attributes']['long_name']='longitude'
NetcdfData['lon']['Attributes']['units']='degrees_east'
NetcdfData['lon']['Attributes']['valid_range']=np.array([-180.,180.])
NetcdfData['lon']['Attributes']['axis']='X'

NetcdfData['station_elevation']={}
NetcdfData['station_elevation']['data']=np.zeros((nstat),dtype='f4')
NetcdfData['station_elevation']['DimVars']=(['station'])
NetcdfData['station_elevation']['Attributes']={}
NetcdfData['station_elevation']['Attributes']['standard_name']='height'
NetcdfData['station_elevation']['Attributes']['long_name']='vertical distance above the surface'
NetcdfData['station_elevation']['Attributes']['units']='m'
NetcdfData['station_elevation']['Attributes']['_FillValue'] = np.float(9.96920996838687e+36)

NetcdfData['time']={}
NetcdfData['time']['data']=np.arange(ntime,dtype='f8')
NetcdfData['time']['DimVars']=(['time'])
NetcdfData['time']['Attributes']={}
NetcdfData['time']['Attributes']['units']='days since 2001-01-01 00:00:00'
NetcdfData['time']['Attributes']['standard_name']='time'
NetcdfData['time']['Attributes']['calendar']='gregorian'
#This is to create a proper time axis
#Note that timedelta has weeks as biggest time step size
date_dummy = [datetime(2001,3,1)+n*timedelta(days=1) for n in range(NetcdfData['time']['data'].shape[0])]
NetcdfData['time']['data'] = date2num(date_dummy,units=NetcdfData['time']['Attributes']['units'],calendar=NetcdfData['time']['Attributes']['calendar'])

NetcdfData['time_bnds']={}
NetcdfData['time_bnds']['data']=np.zeros((nstat,2),dtype='f8')
NetcdfData['time_bnds']['DimVars']=(['time','bnds'])
NetcdfData['time_bnds']['Attributes']={}
NetcdfData['time_bnds']['Attributes']['units']='days since 2001-01-01 00:00:00'
NetcdfData['time_bnds']['Attributes']['standard_name']='time'
NetcdfData['time_bnds']['Attributes']['calendar']='gregorian'


NetcdfData['station']={}
NetcdfData['station']['data']=np.arange(nstat,dtype='i4')
NetcdfData['station']['DimVars']=['station']
NetcdfData['station']['Attributes']={}
NetcdfData['station']['Attributes']['units']='1'
NetcdfData['station']['Attributes']['standard_name']='Station_number'

NetcdfData['stationid']={}
NetcdfData['stationid']['data']=np.zeros([nstat,ncharlen1], dtype='S1')
#note that the string always has to be the size of ncharlen1
#and an array of char
NetcdfData['stationid']['data'][0,:]=list('This is a test station name'.ljust(ncharlen1,' '))
NetcdfData['stationid']['DimVars']=['station','charlen']
NetcdfData['stationid']['Attributes']={}
NetcdfData['stationid']['Attributes']['units']='1'
NetcdfData['stationid']['Attributes']['long_name']='Station number'

NetcdfData['od550aer']={}
NetcdfData['od550aer']['data']=np.zeros((ntime,nstat),dtype='f4')
NetcdfData['od550aer']['DimVars']=["time","station"]
NetcdfData['od550aer']['Attributes']={}
NetcdfData['od550aer']['Attributes']['units']='1'
NetcdfData['od550aer']['Attributes']['standard_name']='atmosphere_optical_thickness_due_to_aerosol'
NetcdfData['od550aer']['Attributes']['cell_methods'] = 'time: point'
NetcdfData['od550aer']['Attributes']['_FillValue'] = np.float(9.96920996838687e+36)


#These are the global attributes
NetcdfData['GLOBAL']={}
NetcdfData['GLOBAL']['Attributes']={}
NetcdfData['GLOBAL']['Attributes']['Convention']='CF-1.6'
NetcdfData['GLOBAL']['Attributes']['CreationContact']='jang@met.no'
NetcdfData['GLOBAL']['Attributes']['DatasetName']='test data set'
NetcdfData['GLOBAL']['Attributes']['CreationDate']="{:%Y-%m-%dT%H:%M:%S%z}".format(datetime.now())


#Dimensions
#set len to 0 if you want the dimension to be unlimited
d_Dimensions={}
d_Dimensions['charlen']={}
d_Dimensions['charlen']['len']=ncharlen1
d_Dimensions['lev']={}
d_Dimensions['lev']['len']=0
d_Dimensions['time']={}
d_Dimensions['time']['len']=0
d_Dimensions['station']={}
d_Dimensions['station']['len']=0
d_Dimensions['bnds']={}
d_Dimensions['bnds']['len']=2

#function call to write the data to a netcdf file
WriteNetcdf(filename, d_Dimensions, NetcdfData)

	"""
	# routine to write data to netcdf file
	# The dimensions and the actual data has to be submitted as dictionaries
	#
	# An example for the usage of this routine can be found in the file 
	# CreateStationFile.py in this directory
	#
	####################################################################################
	# Created 201602 by Jan Griesfeller for Met Norway
	#
	# Last update: see git log
	####################################################################################
	from netCDF4 import Dataset, num2date, date2num, stringtochar, stringtoarr, chartostring
	import numpy as np
	import pdb

	#for time variable
	from datetime import datetime, timedelta

	rootgrp = Dataset(c_Filename, "w", format="NETCDF4")

	#create the dimensions 
	d_Dims={}
	for Dim in d_Dimensions:
		if VerboseFlag is True:
			print('creating dimension ',Dim)
		if d_Dimensions[Dim]['len'] <= 0:
			d_Dims[Dim]= rootgrp.createDimension(Dim, None)
		else:
			d_Dims[Dim]= rootgrp.createDimension(Dim, d_Dimensions[Dim]['len'])

	#rootgrp.sync()
	d_Vars={}

	#create the data vars 
	for key in d_Data:
		if key == 'GLOBAL': continue	#that's the global attributes
		if VerboseFlag is True:
			print('Writing data var',key)
		dtype=d_Data[key]['data'].dtype
		d_Vars[key]=rootgrp.createVariable(key,dtype, d_Data[key]['DimVars'])
		
		if 'Attributes' in d_Data[key]:
			for attrib in d_Data[key]['Attributes']:
				if VerboseFlag is True:
					print('Attrib:',attrib)
				#pdb.set_trace()
				d_Vars[key].setncattr(attrib,d_Data[key]['Attributes'][attrib])
		else:
			if VerboseFlag is True:
				print('No attributes for var ',key,' defined')

		#put the data into the variable
		d_Vars[key][:]=d_Data[key]['data']

	#set the global attributes
	for key in d_Data['GLOBAL']['Attributes']:
		dummy=rootgrp.setncattr(key,d_Data['GLOBAL']['Attributes'][key])

	
	rootgrp.close()	#write the file

#############################################################

