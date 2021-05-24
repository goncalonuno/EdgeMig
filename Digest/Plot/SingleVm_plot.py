import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sn
import matplotlib.patches as mpatches
from LoopVm_plot import *
from natsort import index_natsorted, order_by_index


#single VM Only - (NO Comparisons)
def latency_equilibrium(df, title):

    fig, ax = plt.subplots()

    ax.set_title("Migration Mechanism - Deviation relative to Latency Equilibrium " + title)

    ax.scatter(df['INDEX'], df['delta_lat_real_end'], label = 'Latency delta as migration completed')
    ax.plot(df['INDEX'], df['delta_lat_real_end'])
    ax.scatter(df['INDEX'], df['delta_lat_init'], label = 'Latency delta as migration started')
    ax.plot(df['INDEX'], df['delta_lat_init'])
    #ax.scatter(df['INDEX'], df['lat_source_init'], label = 'Latency to the source as migration started')
    #ax.plot(df['INDEX'], df['lat_source_init'])
    #ax.scatter(df['INDEX'], df['lat_target_init'], label = 'Latency to the target as migration started')
    #ax.plot(df['INDEX'], df['lat_target_init'])
    #ax.scatter(df['INDEX'], df['lat_source_end'], label = 'Latency to the source as migration completed')
    #ax.plot(df['INDEX'], df['lat_source_end'])
    #ax.scatter(df['INDEX'], df['lat_target_end'], label = 'Latency to the target as migration completed')
    #ax.plot(df['INDEX'], df['lat_target_end'])
    #ax.axhline(0,color= 'black')
    """
    i=0
    for id_lte, idtrip in zip(df['id_lte_origin'],df['TripID']):
        ax.annotate("S_ID_LTE: "+str(id_lte) + "\nTripID: " + str(idtrip), (df['INDEX'].values[i], df['lat_source_init'].values[i]))
        ax.annotate("S_ID_LTE: "+str(id_lte) + "\nTripID: " + str(idtrip), (df['INDEX'].values[i], df['lat_source_end'].values[i]))
        i = i + 1

    i=0
    for id_lte, idtrip in zip(df['id_lte_target'],df['TripID']):
        ax.annotate("T_ID_LTE: "+str(id_lte) + "\nTripID: " + str(idtrip), (df['INDEX'].values[i], df['lat_target_init'].values[i]))
        ax.annotate("T_ID_LTE: "+str(id_lte) + "\nTripID: " + str(idtrip), (df['INDEX'].values[i], df['lat_target_end'].values[i]))
        i = i + 1

    i=0
    for id_lte_o, id_lte_d in zip(df['id_lte_origin'],df['id_lte_target']):
        ax.annotate(""+str(id_lte_o) + "->" + str(id_lte_d), (df['INDEX'].values[i], df['delta_lat_init'].values[i]))
        ax.annotate(""+str(id_lte_o) + "->" + str(id_lte_d), (df['INDEX'].values[i], df['delta_lat_real_end'].values[i]))
        i = i + 1
    """
    ax.set_xlabel('Migrations Performed')
    ax.set_ylabel('Delta Latency in ms')
    ax.legend()

    return 1


