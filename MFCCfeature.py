#!/usr/bin/env python
# coding: utf-8

# In[3]:


from PIL import Image as img
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.pyplot import figure
import os


# In[8]:


# To use, we can simply import the functions here
# the outputs are a list of 2, 1st element is MFCC image, 2nd element is other features
def AudioFeature_from_csv(input_path,*,img_size=[240,120],output_mfcc='default',output_other='default'):
    filename = input_path[-21:]
    data_audio = pd.read_csv(input_path,sep=';')
    data_mfcc = data_audio.iloc[:,31:43]
    data_other = data_audio.loc[:,['pcm_intensity','pcm_loudness','pcm_zcr','voiceProb']]
    data_mfcc_array = np.array(data_mfcc).transpose()
    image = img.fromarray(data_mfcc_array,'L')
    img_mfcc = image.resize(img_size,img.LANCZOS)
    plt.rcParams["figure.figsize"] = (12,8)
    fig, ax = plt.subplots()
    cax = ax.imshow(img_mfcc, interpolation='nearest', cmap=cm.viridis, origin='lower')
    ax.axis('off')
    if output_mfcc=='default':
        if 'MFCC_features' not in os.listdir():
            os.mkdir('MFCC_features')
        fig.savefig('MFCC_features\\'+filename+'_MFCC.png',dpi=150)
    else:
        fig.savefig(output_mfcc+'\\'+filename+'_MFCC.png',dpi=150)
    if output_other=='default':
        if 'other_audio_features' not in os.listdir():
            os.mkdir('other_audio_features')
        data_other.to_csv('other_audio_features\\'+filename+'_otherfeatures.csv')
    else:
        data_other.to_csv(output_other+'\\'+filename+'_otherfeatures.csv')      

