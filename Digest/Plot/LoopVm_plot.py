import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sn
import matplotlib.patches as mpatches
from natsort import index_natsorted, order_by_index

#AUX FUNC
def Vm_groupby(df, group_by, aggr):

    df = df.groupby(group_by)
    df = df.agg(aggr)
    df = df.reset_index()
    df = df.reindex(index=order_by_index(df.index, index_natsorted(df['TripID'], reverse=False)))

    return df



####
    #Loop VM - Single Plot + Compare Plot (BAR/BOXPLOT)
def prep_n_mig_LoopVM(plot_dict, df_lst_files):

    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):

        dfaux = Vm_groupby(df, ['TripID', 'VmID'], {'Mig_ID':'count', 'tripdistance': 'first'})
        dfaux.rename(columns={'TripID':'TripID', 'VmID':'VmID', 'Mig_ID':'Number of Migrations', 'tripdistance': 'tripdistance'},inplace=True)
        #dfaux = Vm_groupby(dfaux, ['TripID'], {'Number of Migrations':'mean'})
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)
        
    dfconcat = pd.concat(df_aux_list) 

    return dfconcat

def n_mig_LoopVM(df):

    fig, ax = plt.subplots()
    
    #BOXPLOT
    #ax.set_title("Number of Migrations by Trip " + title)
    #sn.boxplot(x='TripID', y='Number of Migrations', hue='Class', palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax)

    #BAR
    ax.set_title("Number of Migrations by Trip")
    sn.barplot(x='TripID', y='Number of Migrations', hue='Class', palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data=df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Number of migrations')
    ax.legend()


    return 1

def normalized_n_mig_LoopVM(df):

    df["n_mig_km"] = ""

    for i in range(df['TripID'].count()):

        tripdistance = df['tripdistance'].values[i]
        n_mig = df['Number of Migrations'].values[i]

        normalized = n_mig / tripdistance

        df['n_mig_km'].values[i] = normalized

    #print(df)

    fig, ax = plt.subplots()
    
    #BOXPLOT
    #ax.set_title("Number of Migrations by Trip " + title)
    #sn.boxplot(x='TripID', y='Number of Migrations', hue='Class', palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax)

    #BAR
    ax.set_title("Number of Migrations / km  -  by Trip")
    sn.barplot(x='TripID', y='n_mig_km', hue='Class', palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data=df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Number of migrations / KM')
    ax.legend()


    return 1
####



####
    #Loop VM - Single Plot + Compare Plot
def prep_migtime_LoopVM(plot_dict, df_lst_files):

    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):

        dfaux = Vm_groupby(df, ['TripID', 'VmID'], {'Mt_real':'sum', 'triptime': 'first'})
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)

    dfconcat = pd.concat(df_aux_list)

    return dfconcat

def migtime_LoopVM(df):

    fig, ax = plt.subplots()

    ax.set_title("Time Spent Migrating vs Trip Time")

    ax.scatter(df['TripID'], df['triptime'], color='black', label='Total Trip Time')
    sn.boxplot(x='TripID', y='Mt_real', hue="Class", palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Time in Seconds')

    ax.legend()

    return 1

def percentage_migtime_LoopVM(df):

    df["Percentage_migtime"] = ""

    for i in range(df['TripID'].count()):

        triptime = df['triptime'].values[i]
        Mt_real = df['Mt_real'].values[i]

        percentage = (Mt_real * 100) / triptime

        df['Percentage_migtime'].values[i] = percentage

    #print(df)

    fig, ax = plt.subplots()

    ax.set_title("Time Spent Migrating vs Trip Time (Percentage)")

    sn.boxplot(x='TripID', y='Percentage_migtime', hue="Class", palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Percentage')

    ax.legend()

    return 1
####



####
#Loop VM - Single Plot + Compare Plot
def prep_downtime_LoopVM(plot_dict, df_lst_files):
    
    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):
        dfaux = Vm_groupby(df, ['TripID', 'VmID'], {'DT_real':'sum', 'triptime': 'first'})
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)

    dfconcat = pd.concat(df_aux_list)

    return dfconcat

