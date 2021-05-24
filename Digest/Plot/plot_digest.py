import pandas as pd
import matplotlib.pyplot as plt
from LoopVm_plot import *
from SingleVm_plot import *
import sys
import os.path
from natsort import index_natsorted, order_by_index


node_path = 'Node_Determination.xlsx' #Not used for now 
stats_path = 'Statistics.xlsx'
latency = 'Client_path.xlsx'



def plot_loopVM(plot_dict):

    df_list_stats = list()
    df_list_path = list()

    for path in plot_dict['Paths_Stats']:
        df_list_stats.append(pd.read_excel(path + stats_path))
    
    for path in plot_dict['Paths_Stats']:
        df_list_path.append(pd.read_excel(path + latency))


    ## Number of migrations ##
    df = prep_n_mig_LoopVM(plot_dict, df_list_stats)
    n_mig_LoopVM(df)
    normalized_n_mig_LoopVM(df)

    ## Client Latency ## 
    df = prep_client_latency_LoopVM(plot_dict, df_list_path)
    client_latency_LoopVM(df)

    ## Client Distance ## 
    df = prep_client_distance_LoopVM(plot_dict, df_list_path)
    client_distance_LoopVM(df)

    ## Migration Time Estimate vs Real Migration Time ##
    df = prep_mte_vs_mtr_LoopVM(plot_dict, df_list_stats)
    mte_vs_mtr_LoopVM(df)

    ## Migration Time ##
    df = prep_migtime_LoopVM(plot_dict, df_list_stats)
    migtime_LoopVM(df)
    percentage_migtime_LoopVM(df)

    ## Downtime ##
    df = prep_downtime_LoopVM(plot_dict, df_list_stats)
    downtime_LoopVM(df)
    percentage_downtime_LoopVM(df)

    ## Transferred Data ##
    df = prep_transferred_data_LoopVM(plot_dict, df_list_stats)
    transferred_data_LoopVM(df)
    normalized_transferred_data_LoopVM(df)

    return 1
    

def plot_SingleVM(plot_dict):

    df_list_stats = list()
    df_list_path = list()

    for path in plot_dict['Paths_Stats']:
        df_list_stats.append(pd.read_excel(path + stats_path))
    
    for path in plot_dict['Paths_Stats']:
        df_list_path.append(pd.read_excel(path + latency))


    ## Number of migrations ##
    df = prep_n_mig(plot_dict, df_list_stats)
    n_mig(df)


    ## Migration Time Estimate vs Real Migration Time ##
    df = prep_mte_vs_mtr(plot_dict, df_list_stats)
    mte_vs_mtr(df)


    ## Migration Time ##
    df = prep_migtime(plot_dict, df_list_stats)
    migtime(df)


    ## Downtime ##
    df = prep_downtime(plot_dict, df_list_stats)
    downtime(df)

    ## Transferred Data ##
    df = prep_transferred_data(plot_dict, df_list_stats)
    transferred_data(df)


    #####   Special Plots
    
    for i in range(len(df_list_stats)):

        latency_equilibrium(df_list_stats[i], plot_dict['Classes'][i])

        distance_equilibrium(df_list_stats[i], plot_dict['Classes'][i])

    for i in range(len(df_list_path)-1):
        fig, ax = client_latency(df_list_path[i], 1, 0, 0, plot_dict['Classes'][i])
        client_latency(df_list_path[i+1], 0, fig, ax, plot_dict['Classes'][i+1] )
        fig, ax = client_distance(df_list_path[i], 1, 0, 0, plot_dict['Classes'][i])
        client_distance(df_list_path[i+1], 0, fig, ax, plot_dict['Classes'][i+1] )

    if ( len(df_list_path) == 1 ):
        client_latency(df_list_path[0], 1, 0, 0, plot_dict['Classes'][0])
        client_distance(df_list_path[0], 1, 0, 0, plot_dict['Classes'][0])
    
    #####
    
    return 1


def user_specs():

    plot_dict = dict()

    mode =  input("Enter 0 for single plot or enter 1 for loop plot:")

    if(int(mode)==0):
        folder = 'SingleVM/'
    elif(int(mode)==1):
        folder = 'LoopVM/'
    else:
        print('Invalid mode was entered. Only 0 or 1 is accepted.')
        sys.exit(2) 
        
    classes = input("Enter the identifiers of each test seperated by a space (ex: Cone_180 Cone_60):").split()

    paths_stats = input("Enter the name of the folders of each test seperated by a space (ex:test1 test2):").split()
    
    if(len(classes) != len(paths_stats)):
        print('Missmatch between number of identifiers and folders')
        sys.exit(2)
    
    for i in range(len(paths_stats)):

        paths_stats[i] = '../' + folder +  paths_stats[i] + '/'

        if(not(os.path.isfile(paths_stats[i]+stats_path)) or not(os.path.isfile(paths_stats[i]+latency))):

            print('Missing files to plot! exiting...')
            sys.exit(2)
    
    plot_dict['Classes'] = classes
    plot_dict['Paths_Stats'] = paths_stats

    return plot_dict



if __name__ == "__main__":

    plot_dict = user_specs()

    #Example Compare Plot
    #plot_dict = { 'Classes': ['Cone 180', 'Cone 60', 'Remove Cluster', 'Timeout'],
    #              'Paths_Stats': ['../LoopVM/A/', '../LoopVM/B/', '../LoopVM/C/', '../LoopVM/D/']
    #            }

    #Cone_180 Cone_60 Remove_Cluster Timeout
    #../LoopVM/A/ ../LoopVM/B/ ../LoopVM/C/ ../LoopVM/D/

    #Example Single Plot
    #plot_dict = { 'Classes': ['Cone 180'],
    #              'Paths_Stats': ['../SingleVM/Test/'],
    #            }

    plot_loopVM(plot_dict)

    #plot_SingleVM(plot_dict)


    plt.show()

