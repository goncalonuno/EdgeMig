import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sn
import matplotlib.patches as mpatches
from matplotlib import rcParams
#from brokenaxes import brokenaxes 
from natsort import index_natsorted, order_by_index

#sn.set_context("paper", font_scale = 2)


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

    ax.get_legend().remove()
    ax.legend(loc='upper right')

    ax.set_ylim(0, 25)
    ax.set_xlabel('Trips')
    ax.set_ylabel('Number of migrations')

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

    ax.get_legend().remove()
    ax.legend(loc='upper right')

    ax.set_ylim(0, 1.4)
    ax.set_xlabel('Trips')
    ax.set_ylabel('Number of migrations / KM')

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

    ax.get_legend().remove()
    ax.legend(loc='upper right')
    ax.set_ylim(0, 70)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Percentage')

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

    ax.get_legend().remove()
    ax.legend(loc='upper right')
    ax.set_ylim(0, 2)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Percentage')

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

    fig, (ax2, ax1) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [8, 1]})
    fig.subplots_adjust(hspace=0.1)

    ax2.set_title("Client Latency to Origin by Trip")

    sn.boxplot(x='TripID', y='Latency', hue="Class", palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax2)
    sn.boxplot(x='TripID', y='Latency', hue="Class", palette=['C0', 'C1','C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'], data = df, ax=ax1)

    #ax1.axhline(50, ls='--')
    #ax1.text(-0.75,50.01, "Cloud one-way latency (Best Case)", fontsize=12)

    ax1.set_ylim(0, 0.002)  # below
    ax2.set_ylim(26.564, 26.580)  # most of the data
    ax1.set_yticks([0,0.002])

    #26.567 26.580
    # hide the spines between ax1 and ax2
    sn.despine(ax=ax1)
    sn.despine(ax=ax2, bottom=True)

    ax = ax2
    d = .01  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal

    ax = ax1
    kwargs.update(transform=ax.transAxes)  # switch to the bottom axes
    ax.plot((-d, +d), (1 - d*8, 1 + d*8), **kwargs)  # bottom-left diagonal
    
    ax1.get_legend().remove()
    ax2.get_legend().remove()
    ax2.legend(loc='upper left')

    #ax1.legend_.remove()
    ax1.set_xlabel('')
    ax1.set_ylabel('')
    ax1.set_xlabel('Trips')

    ax2.legend_.set_title(None)
    #ax2.legend()
    ax2.xaxis.set_ticks_position('none') 
    ax2.set_xlabel('')
    ax2.set_ylabel('')
    ax2.set_ylabel('Latency in milliseconds')

    return fig, ax1
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

    ax.get_legend().remove()
    ax.legend(loc='upper right')

    ax.set_ylim(0, 6500)

    ax.set_xlabel('Path coordinates')
    ax.set_ylabel('Distance in meters')

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

    ax.get_legend().remove()
    ax.legend(loc='upper right')
    ax.set_ylim(0, 3.5)

    ax.set_xlabel('Trips')
    ax.set_ylabel('Data in GB/KM')

    return 1