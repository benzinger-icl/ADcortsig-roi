# AD Cortical Signature ROI's
## Overview

This repository contains the Alzheimer disease cortical signature region of interests (ROIs). The cortical signatures are a composite of brain regions susceptible to AD-related cortical atrophy for autosomal dominant Alzheimer disease (ADAD, Figure 1) and late-onset Alzheimer disease (LOAD, Figure 2) defined in Dincer et.al., 2020 (submitted).

![ADAD Cortical Signature](https://github.com/benzinger-icl/ADcortsig-roi/blob/master/example_images/ADADCortSig_image.png)

Figure 1: Brain regions susceptible cortical atrophy for autosomal domainant Alzheimer disease

![LOAD Cortical Signature](https://github.com/benzinger-icl/ADcortsig-roi/blob/master/example_images/LOADCortSig_image.png)

Figure 2: Brain regions susceptible cortical atrophy for late-onset Alzheimer disease


The cortical signature files are located under the 'cortical_signature_roi' directory.  The ROI files are in FreeSurfer label format. Python scripts are available to calculate the cortical signature thickness measure for a batch of FreeSurfer sessions. We recommend using the cortical signature maps on FreeSurfer version 5.3, 6.0, and 7.1. Other FreeSurfer versions have not been tested.

The scripts perform the following steps:
-	Register cortical signature maps to participant space. (*mri_label2label*)
-	Obtain the cortical thickness value from the maps for the left and right hemisphere (*mris_anatomicalstats*)
-	Format the *mris_anatomicalstats* output to a readable table
-	Calculate the cortical signature thickness measure and output to a CSV file.


## To Use:
1. Download and install python 3 (https://www.python.org/) and the pandas package (https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)

2. Download from this repository:
- 'cortical_signature_ROIs' directory
- cs_calc.py
- cs_format.py
- cs_main.py
- freesurfer_list.csv

3. Open the terminal and setup your FreeSurfer environment variables.

```
export FREESURFER_HOME=/usr/local/freesurfer

export SUBJECTS_DIR=/path/to/freesurfer_files

source $FREESURFER_HOME/SetUpFreeSurfer.sh
```

4. Copy the 'fsaverage' to your $SUBJECTS_DIR directory.

```
cp -r $FREESURFER_HOME/subjects/fsaverage $SUBJECTS_DIR
```

5. Copy the cortical siganture FreeSurfer label files under the 'cortical_signature_roi' directory to $SUBJECTS_DIR/fsaverage/label.

```
cp /path/to/cortical_signature_roi/* $SUBJECTS_DIR/fsaverage/label/
```

6. Update the targeted FreeSurfer session list into the freesurfer_list.csv, with each row being a FreeSurfer session.

Note: FreeSurfers listed in freesurfer_list.csv should be in your SUBJECT_DIR path.

7. Run the cs_main.py script.
```
Command for the LOAD cortical signature:
python ./cs_main.py LOAD /absolute_path/to/freesurfer_list.csv /absolute_path/to/output_directory

Command for the ADAD cortical signature:
python ./cs_main.py ADAD /absolute_path/to/freesurfer_list.csv /absolute_path/to/output_directory
```
Note:  output directory should exist before running script.

## Script Output Description

The output directory will contain the following: 
1.	'orig_th' directory
2.	'concat_th' directory
3.	[ADAD/LOAD].CortSig.csv
4.	Cortsig_DATE_TIME.txt

**'orig_th' directory**
: This directory hold the original stat output from the *mris_anatomicalstats* command for each FreeSurfer in freesurfer_list.csv

**'concat_th' directory**
: The original *mris_anatomicalstats* output is formatted to be more readable and the data is combined for all FreeSurfers and saved into this directory.

**[ADAD/LOAD].CortSig.csv**
: This is the finalized output containing the average cortical signature thickness value for each FreeSurfer in freesurfer_list.csv

**cortsig_DATE_TIME.txt**
: Logs the output from the *mris_label2label* and *mris_anatomicalstats* functions
