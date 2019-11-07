#!/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

#workdirremote='/global/work/mifahf/DO_AEROCOM/'
#workdirremote2='/work/mifahf/DO_AEROCOM/'


#model=${1}
#year=${2}
#projection=${3}

#InputFileName=${model}_day_${year}.nc
#LatLonInFileName=${model}_day_${year}latlon.nc

#if [ "${projection}" = "lonlat" ]
#then
#echo "lon lat grid"
#LatLonInFileName=$InputFileName
#else
#echo "Non regular lon lat grid"
#fi


#GriddescriptionFile='/lustre/storeB/project/aerocom/bin/EECCA50PS.griddes'

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
variablelist=(\
'sconcpm10=SURF_ug_PM10' \
'sconcpm10=SURF_ug_PM10rh50' \
'sconcpm10=SURF_ug_PM10_rh50' \
'sconcpm25=SURF_ug_PM25' \
'sconcpm25=SURF_ug_PM25rh50' \
'sconcpm25=SURF_ug_PM25_rh50' \
'sconcso2=SURF_ug_SO2' \
'sconcso2=SURF_ugS_SO2' \
'sconcso4=SURF_ug_SO4' \
'sconcso4=SURF_ugS_SO4' \
'wetso4=WDEP_SOX' \
'sconcnh3=SURF_ug_NH3' \
'sconcnh3=SURF_ugN_NH3' \
'sconcnh4=SURF_ug_NH4_F' \
'sconcnh4=SURF_ugN_NH4_F' \
'wetrdn=WDEP_RDN' \
'sconcrdn=SURF_ugN_RDN' \
'sconcno=SURF_ug_NO' \
'sconcno=SURF_ugN_NO' \
'sconcno2=SURF_ug_NO2' \
'sconcno2=SURF_ugN_NO2' \
'sconchno3=SURF_ug_HNO3' \
'sconchno3=SURF_ugN_HNO3' \
'sconcno3=SURF_ug_TNO3' \
'wetoxn=WDEP_OXN' \
'vmro3max=SURF_MAXO3' \
'vmro3=SURF_ppb_O3' \
'vmro32m=SURF_2MO3' \
'sconcss=SURF_ug_SS' \
'sconcaeroh2o=SURF_PM25water' \
'emidust=DUST_flux' \
'od550aer=AOD' \
'od350aer=AOD_350nm' \
'od550aer=AOD_550nm' \
'od440aer=AOD_440nm' \
'od870aer=AOD_870nm' \
'od550ss=AOD_SS_550nm' \
'od550so4=AOD_SO4_550nm' \
'od550no3=AOD_TNO3_550nm' \
'od550nh4=AOD_NH4_F_550nm' \
'od550oa=AOD_OM25_550nm' \
'od550bc=AOD_EC_550nm' \
'od550dust=AOD_DUST_550nm' \
'od550oa=AOD_OM25_550nm' \
'od550lt1aer=AOD_PMFINE_550nm'
'absc550dryaer=AbsCoef' \
'ec550aer=ExtinSurf' \
'ec3503Daer=EXT_350nm' \
'ec5503Daer=EXT_550nm' \
'ec5503Daer=D3_ExtinCoef' \
'sconcdust=SURF_ug_DUST' \
'sconcbcf=SURF_ug_ECFINE' \
'sconcbcc=SURF_ug_ECCOARSE' \
'sconcoaf=SURF_ug_PART_OM_F' \
'sconcoac=SURF_ug_OMCOARSE' \
'z3d=D3_Zmid' \
'loadso2=COLUMN_SO2_kmax' \
'loadso4=COLUMN_SO4_kmax' \
'loadss=COLUMN_SS_kmax' \
'loadbc=COLUMN_EC_kmax' \
'loadoa=COLUMN_OM25_kmax' \
'loaddust=COLUMN_DUST_kmax' \
'loadno3=COLUMN_TNO3_kmax' \
'loadnh4=COLUMN_NH4_F_kmax' \
'wetso2=WDEP_SO2' \
'wetso4=WDEP_SO4' \
'wetbc=WDEP_EC' \
'wetoa=WDEP_OM25' \
'wetss=WDEP_SS' \
'wetdust=WDEP_DUST' \
'wetno3=WDEP_TNO3' \
'wetnh4=WDEP_NH4_f' \
'dryso2=DDEP_SO2' \
'dryso4=DDEP_SO4' \
'drybc=DDEP_EC' \
'dryoa=DDEP_OM25' \
'dryss=DDEP_SS' \
'drydust=DDEP_DUST' \
'dryno3=DDEP_TNO3' \
'drynh4=DDEP_NH4_f' \
'mmrso2=D3_mmr_SO2' \
'mmrso4=D3_mmr_SO4' \
'mmrbc=D3_mmr_EC' \
'mmroa=D3_mmr_OM25' \
'mmrss=D3_mmr_SS' \
'mmrdust=D3_mmr_DUST' \
'mmrno3=D3_mmr_TNO3' \
'mmrnh4=D3_mmr_NH4_F' \
'emisox=Emis_mgm2_sox' \
'emisnox=Emis_mgm2_nox' )

month_flag=1
day_flag=0

set -x
if [ ${month_flag} -gt 0 ]
	then
   for arg in ${variablelist[*]}
      do echo ${arg}
      aerocomvar=`echo ${arg} | cut -d= -f1`
      emepvar=`echo ${arg} | cut -d= -f2`
      Tempfile="${OutDir}/"
      OutFile="${OutDir}/aerocom.${ModelName}.monthly.${aerocomvar}.${DataYear}.nc"
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
		#if [[ -f ${OutFile} ]]
			#then
			#ncrename -v ${emepvar},${aerocomvar} ${OutFile}
		#fi

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

