import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

os.chdir("UN")

Data_array_1 = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
Errs_array_1 = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
Params_array_1 = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]

Data_array_2 = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
Errs_array_2 = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
Params_array_2 = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]

for a in range(1, 6):
    for b in range(1, 6):
        U_max = round(5*a/1000000.0 + 25.0/1000000.0, 8)
        sigma = round(b/10.0, 3)
        
        print(str(U_max) + "   " + str(sigma))

        Master_out = []
        Params_List = []
        
        for filename in os.listdir(os.getcwd()):
            DataFrame = pd.read_csv(filename)
        
            Out = [0, 0]
            
            Params = DataFrame["Param1"].to_numpy()
            param1 = round(Params[0], 2) #reset time
            Params = DataFrame["Param2"].to_numpy()
            param2 = round(Params[0], 8) #U max
            Params = DataFrame["Param3"].to_numpy()
            param3 = round(Params[0], 3) #sigma
            
            if (U_max == param2) and (sigma == param3):
                U_index = a-1
                S_index = b-1
            else:
                continue
            
            Times = DataFrame["Times"].to_numpy()
            Positions = DataFrame["Positions"].to_numpy()
            RFs = DataFrame["RFs"].to_numpy()
    
            
            if param1 not in Params_List:
                Params_List.append(param1)
                Master_out.append([])
              
            for i in range(len(Times)):
                time = Times[i]
                pos = Positions[i]
                if round(time+0.01, 2)%param1 == 0:
                    if pos < 0:
                        Out[1] = Out[1] + 1
                    elif pos > 0:
                        Out[0] = Out[0] + 1
                        
            Master_out[Params_List.index(param1)].append(100*Out[0]/(Out[0]+Out[1]))

        Data_1 = []
        Errs_1 = []
        Params_1 = Params_List
        for item in Master_out:
            Data_1.append(np.mean(item))
            Errs_1.append(np.std(item) / np.sqrt(len(item)))
            
        Data_array_1[a-1][b-1] = Data_1
        Errs_array_1[a-1][b-1] = Errs_1
        Params_array_1[a-1][b-1] = Params_1

os.chdir("../3_1")

for a in range(1, 6):
    for b in range(1, 6):
        U_max = round(5*a/1000000.0 + 25.0/1000000.0, 8)
        sigma = round(b/10.0, 3)

        print(str(U_max) + "   " + str(sigma))
        
        Master_out = []
        Params_List = []
        
        for filename in os.listdir(os.getcwd()):
            DataFrame = pd.read_csv(filename)
        
            Out = [0, 0]
            
            Params = DataFrame["Param1"].to_numpy()
            param1 = round(Params[0], 2) #reset time
            Params = DataFrame["Param2"].to_numpy()
            param2 = round(Params[0], 8) #U max
            Params = DataFrame["Param3"].to_numpy()
            param3 = round(Params[0], 3) #sigma
            
            if (U_max == param2) and (sigma == param3) and (param1 < 5000):
                U_index = a-1
                S_index = b-1
            else:
                continue
            
            Times = DataFrame["Times"].to_numpy()
            Positions = DataFrame["Positions"].to_numpy()
            RFs = DataFrame["RFs"].to_numpy()
    
            
            if param1 not in Params_List:
                Params_List.append(param1)
                Master_out.append([])
              
            for i in range(len(Times)):
                time = Times[i]
                pos = Positions[i]
                if round(time+0.01, 2)%param1 == 0:
                    if pos < 0:
                        Out[1] = Out[1] + 1
                    elif pos > 0:
                        Out[0] = Out[0] + 1
                        
            Master_out[Params_List.index(param1)].append(100*Out[1]/(Out[0]+Out[1]))

        Data_2 = []
        Errs_2 = []
        Params_2 = Params_List
        for item in Master_out:
            Data_2.append(np.mean(item))
            Errs_2.append(np.std(item) / np.sqrt(len(item)))
            
        Data_array_2[a-1][b-1] = Data_2
        Errs_array_2[a-1][b-1] = Errs_2
        Params_array_2[a-1][b-1] = Params_2
        
os.chdir("..")

"""
fig, axs = plt.subplots(2, sharex='col')
axs[0].errorbar(Params_1, Data_1, yerr=Errs_1, fmt='o')
axs[1].errorbar(Params_2, Data_2, yerr=Errs_2, fmt='o')
axs[0].set_ylabel("% of times UN stayed UN")
axs[1].set_ylabel("% of times 3_1 stayed 3_1")
fig.savefig("UU-33_Differences.pdf")
"""

Differences_array = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
Difference_Params_array = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
Difference_Errs_array = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]

for a in range(5):
    for b in range(5):
        Difference_Params = []
        Differences = []
        Difference_Errs = []
        
        Params_1 = Params_array_1[a][b]
        Data_1 = Data_array_1[a][b]
        Errs_1 = Errs_array_1[a][b]
        Params_2 = Params_array_2[a][b]
        Data_2 = Data_array_2[a][b]
        Errs_2 = Errs_array_2[a][b]
        
        for param in Params_1:
            if param in Params_2:
                Difference_Params.append(param)
                Differences.append(Data_1[Params_1.index(param)] - Data_2[Params_2.index(param)])
                Difference_Errs.append(Errs_1[Params_1.index(param)] + Errs_2[Params_2.index(param)])
        
        Differences_array[a][b] = Differences
        Difference_Params_array[a][b] = Difference_Params
        Difference_Errs_array[a][b] = Difference_Errs

print(Differences_array)
EquilArray = [[[26.562], [28.94], [28.86], [28.267000000000003], [27.712000000000003]], [[29.119], [28.764000000000006], [29.358], [29.316999999999997], [28.991999999999997]], [[28.971000000000004], [26.647999999999996], [29.636999999999997], [30.74], [29.502]], [[25.864], [28.3], [29.523999999999997], [29.71], [30.683999999999997]], [[28.336], [27.557999999999996], [29.113000000000003], [28.563000000000002], [31.171000000000003]]]
fig, axs = plt.subplots(ncols = 5, nrows = 5, sharex = 'all', sharey = 'all', layout='constrained', figsize = (80, 80), dpi = 80)
for a in range(5):
    for b in range(5):
        U_max = round(5*a/1000000.0 + 25.0/1000000.0, 8)
        sigma = round((b+1)/10.0, 3)
        axs[a][b].errorbar(Difference_Params_array[a][b], Differences_array[a][b], yerr=Difference_Errs_array[a][b], fmt = 'o', label = "U_max=" + str(U_max) + "; sigma=" + str(sigma))
        axs[a][b].legend(prop={"size": 50}, loc = 'lower center')
        axs[a][b].tick_params(axis='both', which='major', labelsize=75)
        axs[a][b].tick_params(axis='both', which='minor', labelsize=75)
        axs[a][b].hlines(EquilArray[a][b][0], 0, 5000, linestyles='dashed')
fig.supylabel("Differences %(UN->UN) - %(3_1->3_1)", fontsize = 100)
fig.supxlabel("Reset Time", fontsize = 100)
fig.show()
fig.savefig("UU_33_Differences_Grid.pdf")

