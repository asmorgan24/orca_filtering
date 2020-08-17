import os
import numpy as np
import pandas as pd

all_files = os.listdir("outputs/")
data = pd.DataFrame(columns=all_files, index =['neg_num_vibration', 'gibbs_enthalpy'])
num_neg_vibs = []
gibbs_freq = []
for file in all_files:
    print('Loading file... ', file)
    with open('outputs/'+file, 'rt') as fd:
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
        while 'cm**-1' in mylines[line_start+idx][-6:]:
            vals_str.append(mylines[line_start+idx][6:-6])
            idx+=1
        vals = np.asarray([float(i) for i in vals_str])
        data[file]['neg_num_vibration'] = sum(vals<0)

        ### Now search for gibbs enthalpy
        for line_num in range(len(mylines)):
           if "Final Gibbs free enthalpy " in mylines[line_num]:
                data[file]['gibbs_enthalpy'] = float(mylines[line_num][38:-3])

print ('Done reading...')
data.to_csv('.\output.csv')

inner = input("... Done. Hit enter to close. See output.csv")
