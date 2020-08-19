import os, sys, IPython
import numpy as np
import pandas as pd

all_files = os.listdir("outputs/")
if len(all_files)%3 !=0: #do not have enough matches
    print ('[ERR] do not have matching number of files... Closing...')
    sys.exit()

#First find all Co's
Co_indices = []
for f in range(len(all_files)):
    if all_files[f][:2]=='Co':
        Co_indices.append(f)

#Then, according to each Co in the list, find the corresponding Free and Rad
Free_indices = []
Rad_indices = []
Substituent_order = []
for f in range(len(Co_indices)):
    match_str = all_files[f][3:-4] #This will be the string we want to match from
    Substituent_order.append(match_str)
    for s in range(len(all_files)): #search all the files to see which strings match
        if match_str in all_files[s]:
            if all_files[s][:2] == 'Fr':
                Free_indices.append(s)
            elif all_files[s][:2] == 'Ra':
                Rad_indices.append(s)
            elif all_files[s][:2] == 'Co':
                None
            else:
                print ('Files do not match for seq: ', match_str)
                sys.exit()


def read_file (file_name):
    with open('outputs/'+file_name, 'rt') as fd:
        ### First parse through the vibration data
        mylines = []
        for myline in fd:
            mylines.append(myline.rstrip('\n'))
        line_start = None
        for line_num in range(len(mylines)):
            if "VIBRATIONAL FREQUENCIES" in mylines[line_num]:
                line_start = line_num
        line_start +=3 #offset in ORCID

        idx = 0
        vals_str = []
        while 'cm**-1' in mylines[line_start+idx]:
            vals_str.append(mylines[line_start+idx][6:19])
            idx+=1
        vals = np.asarray([float(i) for i in vals_str])
        neg_num_vibration=sum(vals<0)
        lt_neg_20_vibration = sum(vals<-20)

        ### Now search for gibbs enthalpy
        for line_num in range(len(mylines)):
           if "Final Gibbs free enthalpy " in mylines[line_num]:
                gibbs_enthalpy = float(mylines[line_num][38:-3])
    return neg_num_vibration, lt_neg_20_vibration, gibbs_enthalpy

index_rows = ['Co_neg_vib', 'Co_neg20_vib', "Co_gibbs",
              'Fr_neg_vib', 'Fr_neg20_vib', "Fr_gibbs",
              'Ra_neg_vib', 'Ra_neg20_vib', "Ra_gibbs",
              'BDFE(CH)', 'BDFE(MC)']
data = pd.DataFrame(columns=Substituent_order, index =index_rows)

#Now we have the corresponding indices for each of them, we just need to read all three of them in and get the results
for i in range(len(Co_indices)):
    Co_n, Co_n20, Co_gi = read_file(all_files[Co_indices[i]])
    Fr_n, Fr_n20, Fr_gi = read_file(all_files[Free_indices[i]])
    Ra_n, Ra_n20, Ra_gi = read_file(all_files[Co_indices[i]])
    BDFE_CH = 627.509474*(Fr_gi - (Ra_gi - 0.513321))
    BDFE_MC = 627.509474*(Co_gi - (Ra_gi - 3314.8690))

    vals = [Co_n, Co_n20, Co_gi, Fr_n, Fr_n20, Fr_gi, Ra_n, Ra_n20, Ra_gi, BDFE_CH, BDFE_MC]
    for j in range(len(vals)):
        data[Substituent_order[i]][index_rows[j]] = vals[j]

data.to_csv('.\output.csv')
outie_naval = input("... Done. Hit enter to close. See output.csv")
