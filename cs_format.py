#!/usr/bin/env python3

#----------------------------
#Title: cs_format.py
#Author: Aylin Dincer
#Script Version: 1.0
#Version Date: June 18, 2020
#Built under python version 3.7
#----------------------------

#Import python packages
#----------------------------
import glob, subprocess, os
import pandas as pd
#----------------------------

#Define mri_label2label function
#mri_label2label converts from fsvarege space to subject space.
#----------------------------
def run_label2label(cortsig_filepath, 
                    freesurfer_session, 
                    label2label_output, 
                    hemi, 
                    log_output):
    subprocess.call(['mri_label2label', 
                     '--srclabel', cortsig_filepath, 
                     '--srcsubject', 'fsaverage', 
                     '--trglabel', label2label_output, 
                     '--trgsubject', freesurfer_session, 
                     '--regmethod', 'surface',
                     '--hemi', hemi], 
                    stdout=log_output, stderr=subprocess.STDOUT)
#----------------------------

#Define mris_anatomical_stats function
#mris_anatomical_stats calculates thickness and num of vertices from ROI
#----------------------------
def run_mris_anatstats(label2label_output,
                       thickness_file, 
                       freesurfer_session, 
                       hemi, 
                       log_output):
    subprocess.call(['mris_anatomical_stats', 
                     '-l', label2label_output, 
                     '-f', thickness_file, 
                     freesurfer_session, 
                     hemi], 
                    stdout=log_output, stderr=subprocess.STDOUT)
#----------------------------

#Reformats mris_anatomical_stats output to be readable.
#----------------------------
def run_format(cortsig_name, 
               hemi,
               orig_thicknessdir,
               fs_list):
    #make sure mris_anatstats output exists
    all_files = glob.glob(os.path.join(orig_thicknessdir, 
                                       '*' + cortsig_name + '.csv'))
    #Only keep the files that are in the freesurfer_list 
    req_files = [s for s in all_files if any(xs in s for xs in fs_list)]



    newfile=[]
    for fname in req_files:
        with open(fname, 'r') as oldfile:

            lines = oldfile.read().splitlines()
        #Keep only numerical values in the last line of output.
            last_line = lines[-1]
            last_line = last_line.split('.label')
            th_numbers = last_line[1].split()
            th_title = last_line[0].split('.' + cortsig_name)
            

        #Create new file with numerical values and appropriate header.
            data_f = pd.DataFrame({'Session': th_title[0],
                                   hemi+'.NumVert': [th_numbers[0]], 
                                   hemi+'.SurfArea': [th_numbers[1]],
                                   hemi+'.GrayVol': [th_numbers[2]],
                                   hemi+'.ThickAvg': [th_numbers[3]],
                                   hemi+'.ThickStd': [th_numbers[4]],
                                   hemi+'.MeanCurv': [th_numbers[5]],
                                   hemi+'.GausCurv': [th_numbers[6]],
                                   hemi+'.FoldInd': [th_numbers[7]],
                                   hemi+'.CurvInd': [th_numbers[8]]})
                    
            newfile.append(data_f)
    return newfile
#----------------------------

#Save concat data frame once all freesurfer sessions are appended.
#----------------------------
def save_format(hemi, 
                fs_list, 
                concat_thicknessdir, 
                cortsig_name,
                orig_thicknessdir):
    thickness_concat = os.path.join(concat_thicknessdir, 
                                    cortsig_name + '.concat.csv')
    th_concat = run_format(cortsig_name, hemi, orig_thicknessdir, fs_list)
    concatframe = pd.concat(th_concat, axis=0, ignore_index=True)
    concatframe['match'] = pd.Categorical(
    concatframe['Session'], 
    categories=fs_list, 
    ordered=True)
    concatframe.sort_values('match', inplace = True)
    concatframe.drop('match', axis = 1, inplace = True)
    concatframe.to_csv(thickness_concat, index = False)
#----------------------------


#Run label2label, mris_anatomical_stats, format, and concat functions
#----------------------------
def format_file(cortsig_type,
                outputdir,
                hemisphere, 
                subjectsdir,
                currenttime,
                log_name,
                orig_thicknessdir,
                concat_thicknessdir, 
                fs_list):
    with open(log_name, "a") as log_output: #Log standard output into txt file.
        for hemi in hemisphere:
            cortsig_fname = hemi + '.' + cortsig_type + '.CortSig.label'
            cortsig_name = hemi + '.' + cortsig_type + '.CortSig'
            cortsig_filepath = os.path.join(subjectsdir,
                                            'fsaverage/label/',
                                            cortsig_fname)
            for freesurfer_session in fs_list:
                freesurfer_session = freesurfer_session.strip()

                #Define variables needed for functions

                label2label_output = os.path.join(subjectsdir, 
                                                  freesurfer_session, 
                                                  'label/', 
                                                  freesurfer_session + '.' + cortsig_fname)
                thickness_file = os.path.join(orig_thicknessdir, 
                                              freesurfer_session + '.' + cortsig_name + '.csv')

                
                #Run label2label, mris_anatomical_stats, format, and concat fxns
                run_label2label(cortsig_filepath, 
                                freesurfer_session, 
                                label2label_output, 
                                hemi, 
                                log_output)
                
                run_mris_anatstats(label2label_output, 
                                   thickness_file, 
                                   freesurfer_session, 
                                   hemi, 
                                   log_output)
            save_format(hemi, 
                        fs_list, 
                        concat_thicknessdir, 
                        cortsig_name, 
                        orig_thicknessdir)
            
#----------------------------


        

if __name__ == '__main__':
    format_file()
