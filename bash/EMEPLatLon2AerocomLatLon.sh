#!/bin/bash
# bash script to convert EMEP model data to aerocom standard
# the naming convention is according to aerocom phase 2 standard
# at this point
# depending on the input file name, this script will perform 
# a monthly or daily conversion

# it needs the file names vars_sorted.sh in the same directory as itsself

# This script is work in progress and not very sophisticated at this point

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

if [[ $# -lt 4 ]]
	then echo "usage: ${0} <input file> <model name> <data year> <output dir>"
	exit
fi

set -x

InFile="${1}"
ModelName="${2}"
DataYear="${3}"
OutDir="${4}"

TempFile="${OutDir}/temp.nc"

#ModelName="EMEP_Reporting_2016_3237"
# list of variables treated
# syntax of list elements: first part is aerocom name, second part is emep name
scriptpath=`realpath ${0}`
scriptdir=`dirname ${scriptpath}`
. ${scriptdir}/vars_sorted.sh

day_flag=0
month_flag=0
testfile=`basename ${InFile} .nc`
if [[ ${testfile} =~ .*month.* ]]
	then 
	month_flag=1
fi

day_flag=0
if [[ ${testfile} =~ .*day.* ]]
	then 
	day_flag=1
fi

if [ ${month_flag} -gt 0 ]
	then
   for arg in ${variablelist[*]}
      do echo ${arg}
      aerocomvar=`echo ${arg} | cut -d= -f1`
      emepvar=`echo ${arg} | cut -d= -f2`
      Tempfile="${OutDir}/"
      OutFile="${OutDir}/aerocom.${ModelName}.monthly.${aerocomvar}.${DataYear}.nc"
		if [ ${#aerocomvar} -lt 3 ]
			then exit
		fi
		#aerocom3_EMEP_rv4_33_Glob-CTRL_od550aer_Column_2010_monthly.nc
      #OutFile="${OutDir}/aerocom3_${ModelName}_${aerocomvar}_Column_${DataYear}_monthly.nc"
      #REMAP_EXTRAPOLATE='off' cdo remapdis,${GriddescriptionFile} -selname,${emepvar} ${InFile} ${OutFile}
      ncks -v ${emepvar} -O ${InFile} ${OutFile}
      exitcode=$?
      if [[ ${exitcode} -ne 0 ]] 
         then echo "exit code: ${exitcode}"
         #exit
      else 
         ncrename -v ${emepvar},${aerocomvar} ${OutFile}
      fi
   done
fi


if [ ${day_flag} -gt 0 ]
	then
	for arg in ${variablelist[*]}
		do echo ${arg}
		aerocomvar=`echo ${arg} | cut -d= -f1`
		emepvar=`echo ${arg} | cut -d= -f2`
		Tempfile="${OutDir}/"
		OutFile="${OutDir}/aerocom.${ModelName}.daily.${aerocomvar}.${DataYear}.nc"
		#REMAP_EXTRAPOLATE='off' cdo remapdis,${GriddescriptionFile} -selname,${emepvar} ${InFile} ${OutFile}
		ncks -v ${emepvar} -O ${InFile} ${OutFile}
		exitcode=$?
		if [[ ${exitcode} -ne 0 ]] 
			then echo "exit code: ${exitcode}"
			#exit
		else 
			ncrename -v ${emepvar},${aerocomvar} ${OutFile}
		fi
	done
	exit

	file1=${model}/renamed/aerocom.${model}.daily.sconcno3.${year}.nc
	file2=${model}/renamed/aerocom.${model}.daily.sconchno3.${year}.nc
	file3=${model}/renamed/aerocom.${model}.daily.sconctno3.${year}.nc
	if [ ! -f $file3 ] ; then
	if [ -f $file1 ] ; then
		 if [ -f $file2 ] ; then
		ncks -O -v sconcno3 $file1 $file3
		ncrename -v sconcno3,sconctno3 $file3
		ncks -A -v sconchno3 $file2 $file3
		ncap2 -O -s "sconctno3=sconctno3+sconchno3" $file3 $file3
		ncks -O -x -v sconchno3  $file3 $file3
		 fi    
	fi
	fi

	file1=${model}/renamed/aerocom.${model}.daily.sconcbcc.${year}.nc
	file2=${model}/renamed/aerocom.${model}.daily.sconcbcf.${year}.nc
	file3=${model}/renamed/aerocom.${model}.daily.sconcbc.${year}.nc
	if [ ! -f $file3 ] ; then
	if [ -f $file1 ] ; then
		 if [ -f $file2 ] ; then
		ncks -O -v sconcbcc $file1 $file3
		ncrename -v sconcbcc,sconcbc $file3
		ncks -A -v sconcbcf $file2 $file3
		ncap2 -O -s "sconcbc=sconcbc+sconcbcf" $file3 $file3
		ncks -O -x -v sconcbcf  $file3 $file3
		 fi    
	fi
	fi

	file1=${model}/renamed/aerocom.${model}.daily.sconcoac.${year}.nc
	file2=${model}/renamed/aerocom.${model}.daily.sconcoaf.${year}.nc
	file3=${model}/renamed/aerocom.${model}.daily.sconcoa.${year}.nc
	if [ ! -f $file3 ] ; then
	if [ -f $file1 ] ; then
		 if [ -f $file2 ] ; then
		ncks -O -v sconcoac $file1 $file3
		ncrename -v sconcoac,sconcoa $file3
		ncks -A -v sconcoaf $file2 $file3
		ncap2 -O -s "sconcoa=sconcoa+sconcoaf" $file3 $file3
		ncks -O -x -v sconcoaf  $file3 $file3
		 fi    
	fi
	fi

	file1=${model}/renamed/aerocom.${model}.daily.z3dmod.${year}.nc
	file2=${model}/renamed/aerocom.${model}.daily.z3d.${year}.nc
	if [ ! -f $file2 ] ; then
	if [ -f $file1 ] ; then
		ncks -A -v z topographyEECCAlonlat.nc $file1
		ncrename -v z3d,z3dmod $file1
		ncap2 -O -s "z3d=z3dmod+z" $file1 $file1
		ncks  -O -x -v z,z3dmod  $file1 $file2
		rm $file1
	fi
	fi

	IFS=${SAVEIFS}

	fileemep=${model}_sondes_${year}.nc
	fileaerocom1=${model}/renamed/aerocom3.${model}.vmro3.ModelLevelAtStation.${year}.hourly.nc
	fileaerocom2=${model}/renamed/aerocom3.${model}.pmid.ModelLevelAtStation.${year}.hourly.nc

	logdir='/metno/aerocom/work/logs/'
	logdate=`date +%Y%m%d%H%M%S`
	logfile="${logdir}emep-svn-test_${logdate}.log"

	ntimessonde=`cdo ntime ${fileaerocom1}`
	if [ $ntimessonde -lt 8760 ] ; then
		echo " number of time steps not correct in sondes file" $ntimessonde  >> $logfile
	fi


	if [ -f $fileemep ] ; then	
	#	if [ ! -f $fileaerocom1 ] ; then	
			ncks -O -v latitude,longitude,O3 $fileemep $fileaerocom1
			ncrename -v O3,vmro3 $fileaerocom1
			ncks -O -v latitude,longitude,p_mid $fileemep $fileaerocom2
			ncrename -v p_mid,pmid $fileaerocom2

		 case ${year} in
					1980|1984|1988|1992|1996|2000|2004|2008|2012)
							ndays=366;;
					19*|20*)
							ndays=365;;
		 esac

			if [ -f tmp.nc ] ; then
			 rm tmp.nc
			fi		
			cdo daymean $fileaerocom1 tmp.nc
			ncks -O -F -d time,1,$ndays tmp.nc ${fileaerocom1//hourly/daily}

			if [ -f tmp.nc ] ; then
			 rm tmp.nc
			fi		
			cdo daymean $fileaerocom2 tmp.nc
			ncks -O -F -d time,1,$ndays tmp.nc ${fileaerocom2//hourly/daily}

	#	fi
	fi


	exit
fi






IFS=$SAVEIFS

