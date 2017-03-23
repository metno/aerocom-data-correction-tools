#!/bin/bash

#Sample script of how to create a correct time variable using bash
#and nco (http://nco.sourceforge.net/)
#Note that you can get the time in human readable format using ncdump
#if the netcdf library is compiled with udunits2 support using the -t switch
#e.g. 
#ncdump -v time -t test.nc
#
#should give you something like this after the header information:
#
#data:
#
 #time = "2010-01-01", "2010-01-02", "2010-01-03", "2010-01-04", "2010-01-05", 
    #"2010-01-06", "2010-01-07", "2010-01-08", "2010-01-09", "2010-01-10", 
    #"2010-01-11", "2010-01-12", "2010-01-13", "2010-01-14", "2010-01-15", 
    #"2010-01-16", "2010-01-17", "2010-01-18", "2010-01-19", "2010-01-20", 
    #"2010-01-21", "2010-01-22", "2010-01-23", "2010-01-24", "2010-01-25", 
    #"2010-01-26", "2010-01-27", "2010-01-28", "2010-01-29", "2010-01-30", 
    #"2010-01-31", "2010-02-01", "2010-02-02", "2010-02-03", "2010-02-04", 
    #"2010-02-05", "2010-02-06", "2010-02-07", "2010-02-08", "2010-02-09", 
    #"2010-02-10", "2010-02-11", "2010-02-12", "2010-02-13", "2010-02-14", 

set -x
infile='../exampledata/htap2_EMEP_rv48_BASE_vmrso2_ModelLevelAtStations_2010_daily.nc'
outfile='test.nc'
year='2010'

ncap2 -o ${outfile} -O -s 'time=array(0f,1.,$time)' ${infile}
ncatted -O -a "units,time,o,c,days since ${year}-1-1 0:0:0" ${outfile}
ncatted -O -a 'calendar,time,o,c,standard' ${outfile}
ncatted -O -a 'long_name,time,o,c,time' ${outfile}


