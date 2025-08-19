import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

os.chdir("data")

Data_array_1 = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
Errs_array_1 = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
Params_array_1 = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]


for a in range(1, 6):
    for b in range(1, 6):
        U_max = round(5*a/1000000.0 + 25.0/1000000.0, 8)
        sigma = round(b/10.0, 3)

        print(str(U_max) + "   " + str(sigma))
        
        Master_out = []
        Params_List = []
        
        for filename in os.listdir(os.getcwd()):

            under_list = []
            for i in range(len(filename)):
                if filename[i] == '_':
                    under_list.append(i)

            DataFrame = pd.read_csv(filename)
        
            Out = [0, 0]
            
            param1 = 100.0
            param2 = float(filename[1:under_list[0]])
            param3 = float(filename[under_list[0] + 2: under_list[1]])

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
                if time > 400000:
                    if pos < 0:
                        Out[1] = Out[1] + 1
                    elif pos > 0:
                        Out[0] = Out[0] + 1
                        
            Master_out[Params_List.index(param1)].append(100*(Out[0] - Out[1])/(Out[0]+Out[1]))

        Data_1 = []
        Errs_1 = []
        Params_1 = Params_List
        for item in Master_out:
            Data_1.append(np.mean(item))
            Errs_1.append(np.std(item) / np.sqrt(len(item)))
            
        Data_array_1[a-1][b-1] = Data_1
        Errs_array_1[a-1][b-1] = Errs_1
        Params_array_1[a-1][b-1] = Params_1

os.chdir("..")

fig, axs = plt.subplots(ncols = 1, nrows = 1, layout='constrained')

labels = []
for b in range(5):
    labels.append(str(round((b+1)/10.0, 3)))
    
colours = ["red", "orange", "green", "blue", "purple"]
used_list = []
print(Data_array_1)
for a in range(5):
    for b in range(5):
        if Data_array_1[a][b] != []:
            axs.errorbar([round(5*a/1000000.0 + 25.0/1000000.0 + (b-2)/10000000.0, 8)], Data_array_1[a][b], yerr=Errs_array_1[a][b], fmt = 'o', label = ('sigma = ' + labels[b]) if colours[b] not in used_list else '', color=colours[b])
            used_list.append(colours[b])
            
fig.supylabel("%(UN) - %(3_1) in Equilibrium")
fig.supxlabel("U_max (Staggered for Clarity)")
axs.legend()
fig.show()
fig.savefig("EquilibriumLevels_Diffs.pdf")

