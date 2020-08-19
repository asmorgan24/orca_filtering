#Andy Morgan
#8/18/2020
from dict import H91, H92, H94, H91_names, H92_names, H94_names #load all possible substituents
import numpy as np
from copy import deepcopy
import os, shutil, IPython

############
#function(s)
###########
'''shity way to insert strings into file'''
def insert_sub(array, sub):
    for i in range(len(sub)):
        array.append(sub[i])
    return array

############
#Main Script
############
#clear and then generate directory if it does not exist
if os.path.exists('gen_input_files'):
    shutil.rmtree('gen_input_files')
for retry in range(100): #windows sucks and sometimes this is necessary
    try:
        os.makedirs('gen_input_files')
        break
    except:
        None

############
#User input and filter substituents
############
in91 = input ('Location 3: "H", "F", "CH3", "CF3", "OCH3", "CO2CH3", "COCH3", "CONMe2", "Beg":   ')
in92 = input ('Location 4: "H", "F", "CH3", "CF3", "OCH3", "CO2CH3", "COCH3", "CONMe2", "Beg":   ')
in94 = input ('Location 5: "H", "F", "CH3", "CF3", "OCH3", "CO2CH3", "COCH3", "CONMe2", "Beg":   ')

#Filter out all the options, according to what Dr. Pabst wants
idx91 = H91_names.index(in91)
idx92 = H91_names.index(in92)
idx94 = H91_names.index(in94)

H91 = [list(H91[idx91])]
H91_names = [H91_names[idx91]]
H92 = [list(H92[idx92])]
H92_names = [H92_names[idx92]]
H94 = [list(H94[idx94])]
H94_names = [H94_names[idx94]]

##########
#Generate files for each main group
##########
for eleme in ["Co", "Free", "Rad"]:
    '''open the reference files and use the main headers'''
    with open('refs/'+eleme+'.inp', 'rt') as fd:
        mylines = []
        for myline in fd:
            mylines.append(myline.rstrip('\n'))
    #Change the number of processes you want ot use for each
    nprocs = "12"
    mylines[3] = mylines[3][:-2]+nprocs

    '''main loop for generating the files'''
    for replace_91 in range(len(H91)):
        cpy91 = deepcopy(mylines)
        cpy91 = insert_sub(cpy91, H91[replace_91])
        for replace_92 in range(len(H92)):
            cpy92 = deepcopy(cpy91)
            cpy92 = insert_sub(cpy92, H92[replace_92])
            for replace_94 in range(len(H94)):
                cpy94 = deepcopy(cpy92)
                cpy94 = insert_sub(cpy94, H94[replace_94])
                cpy94.extend(["*"]) #add the star at the end
                with open('gen_input_files/'+eleme+'_'+H91_names[replace_91]+'_'+H92_names[replace_92]+'_'+H94_names[replace_94]+'.inp', 'w') as f:
                    for item in cpy94:
                        f.write("%s\n" % item)

dnt_fuk_w_me = input('All files created in gen_input_files folder... Press Enter to quit...')