def downtime_LoopVM(df):

    fig, ax = plt.subplots()

    ax.set_title("Downtime by Trip")

    sn.boxplot(x='TripID', y='DT_real', hue="Class", palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Time in milliseconds')

    ax.legend()

    return 1

def percentage_downtime_LoopVM(df):

    df["Percentage_downtime"] = ""

    for i in range(df['TripID'].count()):

        triptime = df['triptime'].values[i] * pow(10,3)
        DT_real = df['DT_real'].values[i]

        percentage = (DT_real * 100) / triptime

        df['Percentage_downtime'].values[i] = percentage

    #print(df)

    fig, ax = plt.subplots()

    ax.set_title("Downtime by Trip (Percentage)")

    sn.boxplot(x='TripID', y='Percentage_downtime', hue="Class", palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Percentage')

    ax.legend()

    return 1
####



####
    #Loop VM - Single Plot + Compare Plot
def prep_client_latency_LoopVM(plot_dict, df_lst_files):

    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):

        dfaux = Vm_groupby(df, ['TripID', 'VmID'], {'Latency':'mean'})
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)

    dfconcat = pd.concat(df_aux_list)

    return dfconcat

def client_latency_LoopVM(df):

    fig, ax = plt.subplots()

    ax.set_title("Client Latency to Origin by Trip")

    sn.boxplot(x='TripID', y='Latency', hue="Class", palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax)

    ax.set_xlabel('Path coordinates')
    ax.set_ylabel('Latency in milliseconds')
    ax.legend()

    return fig, ax
####



####
    #Loop VM - Single Plot + Compare Plot
def prep_client_distance_LoopVM(plot_dict, df_lst_files):

    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):

        dfaux = Vm_groupby(df, ['TripID', 'VmID'], {'Distance':'mean'})
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)

    dfconcat = pd.concat(df_aux_list)

    return dfconcat

def client_distance_LoopVM(df):

    fig, ax = plt.subplots()

    ax.set_title("Client Distance to Origin by Trip")

    sn.boxplot(x='TripID', y='Distance', hue="Class", palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax)

    ax.set_xlabel('Path coordinates')
    ax.set_ylabel('Distance in meters')
    ax.legend()

    return fig, ax
####



####
    #Loop VM - Single Plot + Compare Plot
def prep_mte_vs_mtr_LoopVM(plot_dict, df_lst_files):

    df_aux_list = list()
    i=0

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):

        dfaux = df[df['TripID'].values == df['TripID'].values[0]]
        dfaux = Vm_groupby(dfaux, ['TripID', 'VmID'], {'Mt_est':'first', 'Mt_real':'first'})
        dfaux.insert(0, 'Class', 'Estimate Migration Time') # + Class

        df_aux_list.append(dfaux)

        i = i + 1
        if(i == 1): break # Remove if migration estimate method is to be compared!!!!!!

    dfconcat = pd.concat(df_aux_list)

    return dfconcat

def mte_vs_mtr_LoopVM(df):

    fig, ax = plt.subplots(1,2)

    fig.suptitle("Migration Time Estimate vs Real Migration Time")

    sn.boxplot(x='TripID', y='Mt_real', data = df, ax=ax[0], color='C0')
    sn.boxplot(x='TripID', y='Mt_est', hue='Class', palette=['C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax[1])

    leg1 = mpatches.Patch(color='#1f77b4', label='Real Migration Time')
    ax[0].legend(handles=[leg1])
    ax[0].set_ylim([0, 60])
    ax[1].legend()
    ax[1].set_ylim([0, 60])
    
    for i in range(2):
        ax[i].set_xlabel('All Machines')
        ax[i].set_ylabel('Time in Seconds')
        ax[i].set_xticks([])
    
    return 1
####


####
    #Loop VM - Single Plot + Compare Plot
def prep_transferred_data_LoopVM(plot_dict, df_lst_files):

    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):
        dfaux = Vm_groupby(df, ['TripID', 'VmID'], {'transferred_dataGB':'sum', 'tripdistance': 'first'})
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)

    dfconcat = pd.concat(df_aux_list)

    return dfconcat

def transferred_data_LoopVM(df):

    fig, ax = plt.subplots()

    ax.set_title("Transferred Data by Trip")

    sn.boxplot(x='TripID', y='transferred_dataGB', hue='Class', palette=['C0','C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data=df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Data in GB')
    ax.legend()

    return 1

def normalized_transferred_data_LoopVM(df):

    df["gb_km"] = ""

    for i in range(df['TripID'].count()):

        tripdistance = df['tripdistance'].values[i]
        data = df['transferred_dataGB'].values[i]

        normalized = data / tripdistance

        df['gb_km'].values[i] = normalized


    fig, ax = plt.subplots()

    ax.set_title("Transferred Data / KM - by Trip")

    sn.boxplot(x='TripID', y='gb_km', hue='Class', palette=['C0','C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data=df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Data in GB/KM')
    ax.legend()

    return 1