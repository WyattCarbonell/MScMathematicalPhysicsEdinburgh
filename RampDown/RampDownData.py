import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

os.chdir("DataStorage/KymoOutputs/")

topology_data = []

for filename in os.listdir(os.getcwd()):
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        #Remove header
        f.readline()
        f.readline()
        f.readline()
        
        #Loop over all remaining lines and extract topology.
        x='a'
        top_list = []

        while(x!= ''):
            
            x = f.readline()
            position = x.rfind("_")
            
            if(x != ''):
                if position != -1:
                    topology = x[position-2:position+3:1].replace('\t', ' ')
                else:
                    topology = " UN "
                
                top_list.append(topology)
                
        topology_data.append(top_list)
                    
        #Close file
        f.close()
        
N_files = 10000
DT = 1000
percent_data = []
time_data = []

for i in range(N_files):
    UN_count = 0
    count = 0
    for j in range(len(topology_data)):
        try:
            if topology_data[j][i] == " UN ":
                UN_count = UN_count + 1
        except:
            continue
        count = count + 1
        
    percent = UN_count / count
    percent_data.append(percent)
    time_data.append(DT*i)
    
dictionary = {"Percent": percent_data, "Time": time_data}

dataframe = pd.DataFrame(data=dictionary, columns=["Time", "Percent"])

dataframe.to_csv("./RampDown_Unkinked.csv")

