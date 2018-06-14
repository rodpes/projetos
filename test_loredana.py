# https://github.com/sergivalverde/cnn-ms-lesion-segmentation/blob/master/train_leave_one_out.py
# https://github.com/sergivalverde/cnn-ms-lesion-segmentation/blob/master/example_1.ipynb

import os
from collections import OrderedDict
from base import *
from build_model_nolearn import cascade_model
from config import *
options = {}


# --------------------------------------------------
# Experiment parameters
# --------------------------------------------------

# image modalities used (T1, FLAIR, PD, T2, ...) 
options['modalities'] = ['T1', 'FLAIR']

# Select an experiment name to store net weights and segmentation masks
options['experiment'] = 'test_CNN2'

# In order to expose the classifier to more challeging samples, a threshold can be used to to select 
# candidate voxels for training. Note that images are internally normalized to 0 mean 1 standard deviation 
# before applying thresholding. So a value of t > 0.5 on FLAIR is reasonable in most cases to extract 
# all WM lesion candidates
options['min_th'] = 0.5

# randomize training features before fitting the model.  
options['randomize_train'] = True

# Select between pixel-wise or fully-convolutional training models. Although implemented, fully-convolutional
# models have been not tested with this cascaded model 
options['fully_convolutional'] = False


# --------------------------------------------------
# model parameters
# --------------------------------------------------

# 3D patch size. So, far only implemented for 3D CNN models. 
options['patch_size'] = (11,11,11)

# percentage of the training vector that is going to be used to validate the model during training
options['train_split'] = 0.25

# maximum number of epochs used to train the model
options['max_epochs'] = 200

# maximum number of epochs without improving validation before stopping training (early stopping) 
options['patience'] = 25

# Number of samples used to test at once. This parameter should be around 50000 for machines
# with less than 32GB of RAM Deep Learning for Medical Image Analysis 
options['batch_size'] = 50000

# net print verbosity. Set to zero for this particular notebook, but setting this value to 11 is recommended
options['net_verbose'] = 11

# post-processing binary threshold. After segmentation, probabilistic masks are binarized using a defined threshold.
options['t_bin'] = 0.8

# The resulting binary mask is filtered by removing lesion regions with lesion size before a defined value
options['l_min'] = 5

exp_folder = os.path.join(os.getcwd(), options['experiment'])
if not os.path.exists(exp_folder):
    os.mkdir(exp_folder)
    os.mkdir(os.path.join(exp_folder,'nets'))
    os.mkdir(os.path.join(exp_folder,'.train'))

# set the output name 
options['test_name'] = 'cnn_' + options['experiment'] + '.nii.gz'
#train_folder = 'C:/Users/Lory/Documents/Loredana/HSR/MS Lesion Segmentation/CNN_Training'
train_folder = '/home/s/tmp/loredana'
train_x_data = {}
train_y_data = {}
d


# TRAIN X DATA
#train_x_data['im1'] = {'T1': os.path.join(train_folder,'im1', 'adnimpr_ax_brain.nii.gz'), 'FLAIR': os.path.join(train_folder,'im1', 'flair_ax_brain.nii.gz')}
train_x_data['1'] = {'T1': os.path.join(train_folder,'1', 'T1_r.nii.gz'), 'FLAIR': os.path.join(train_folder,'1', 'FLAIR.nii.gz')}
# TRAIN LABELS 
#train_y_data['674'] = os.path.join(train_folder,'674', 'FLAIR_lesMASK.nii')
train_y_data['1'] = os.path.join(train_folder,'1', 'lesion.nii')

# INITIALIZE THE MODEL
options['weight_paths'] = os.getcwd()
model = cascade_model(options)

# TRAIN THE MODEL
model = train_cascaded_model(model, train_x_data, train_y_data,  options)

# TEST THE MODEL
# TEST X DATA
#test_folder = 'C:/Users/Lory/Documents/Loredana/HSR/MS Lesion Segmentation/CNN_Training/test_images'
test_folder = '/home/s/tmp/loredana'

test_x_data = {}
#test_x_data['674'] = {'T1': os.path.join(test_folder,'674', 'adnimpr_ax_brain.nii.gz'), 'FLAIR': os.path.join(test_folder,'674', 'flair_ax_brain.nii.gz')}
test_x_data['674'] = {'T1': os.path.join(train_folder,'674', 'T1.nii.gz'), 'FLAIR': os.path.join(train_folder,'674', 'FLAIR.nii.gz')}

# set the output_location of the final segmentation. In this particular example,we are training and testing on the same images
options['test_folder'] = test_folder
options['test_scan'] = '1'
out_seg = test_cascaded_model(model, test_x_data, options)

# ---> testing the model

