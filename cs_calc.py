#!/usr/bin/env python3

#----------------------------
#Title: cs_calc.py
#Author: Aylin Dincer
#Script Version: 1.0
#Version Date: June 18, 2020
#Built under python version 3.7
#----------------------------

#Import python packages
#----------------------------
import os
import pandas as pd
#----------------------------

#Define equation for weighted average
#----------------------------
def cortsig_eq(df_inner):
    return((df_inner['lh.ThickAvg']*df_inner['lh.NumVert']+df_inner['rh.ThickAvg']*df_inner['rh.NumVert'])/
           (df_inner['lh.NumVert']+df_inner['rh.NumVert']))
#----------------------------


#Calculate weighted average fore every freesurfer session.
#---------------------------- 
def cs_calc(concat_thicknessdir, 
                 cortsig_type, 
                 outputdir):
    #Define lh and rh concat files
    lhfile = os.path.join(concat_thicknessdir,
                          'lh.'+ cortsig_type + '.CortSig.concat.csv')
    rhfile = os.path.join(concat_thicknessdir,
                          'rh.'+ cortsig_type + '.CortSig.concat.csv')
    #Output name for calculated cortsig thickness
    finalfile = os.path.join(outputdir, 
                             cortsig_type + '.CortSig.csv')

    #Make sure lhfile and rhfile concat files exists.
    if not os.path.exists(lhfile) and os.path.exists(rhfile):
        raise FileNotFoundError('Unable to locate thickness file.')
        
    print('Calculating {} cortical signature thickness values...'.format(cortsig_type))
    lhdf = pd.read_csv(lhfile, index_col=None, header=0)
    rhdf = pd.read_csv(rhfile, index_col=None, header=0)
    df_inner = pd.merge(lhdf, rhdf, on='Session', how='inner')
    df_inner['CortSig_Thickness'] = cortsig_eq(df_inner)
    df_inner = df_inner[['Session','CortSig_Thickness']]
    df_inner.to_csv(finalfile, index = False)
       
        
if __name__ == '__main__':
    cs_calc()