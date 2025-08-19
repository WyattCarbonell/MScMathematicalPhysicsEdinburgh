import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
os.chdir("UN")

def ExpDec(x, A, B, C, D):
    return A*np.exp(-B*(x - D)) + C

Master_out = []
Params_List = []
for filename in os.listdir(os.getcwd()):
    DataFrame = pd.read_csv(filename)

    Out = [0, 0]
    
    Times = DataFrame["Times"].to_numpy()
    Positions = DataFrame["Positions"].to_numpy()
    RFs = DataFrame["RFs"].to_numpy()
    Params = DataFrame["Params"].to_numpy()
      
    param = Params[0]
    
    if param not in Params_List:
        Params_List.append(param)
        Master_out.append([])
      
    for i in range(len(Times)):
        time = Times[i]
        pos = Positions[i]
        if round(time+0.01, 2)%param == 0:
            if pos < 0:
                Out[1] = Out[1] + 1
            elif pos > 0:
                Out[0] = Out[0] + 1
                
    Master_out[Params_List.index(param)].append(100*Out[0]/(Out[0]+Out[1]))

Data_1 = []
Errs_1 = []
Params_1 = Params_List
for item in Master_out:
    Data_1.append(np.mean(item))
    Errs_1.append(np.std(item) / np.sqrt(len(item)))

os.chdir("../3_1")

Master_out = []
Params_List = []
for filename in os.listdir(os.getcwd()):
    
    DataFrame = pd.read_csv(filename)

    Out = [0, 0]
    
    Times = DataFrame["Times"].to_numpy()
    Positions = DataFrame["Positions"].to_numpy()
    RFs = DataFrame["RFs"].to_numpy()
    Params = DataFrame["Params"].to_numpy()
      
    param = Params[0]
    
    if param not in Params_List:
        Params_List.append(param)
        Master_out.append([])
      
    for i in range(len(Times)):
        time = Times[i]
        pos = Positions[i]
        if round(time+0.01, 2)%param == 0:
            if pos < 0:
                Out[1] = Out[1] + 1
            elif pos > 0:
                Out[0] = Out[0] + 1
                
    Master_out[Params_List.index(param)].append(100*Out[1]/(Out[0]+Out[1]))

Data_2 = []
Errs_2 = []
Params_2 = Params_List
for item in Master_out:
    Data_2.append(np.mean(item))
    Errs_2.append(np.std(item)/np.sqrt(len(item)))

popt1, pcov = curve_fit(ExpDec, Params_1, Data_1, sigma=Errs_1)
popt2, pcov = curve_fit(ExpDec, Params_2, Data_2, sigma=Errs_2)

y_1 = []
y_2 = []
y_diff = []

for param in Params_1:
    y_1.append(ExpDec(param, popt1[0], popt1[1], popt1[2], popt1[3]))

for param in Params_2:
    y_2.append(ExpDec(param, popt2[0], popt2[1], popt2[2], popt2[3]))


os.chdir("..")

fig, axs = plt.subplots(2, sharex='col')
axs[0].errorbar(Params_1, Data_1, yerr=Errs_1, fmt='o')
axs[1].errorbar(Params_2, Data_2, yerr=Errs_2, fmt='o')
axs[0].plot(Params_1, y_1, alpha = 0.5, linestyle='dashed')
axs[1].plot(Params_2, y_2, alpha = 0.5, linestyle='dashed')
axs[0].set_ylabel("% of times UN stayed UN")
axs[1].set_ylabel("% of times 3_1 stayed 3_1")
fig.savefig("UU-33_Differences.pdf")
"""
Differences = []
Difference_Params = []
Difference_Errs = []
for param in Params_1:
    if param <= 3500:
        Difference_Params.append(param)
        Differences.append(Data_1[Params_1.index(param)] - Data_2[Params_2.index(param)])
        Difference_Errs.append(Errs_1[Params_1.index(param)] + Errs_2[Params_2.index(param)])
        y_diff.append(ExpDec(param, popt1[0], popt1[1], popt1[2], popt1[3]) - ExpDec(param, popt2[0], popt2[1], popt2[2], popt2[3]))

plt.errorbar(Difference_Params, Differences, yerr=Difference_Errs, fmt = 'o')
plt.plot(Difference_Params, y_diff, alpha = 0.5, linestyle='dashed')
plt.ylabel("%(UN->UN) - %(3_1->3_1)")
plt.xlabel("Reset Time")
plt.savefig("UU_33_ResetTimes.pdf")
"""
