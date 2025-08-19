import numpy as np
import pandas as pd
import argparse

def GradExp(sigma, mu, x, U):
    return -U*(x-mu)*np.exp(-(x-mu)**2/(2*sigma**2))/((sigma**3)*np.sqrt(2*np.pi))

def Step(x0, gamma, sigma, mu, U, left_bound, right_bound, timestep, temp, rng):
    
    #Letting m=1
    rf = np.power(10.0, 9)*np.sqrt(2*temp*1.380649*np.power(10.0, -23)*timestep/gamma)*rng.normal(loc=0, scale=1)
    
    #Move the particle forward in time
    x = x0 - (1/gamma)*GradExp(sigma, mu, x0, U) + rf
    
    if x < left_bound: 
        #reset the position
        x = left_bound
        
    elif x > right_bound:
        #reset the position
        x = right_bound
    
    return [x, rf]
    
def main():
    #Parse Input
    parser = argparse.ArgumentParser()
    parser.add_argument("Parameter1")
    parser.add_argument("Parameter2")
    parser.add_argument("Parameter3")
    parser.add_argument("SimNumber")
    args = parser.parse_args()
    
    Param1 = float(args.Parameter1)
    Param2 = 5*float(args.Parameter2)/1000000.0 + 25.0/1000000.0
    Param3 = float(args.Parameter3)/10.0
    SimNum = args.SimNumber

    timestep = 0.01
    total_time = 500000
    reset_time = Param1
    
    Rg_ratio_UN_3_1 = 1.7
    
    sigma = Param3
    mu = 0
    U = Param2
    temp = 300
    gamma = 1
    
    starting_config = 'UN'
    starting_x = 1.5
    
    if starting_config == 'UN':
        starting_x = 1.5
    elif starting_config == '3_1':
        starting_x = -starting_x / Rg_ratio_UN_3_1
    else:
        print("ERROR: Invalid starting configuration")
        exit
    
    right_bound = 3
    left_bound = -right_bound
    
    steps_before_reset = reset_time / timestep
    total_steps = total_time / timestep
    number_of_resets = 100
    
    rng = np.random.default_rng()
    
    initial_conditions = [starting_x, gamma, sigma, mu, U, left_bound, right_bound, timestep, temp, rng]
    x, gamma, sigma, mu, U, left_bound, right_bound, timestep, temp, rng = initial_conditions
    
    
    #Data Storage Variables
    x_list = []
    time_list = []
    rf_list = []
    param_list1 = []
    param_list2 = []
    param_list3 = []
    
    current_time = 0
    
    #Primary loop
    for i in range(int(number_of_resets)):
        
        rng = np.random.default_rng()
        
        #Execute steps before resetting
        for j in range(int(steps_before_reset)):
            if round(current_time + timestep, 2)%reset_time == 0:
                x_list.append(x)
                time_list.append(current_time)
                current_time = current_time + timestep
                x, rf = Step(x, gamma, sigma, mu, U, left_bound, right_bound, timestep, temp, rng)
                rf_list.append(rf)
                param_list1.append(Param1)
                param_list2.append(Param2)
                param_list3.append(Param3)
            else:
                current_time = current_time + timestep
                x, rf = Step(x, gamma, sigma, mu, U, left_bound, right_bound, timestep, temp, rng)
        #Reset
        x, gamma, sigma, mu, U, left_bound, right_bound, timestep, temp, rng = initial_conditions
    
    #Export Data
    dictionary = {"Times": time_list,
              "Positions": x_list,
              "RFs": rf_list,
              "Param1": param_list1,
              "Param2": param_list2,
              "Param3": param_list3}

    dataframe = pd.DataFrame(data=dictionary, columns=["Times", "Positions", "RFs", "Param1", "Param2", "Param3"])

    dataframe.to_csv("./WalkData_" + str(SimNum) + ".csv")
    
if __name__ == '__main__':
    main()
    print('done')