#single VM Only - (NO Comparisons)
def distance_equilibrium(df, title):

    fig, ax = plt.subplots()

    ax.set_title("Migration Mechanism - Deviation relative to Distance Equilibrium " + title)
    
    ax.scatter(df['INDEX'], df['delta_dist_real_end'], label = 'Distance to equilibrium as migration completed')
    ax.plot(df['INDEX'], df['delta_dist_real_end'])
    ax.scatter(df['INDEX'], df['delta_dist_init'], label = 'Distance to equilibrium as migration started')
    ax.plot(df['INDEX'], df['delta_dist_init'])
    ax.scatter(df['INDEX'], df['dist_source_init'], label = 'Distance to the source as migration started')
    ax.plot(df['INDEX'], df['dist_source_init'])
    ax.scatter(df['INDEX'], df['dist_target_init'], label = 'Distance to the target as migration started')
    ax.plot(df['INDEX'], df['dist_target_init'])
    ax.scatter(df['INDEX'], df['dist_source_end'], label = 'Distance to the source as migration finished')
    ax.plot(df['INDEX'], df['dist_source_end'])
    ax.scatter(df['INDEX'], df['dist_target_end'], label = 'Distance to the target as migration finished')
    ax.plot(df['INDEX'], df['dist_target_end'])
    ax.axhline(0,color= 'black')

    i=0
    for id_lte, idtrip in zip(df['id_lte_origin'],df['TripID']):
        ax.annotate("S_ID_LTE: "+str(id_lte) + "\nTripID: " + str(idtrip), (df['INDEX'].values[i], df['dist_source_init'].values[i]))
        ax.annotate("S_ID_LTE: "+str(id_lte) + "\nTripID: " + str(idtrip), (df['INDEX'].values[i], df['dist_source_end'].values[i]))
        i = i + 1

    i=0
    for id_lte, idtrip in zip(df['id_lte_target'],df['TripID']):
        ax.annotate("T_ID_LTE: "+str(id_lte) + "\nTripID: " + str(idtrip), (df['INDEX'].values[i], df['dist_target_init'].values[i]))
        ax.annotate("T_ID_LTE: "+str(id_lte) + "\nTripID: " + str(idtrip), (df['INDEX'].values[i], df['dist_target_end'].values[i]))
        i = i + 1

    i=0
    for id_lte_o, id_lte_d in zip(df['id_lte_origin'],df['id_lte_target']):
        ax.annotate(""+str(id_lte_o) + "->" + str(id_lte_d), (df['INDEX'].values[i], df['delta_dist_init'].values[i]))
        ax.annotate(""+str(id_lte_o) + "->" + str(id_lte_d), (df['INDEX'].values[i], df['delta_dist_real_end'].values[i]))
        i = i + 1

    ax.set_xlabel('Migrations Performed')
    ax.set_ylabel('Delta Distance in m')
    ax.legend()

    return 1


#single VM Only - Single Plot + Compare Plot (OLD WAY)
def client_latency(df, new_fig, fig, ax, label):

    if (new_fig == 1):
        fig, ax = plt.subplots()

    ax.set_title("Client Latency Evolution by Trip ")
    ax.plot(df.index, df['Latency'], label = 'Latency to the station ' + label)
    
    df = df.drop_duplicates(subset=['TripID'])

    for i in range(len(df.index)):
        latency = df.at[df.index[i], 'Latency']
        tripid = df.at[df.index[i], 'TripID']
        ax.annotate("TripID: " + str(tripid), (df.index[i], latency))
        ax.scatter(df.index[i], latency, color='blue')

    ax.set_xlabel('Path coordinates')
    ax.set_ylabel('Latency in milliseconds')
    ax.legend()

    return fig, ax


#single VM Only - Single Plot + Compare Plot (OLD WAY)
def client_distance(df, new_fig, fig, ax, label):

    if (new_fig == 1):
        fig, ax = plt.subplots()

    ax.set_title("Evolution of Client Distance to Origin by Trip ")
    ax.plot(df.index, df['Distance'], label = 'Distance to the station ' + label)
    
    df = df.drop_duplicates(subset=['TripID'])

    for i in range(len(df.index)):
        distance = df.at[df.index[i], 'Distance']
        tripid = df.at[df.index[i], 'TripID']
        ax.annotate("TripID: " + str(tripid), (df.index[i], distance))
        ax.scatter(df.index[i], distance, color='blue')

    ax.set_xlabel('Path coordinates')
    ax.set_ylabel('Distance in meters')
    ax.legend()

    return fig, ax




####
    #single VM - Single Plot + Compare Plot
def prep_n_mig(plot_dict, df_lst_files):

    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):

        dfaux = Vm_groupby(df, ['TripID'], {'Mig_ID':'count'})
        dfaux.rename(columns={'TripID':'TripID', 'Mig_ID':'Number of Migrations'},inplace=True)
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)
        
    dfconcat = pd.concat(df_aux_list) 

    return dfconcat

