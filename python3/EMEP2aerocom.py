#!/usr/bin/env python3

#  Copyright (c) 2019. Met Norway
#   Contact information:
#   Norwegian Meteorological Institute
#   Box 43 Blindern
#   0313 OSLO
#   NORWAY
#   E-mail: jan.griesfeller@met.no
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#   MA 02110-1301, USA
#

def __init__():
    pass

if __name__ == "__main__":
    """command line converter between EMEP output format and aerocom input format
    
    """
    import argparse
    import os

    options = {}

    parser = argparse.ArgumentParser(
        description='EMEP2aerocom.py\n a command line converter between the EMEP data format and the aerocom format\n\n')
    parser.add_argument("--file",
                        help="file(s) to read", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity",
                        action='store_true')
    parser.add_argument("-o", "--outfile", help="output file")
    parser.add_argument("--outdir", help="output directory")
    parser.add_argument("-O", "--overwrite", help="overwrite output file", action='store_true')
    parser.add_argument("--dir", help="work on all files below this directory",
                        default='./')
    parser.add_argument("--tempdir", help="directory for temporary files",
                        default=os.path.join(os.environ['HOME'], 'tmp'))
    parser.add_argument("--variables",
                        help="comma separated list of variables to write; default: ec355aer,bs355aer",
                        default='ec355aer')

    args = parser.parse_args()

    if args.dir:
        options['dir'] = args.dir

    if args.outdir:
        options['outdir'] = args.outdir

    if args.variables:
        options['variables'] = args.variables.split(',')

    if args.file:
        options['files'] = args.file

    if args.overwrite:
        options['overwrite'] = True
    else:
        options['overwrite'] = False

    if args.outfile:
        options['outfile'] = args.outfile

    from nco import Nco

    nco = Nco()

    # dict where the key is the EMEP variable name
    CONV_VARS = {}
    CONV_VARS['SURF_ug_PM10'] = {}
    CONV_VARS['SURF_ug_PM10']['aerocom_name'] = 'sconcpm10'
    CONV_VARS['SURF_ug_PM10rh50'] = {}
    CONV_VARS['SURF_ug_PM10rh50']['aerocom_name'] = 'sconcpm10'
    CONV_VARS['SURF_ug_PM10_rh50'] = {}
    CONV_VARS['SURF_ug_PM10_rh50']['aerocom_name'] = 'sconcpm10'
    CONV_VARS['SURF_ug_PM25'] = {}
    CONV_VARS['SURF_ug_PM25']['aerocom_name'] = 'sconcpm25'
    CONV_VARS['SURF_ug_PM25rh50'] = {}
    CONV_VARS['SURF_ug_PM25rh50']['aerocom_name'] = 'sconcpm25'
    CONV_VARS['SURF_ug_PM25_rh50'] = {}
    CONV_VARS['SURF_ug_PM25_rh50']['aerocom_name'] = 'sconcpm25'
    CONV_VARS['SURF_ug_SO2'] = {}
    CONV_VARS['SURF_ug_SO2']['aerocom_name'] = 'sconcso2'
    CONV_VARS['SURF_ugS_SO2'] = {}
    CONV_VARS['SURF_ugS_SO2']['aerocom_name'] = 'sconcso2'
    CONV_VARS['SURF_ug_SO4'] = {}
    CONV_VARS['SURF_ug_SO4']['aerocom_name'] = 'sconcso4'
    CONV_VARS['SURF_ugS_SO4'] = {}
    CONV_VARS['SURF_ugS_SO4']['aerocom_name'] = 'sconcso4'
    CONV_VARS['WDEP_SOX'] = {}
    CONV_VARS['WDEP_SOX']['aerocom_name'] = 'wetso4'
    CONV_VARS['SURF_ug_NH3'] = {}
    CONV_VARS['SURF_ug_NH3']['aerocom_name'] = 'sconcnh3'
    CONV_VARS['SURF_ugN_NH3'] = {}
    CONV_VARS['SURF_ugN_NH3']['aerocom_name'] = 'sconcnh3'
    CONV_VARS['SURF_ug_NH4_F'] = {}
    CONV_VARS['SURF_ug_NH4_F']['aerocom_name'] = 'sconcnh4'
    CONV_VARS['SURF_ugN_NH4_F'] = {}
    CONV_VARS['SURF_ugN_NH4_F']['aerocom_name'] = 'sconcnh4'
    CONV_VARS['WDEP_RDN'] = {}
    CONV_VARS['WDEP_RDN']['aerocom_name'] = 'wetrdn'
    CONV_VARS['SURF_ugN_RDN'] = {}
    CONV_VARS['SURF_ugN_RDN']['aerocom_name'] = 'sconcrdn'
    CONV_VARS['SURF_ug_NO'] = {}
    CONV_VARS['SURF_ug_NO']['aerocom_name'] = 'sconcno'
    CONV_VARS['SURF_ugN_NO'] = {}
    CONV_VARS['SURF_ugN_NO']['aerocom_name'] = 'sconcno'
    CONV_VARS['SURF_ug_NO2'] = {}
    CONV_VARS['SURF_ug_NO2']['aerocom_name'] = 'sconcno2'
    CONV_VARS['SURF_ugN_NO2'] = {}
    CONV_VARS['SURF_ugN_NO2']['aerocom_name'] = 'sconcno2'
    CONV_VARS['SURF_ug_HNO3'] = {}
    CONV_VARS['SURF_ug_HNO3']['aerocom_name'] = 'sconchno3'
    CONV_VARS['SURF_ugN_HNO3'] = {}
    CONV_VARS['SURF_ugN_HNO3']['aerocom_name'] = 'sconchno3'
    CONV_VARS['SURF_ug_TNO3'] = {}
    CONV_VARS['SURF_ug_TNO3']['aerocom_name'] = 'sconcno3'
    CONV_VARS['WDEP_OXN'] = {}
    CONV_VARS['WDEP_OXN']['aerocom_name'] = 'wetoxn'
    CONV_VARS['SURF_MAXO3'] = {}
    CONV_VARS['SURF_MAXO3']['aerocom_name'] = 'vmro3max'
    CONV_VARS['SURF_ppb_O3'] = {}
    CONV_VARS['SURF_ppb_O3']['aerocom_name'] = 'vmro3'
    CONV_VARS['SURF_2MO3'] = {}
    CONV_VARS['SURF_2MO3']['aerocom_name'] = 'vmro32m'
    CONV_VARS['SURF_ug_SS'] = {}
    CONV_VARS['SURF_ug_SS']['aerocom_name'] = 'sconcss'
    CONV_VARS['SURF_PM25water'] = {}
    CONV_VARS['SURF_PM25water']['aerocom_name'] = 'sconcaeroh2o'
    CONV_VARS['DUST_flux'] = {}
    CONV_VARS['DUST_flux']['aerocom_name'] = 'emidust'
    CONV_VARS['AOD'] = {}
    CONV_VARS['AOD']['aerocom_name'] = 'od550aer'
    CONV_VARS['AOD_350nm'] = {}
    CONV_VARS['AOD_350nm']['aerocom_name'] = 'od350aer'
    CONV_VARS['AOD_550nm'] = {}
    CONV_VARS['AOD_550nm']['aerocom_name'] = 'od550aer'
    CONV_VARS['AOD_440nm'] = {}
    CONV_VARS['AOD_440nm']['aerocom_name'] = 'od440aer'
    CONV_VARS['AOD_870nm'] = {}
    CONV_VARS['AOD_870nm']['aerocom_name'] = 'od870aer'
    CONV_VARS['AOD_SS_550nm'] = {}
    CONV_VARS['AOD_SS_550nm']['aerocom_name'] = 'od550ss'
    CONV_VARS['AOD_SO4_550nm'] = {}
    CONV_VARS['AOD_SO4_550nm']['aerocom_name'] = 'od550so4'
    CONV_VARS['AOD_TNO3_550nm'] = {}
    CONV_VARS['AOD_TNO3_550nm']['aerocom_name'] = 'od550no3'
    CONV_VARS['AOD_NH4_F_550nm'] = {}
    CONV_VARS['AOD_NH4_F_550nm']['aerocom_name'] = 'od550nh4'
    CONV_VARS['AOD_OM25_550nm'] = {}
    CONV_VARS['AOD_OM25_550nm']['aerocom_name'] = 'od550oa'
    CONV_VARS['AOD_EC_550nm'] = {}
    CONV_VARS['AOD_EC_550nm']['aerocom_name'] = 'od550bc'
    CONV_VARS['AOD_DUST_550nm'] = {}
    CONV_VARS['AOD_DUST_550nm']['aerocom_name'] = 'od550dust'
    CONV_VARS['AOD_OM25_550nm'] = {}
    CONV_VARS['AOD_OM25_550nm']['aerocom_name'] = 'od550oa'
    CONV_VARS['AOD_PMFINE_550nm'] = {}
    CONV_VARS['AOD_PMFINE_550nm']['aerocom_name'] = 'od550lt1aer'
    CONV_VARS['AbsCoef'] = {}
    CONV_VARS['AbsCoef']['aerocom_name'] = 'absc550dryaer'
    CONV_VARS['ExtinSurf'] = {}
    CONV_VARS['ExtinSurf']['aerocom_name'] = 'ec550aer'
    CONV_VARS['EXT_350nm'] = {}
    CONV_VARS['EXT_350nm']['aerocom_name'] = 'ec3503Daer'
    CONV_VARS['EXT_550nm'] = {}
    CONV_VARS['EXT_550nm']['aerocom_name'] = 'ec5503Daer'
    CONV_VARS['D3_ExtinCoef'] = {}
    CONV_VARS['D3_ExtinCoef']['aerocom_name'] = 'ec5503Daer'
    CONV_VARS['SURF_ug_DUST'] = {}
    CONV_VARS['SURF_ug_DUST']['aerocom_name'] = 'sconcdust'
    CONV_VARS['SURF_ug_ECFINE'] = {}
    CONV_VARS['SURF_ug_ECFINE']['aerocom_name'] = 'sconcbcf'
    CONV_VARS['SURF_ug_ECCOARSE'] = {}
    CONV_VARS['SURF_ug_ECCOARSE']['aerocom_name'] = 'sconcbcc'
    CONV_VARS['SURF_ug_PART_OM_F'] = {}
    CONV_VARS['SURF_ug_PART_OM_F']['aerocom_name'] = 'sconcoaf'
    CONV_VARS['SURF_ug_OMCOARSE'] = {}
    CONV_VARS['SURF_ug_OMCOARSE']['aerocom_name'] = 'sconcoac'
    CONV_VARS['D3_Zmid'] = {}
    CONV_VARS['D3_Zmid']['aerocom_name'] = 'z3d'
    CONV_VARS['COLUMN_SO2_kmax'] = {}
    CONV_VARS['COLUMN_SO2_kmax']['aerocom_name'] = 'loadso2'
    CONV_VARS['COLUMN_SO4_kmax'] = {}
    CONV_VARS['COLUMN_SO4_kmax']['aerocom_name'] = 'loadso4'
    CONV_VARS['COLUMN_SS_kmax'] = {}
    CONV_VARS['COLUMN_SS_kmax']['aerocom_name'] = 'loadss'
    CONV_VARS['COLUMN_EC_kmax'] = {}
    CONV_VARS['COLUMN_EC_kmax']['aerocom_name'] = 'loadbc'
    CONV_VARS['COLUMN_OM25_kmax'] = {}
    CONV_VARS['COLUMN_OM25_kmax']['aerocom_name'] = 'loadoa'
    CONV_VARS['COLUMN_DUST_kmax'] = {}
    CONV_VARS['COLUMN_DUST_kmax']['aerocom_name'] = 'loaddust'
    CONV_VARS['COLUMN_TNO3_kmax'] = {}
    CONV_VARS['COLUMN_TNO3_kmax']['aerocom_name'] = 'loadno3'
    CONV_VARS['COLUMN_NH4_F_kmax'] = {}
    CONV_VARS['COLUMN_NH4_F_kmax']['aerocom_name'] = 'loadnh4'
    CONV_VARS['WDEP_SO2'] = {}
    CONV_VARS['WDEP_SO2']['aerocom_name'] = 'wetso2'
    CONV_VARS['WDEP_SO4'] = {}
    CONV_VARS['WDEP_SO4']['aerocom_name'] = 'wetso4'
    CONV_VARS['WDEP_EC'] = {}
    CONV_VARS['WDEP_EC']['aerocom_name'] = 'wetbc'
    CONV_VARS['WDEP_OM25'] = {}
    CONV_VARS['WDEP_OM25']['aerocom_name'] = 'wetoa'
    CONV_VARS['WDEP_SS'] = {}
    CONV_VARS['WDEP_SS']['aerocom_name'] = 'wetss'
    CONV_VARS['WDEP_DUST'] = {}
    CONV_VARS['WDEP_DUST']['aerocom_name'] = 'wetdust'
    CONV_VARS['WDEP_TNO3'] = {}
    CONV_VARS['WDEP_TNO3']['aerocom_name'] = 'wetno3'
    CONV_VARS['WDEP_NH4_f'] = {}
    CONV_VARS['WDEP_NH4_f']['aerocom_name'] = 'wetnh4'
    CONV_VARS['DDEP_SO2'] = {}
    CONV_VARS['DDEP_SO2']['aerocom_name'] = 'dryso2'
    CONV_VARS['DDEP_SO4'] = {}
    CONV_VARS['DDEP_SO4']['aerocom_name'] = 'dryso4'
    CONV_VARS['DDEP_EC'] = {}
    CONV_VARS['DDEP_EC']['aerocom_name'] = 'drybc'
    CONV_VARS['DDEP_OM25'] = {}
    CONV_VARS['DDEP_OM25']['aerocom_name'] = 'dryoa'
    CONV_VARS['DDEP_SS'] = {}
    CONV_VARS['DDEP_SS']['aerocom_name'] = 'dryss'
    CONV_VARS['DDEP_DUST'] = {}
    CONV_VARS['DDEP_DUST']['aerocom_name'] = 'drydust'
    CONV_VARS['DDEP_TNO3'] = {}
    CONV_VARS['DDEP_TNO3']['aerocom_name'] = 'dryno3'
    CONV_VARS['DDEP_NH4_f'] = {}
    CONV_VARS['DDEP_NH4_f']['aerocom_name'] = 'drynh4'
    CONV_VARS['D3_mmr_SO2'] = {}
    CONV_VARS['D3_mmr_SO2']['aerocom_name'] = 'mmrso2'
    CONV_VARS['D3_mmr_SO4'] = {}
    CONV_VARS['D3_mmr_SO4']['aerocom_name'] = 'mmrso4'
    CONV_VARS['D3_mmr_EC'] = {}
    CONV_VARS['D3_mmr_EC']['aerocom_name'] = 'mmrbc'
    CONV_VARS['D3_mmr_OM25'] = {}
    CONV_VARS['D3_mmr_OM25']['aerocom_name'] = 'mmroa'
    CONV_VARS['D3_mmr_SS'] = {}
    CONV_VARS['D3_mmr_SS']['aerocom_name'] = 'mmrss'
    CONV_VARS['D3_mmr_DUST'] = {}
    CONV_VARS['D3_mmr_DUST']['aerocom_name'] = 'mmrdust'
    CONV_VARS['D3_mmr_TNO3'] = {}
    CONV_VARS['D3_mmr_TNO3']['aerocom_name'] = 'mmrno3'
    CONV_VARS['D3_mmr_NH4_F'] = {}
    CONV_VARS['D3_mmr_NH4_F']['aerocom_name'] = 'mmrnh4'
    CONV_VARS['Emis_mgm2_sox'] = {}
    CONV_VARS['Emis_mgm2_sox']['aerocom_name'] = 'emisox'
    CONV_VARS['Emis_mgm2_nox'] = {}
    CONV_VARS['Emis_mgm2_nox']['aerocom_name'] = 'emisnox'








    import nco
    # os.environ['CODA_DEFINITION'] = options['codadef']
