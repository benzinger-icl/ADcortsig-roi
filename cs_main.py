#!/usr/bin/env python3

#----------------------------
#Title: cortsig_main.py
#Author: Aylin Dincer
#Script Version: 1.0
#Version Date: June 18, 2020
#Built under python version 3.7
#----------------------------

#Import python packages
#----------------------------
import argparse, os
from datetime import datetime
import cs_format, cs_calc
#----------------------------

# Define agruments
#----------------------------
parser = argparse.ArgumentParser(
    description = '''This program will calculate the ADAD or LOAD 
    cortical signature thickness values for a list of FreeSurfers. 
    Example usage: python ./cortsig_main.py 
    LOAD abs_path/to/freesurfer_file.csv abs_path/to/outputdir''')
    
parser.add_argument('cortsig_type', 
                    help = 'ADAD or LOAD. Uppercase letters are required.')
parser.add_argument('freesurfer_file', 
                    help = '''Absolute path to txt/csv file with a list of 
                    FreeSurfer sessions.''')
parser.add_argument('outputdir',  
                    help = '''Absolute path to output directory.  
                    This is where all the output files will be saved.''')

args=parser.parse_args()

cortsig_type = args.cortsig_type
freesurfer_file = args.freesurfer_file
outputdir = args.outputdir
#----------------------------

# Check FreeSurfer Environment Variables
#----------------------------
fs_env_var = ['FREESURFER_HOME', 'SUBJECTS_DIR']
for var in fs_env_var:
    if var not in os.environ:
        raise EnvironmentError('{} is not defined.'.format(var))

subjectsdir = os.getenv('SUBJECTS_DIR')
print("\n Found SUBJECTS_DIR path: {}\n".format(subjectsdir))
#----------------------------

# Check agrument variables
#----------------------------
cs_check = ['ADAD', 'LOAD']
if cortsig_type not in cs_check:
    raise ValueError('Invalid input. Please input [ADAD] or [LOAD] in the cortsig_type argument.')

if not os.path.exists(outputdir):
    raise FileNotFoundError('Unable to locate output directory path.')
    
if not os.path.exists(freesurfer_file):
    raise FileNotFoundError('Unable to locate freesurfer file.')
#----------------------------

#Create additional output directories
#----------------------------
orig_thicknessdir = os.path.join(outputdir,'orig_th')
os.makedirs(orig_thicknessdir, exist_ok=True)

concat_thicknessdir = os.path.join(outputdir,'concat_th')
os.makedirs(concat_thicknessdir, exist_ok=True)
#----------------------------

#Setup log output file
#----------------------------
currenttime = datetime.today().strftime('%Y%m%d-%H%M%S')
log_name = os.path.join(outputdir, 'cortsig' + '_' + currenttime + ".txt")
#----------------------------

#Define other required variables
#----------------------------
hemisphere = ['lh', 'rh']

#Generate list of FreeSurfer sessions
fs_list = []
with open(freesurfer_file, 'r') as freesurfer_list, open(log_name, 'a') as log_output:
    fs_list = freesurfer_list.read().splitlines()
    print('FreeSurfer List:', file = log_output, flush = True)
    print(fs_list, file = log_output, flush = True)
#----------------------------
 
#Run cs_format.py and cs_calc.py
#----------------------------
cs_format.format_file(cortsig_type, 
                      outputdir, 
                      hemisphere, 
                      subjectsdir, 
                      currenttime, 
                      log_name, 
                      orig_thicknessdir, 
                      concat_thicknessdir, 
                      fs_list)

cs_calc.cs_calc(concat_thicknessdir, 
                cortsig_type, 
                outputdir)
#----------------------------