def n_mig(df):

    fig, ax = plt.subplots()

    ax.set_title("Number of Migrations by Trip ")
    sn.barplot(x='TripID', y='Number of Migrations', hue='Class', palette=['C0','C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data=df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Number of migrations')
    ax.legend()

    return 1
####



####
    #single VM - Single Plot + Compare Plot
def prep_migtime(plot_dict, df_lst_files):

    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):

        dfaux = Vm_groupby(df, ['TripID'], {'Mt_real':'sum', 'triptime': 'first'})
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)

    dfconcat = pd.concat(df_aux_list)    

    return dfconcat

def migtime(df):

    fig, ax = plt.subplots()

    ax.set_title("Time Spent Migrating vs Trip Time ")

    ax.scatter(df['TripID'], df['triptime'], label = 'Total Trip Time', color='black')
    sn.barplot(x='TripID', y='Mt_real', hue='Class', palette=['C0','C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data=df, ax=ax)
    
    ax.set_xlabel('Trips')
    ax.set_ylabel('Time in Seconds')
    ax.legend()

    return 1
####



####
    #single VM - Single Plot + Compare Plot
def prep_downtime(plot_dict, df_lst_files):

    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):
        dfaux = Vm_groupby(df, ['TripID'], {'DT_real':'sum'})
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)

    dfconcat = pd.concat(df_aux_list)

    return dfconcat

def downtime(df):

    fig, ax = plt.subplots()

    ax.set_title("Downtime by Trip")

    sn.barplot(x='TripID', y='DT_real', hue='Class', palette=['C0','C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data=df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Time in milliseconds')
    ax.legend()

    return 1
####



####
    #single VM - Single Plot + Compare Plot
def prep_mte_vs_mtr(plot_dict, df_lst_files):

    df_aux_list = list()
    i = 0

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):

        dfaux = df[df['TripID'].values == df['TripID'].values[0]]
        dfaux = Vm_groupby(dfaux, ['TripID'], {'Mt_est':'first', 'Mt_real':'first'})
        dfaux.insert(0, 'Class', 'Estimate Migration Time')  # + Class

        df_aux_list.append(dfaux)

        i = i + 1
        if(i==1): break  # Remove if migration estimate method is to be compared!!!!!!

    dfconcat = pd.concat(df_aux_list)

    return dfconcat

def mte_vs_mtr(df):

    fig, ax = plt.subplots(1,2)

    fig.suptitle("Migration Time Estimate vs Real Migration Time")

    sn.barplot(x='TripID', y='Mt_real', data=df, ax=ax[0])
    sn.barplot(x='TripID', y='Mt_est', hue='Class', palette=['C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data=df, ax=ax[1])

    leg1 = mpatches.Patch(color='#1f77b4', label='Real Migration Time')
    ax[0].legend(handles=[leg1])
    ax[0].set_ylim([0, 60])
    ax[1].legend()
    ax[1].set_ylim([0, 60])

    for i in range(2):
        ax[i].set_xlabel('Single Machine')
        ax[i].set_ylabel('Time in Seconds')
        ax[i].set_xticks([])

    return 1
####


####
    #single VM - Single Plot + Compare Plot
def prep_transferred_data(plot_dict, df_lst_files):

    df_aux_list = list()

    for Class, df  in zip(plot_dict['Classes'], df_lst_files):
        dfaux = Vm_groupby(df, ['TripID'], {'transferred_dataGB':'sum'})
        dfaux.insert(0, 'Class', Class)

        df_aux_list.append(dfaux)

    dfconcat = pd.concat(df_aux_list)
    
    return dfconcat

def transferred_data(df):

    fig, ax = plt.subplots()

    ax.set_title("Transferred Data by Trip")

    sn.barplot(x='TripID', y='transferred_dataGB', hue='Class', palette=['C0','C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data=df, ax=ax)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Data in GB')
    ax.legend()

    return 1