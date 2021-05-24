import pandas as pd
from Client import clientclass
from Server import serverclass
from Stats import *
from LTE import *
from NodeDiscovery import *
from policy import *
from dynamic_plot import *
from user import *
from multiprocessing import Process
import multiprocessing
import os.path
import os
import shutil as sh

import time
import datetime
import sys


def choose_vm(dfvm, user_def):

    """This is the choose vm function!

    :param dfvm: dataframe with the VMs
    :param user_def: User definitions 
    
    :return: Returns a filtered dataframe of the VM's

    """

    if(user_def.vm_mode == 0):

        dfvm = dfvm[dfvm['Migration ID'].values == user_def.vm_id]

        dfvm = dfvm.reset_index(drop=True)

    elif(user_def.vm_mode == 1):

        dfvm = dfvm[dfvm['Migration Technique'].values == user_def.migtype]

        dfvm = dfvm[dfvm['Workload'].values == user_def.benchmark]

        dfvm = dfvm[dfvm['Page transfer rate (MB/s)'].values == user_def.PTR]

        dfvm = dfvm.reset_index(drop=True)

    return dfvm

def setup_folders(user_def):

    if(not os.path.isdir('./Digest/LoopVM')):
        os.makedirs('./Digest/LoopVM')

    if(not os.path.isdir('./Digest/SingleVM')):
        os.makedirs('./Digest/SingleVM')

    if(not os.path.isdir(user_def.digest_path)):
        os.makedirs(user_def.digest_path)

    if(not os.path.isdir('./OUT')):
        os.makedirs('./OUT')

    for files in os.listdir('./OUT'):
        os.remove(os.path.join('./OUT', files))

    return 1

def data_to_digest(user_def):

    sh.copy2('./OUT/Node_Determination.xlsx', user_def.digest_path)
    sh.copy2('./OUT/Statistics.xlsx', user_def.digest_path)
    sh.copy2('./OUT/Client_path.xlsx', user_def.digest_path)
    return 1

def check_dataframes(dftrips, dfstations, df_LTE, dfvm, user_def):

    trips = ['TripID', 'TimeStamp', 'Speed', 'Acceleration', 'Heading', 'HeadingChange', 'Latitude', 'Longitude']
    stations = ['ID_LTE', 'radio', 'lat', 'lon']
    vm = ['Migration ID', 'Migration Technique', 'Workload', 'Page Dirty Rate (4KB pages per second)', 'VM_SIZE (MB)', 
          'Page transfer rate (MB/s)', 'Total Migration Time (ms)', 'Downtime (ms)', 'Total Transferred Data (KB)']

    list_df = [trips, stations, stations, vm]

    trips_hd = dftrips.columns.values.tolist()
    stations_hd = dfstations.columns.values.tolist()
    lte_hd = df_LTE.columns.values.tolist()
    vm_hd = dfvm.columns.values.tolist()

    list_hd = [trips_hd, stations_hd, lte_hd, vm_hd]

    flag = 0

    for df in list_df:
        
        for column in df: #

            for hd in list_hd:

                for column_hd in hd: #
                    
                    if(column_hd == column):
                        flag = 1
                        break

                if (flag == 0):
                    print('Dataset has wrong header sintaxe\n\tCheck header: ', hd)
                    sys.exit(2)

                if(flag == 1):
                    flag = 0
                    break
        
        list_hd.pop(0)

    list_vm = ['Migration ID', 'Migration Technique', 'Workload', 'Page Dirty Rate (4KB pages per second)']
    list_user = [user_def.vm_id, user_def.migtype, user_def.benchmark, user_def.PTR]

    for vm_def, usr_def in zip(list_vm, list_user):

        if(dfvm.loc[dfvm[vm_def] == usr_def][vm_def].empty):
            print('User definitions not found in the provided dataframes\n\t Definition error: ', vm_def)
            sys.exit(2)

    return 1 

start_time = time.time()

if __name__ == "__main__":

    #Setup user definitions
    if(len(sys.argv)<=1):
        print('Missing Parameters:\n\tTo run default mode enter: main.py -d\n\tTo get help enter: main.py -h')
        sys.exit(1)
    argv = sys.argv[1:]
    user_def_dict = handle_user_def (argv)
    user_def = UserDef(user_def_dict)
    setup_folders(user_def)

    #define and initilize the dataframes and lists
    dftrips = pd.read_csv("./Datasets/Mobility/" + user_def.dftrips_path)
    dfstations = pd.read_csv("./Datasets/Network/" + user_def.dfstations_path)
    df_LTE = pd.read_csv("./Datasets/Network/" + user_def.df_LTE_path)
    dfvm = pd.read_csv("./Datasets/Vm/" + user_def.dfvm_path)
    check_dataframes(dftrips, dfstations, df_LTE, dfvm, user_def)

    dfnode = pd.DataFrame({'C_LAT': pd.Series([], dtype='float'),'C_LON': pd.Series([], dtype='float'),
                           'STO_LAT': pd.Series([], dtype='float'), 'STO_LON': pd.Series([], dtype='float'), 
                           'STO_ID': pd.Series([], dtype='int'),'STT_LAT': pd.Series([], dtype='float'), 
                           'STT_LON': pd.Series([], dtype='float'), 'STT_ID': pd.Series([], dtype='int'),
                           'Cone_Max': pd.Series([], dtype='float'), 'Cone_Min': pd.Series([], dtype='float'),
                           'Migration Occurance': pd.Series([], dtype='int'), 'C_Heading': pd.Series([], dtype='float')})

    dfpath = pd.DataFrame({'TripID': pd.Series([], dtype='str'), 'VmID': pd.Series([], dtype='int'), 
                            'Coor_index': pd.Series([], dtype='int'), 'Latency': pd.Series([], dtype='float'), 
                            'STO_ID': pd.Series([], dtype='int')}) 

    clientlist = list()
    stationlist = list()
    latencies = list()
    distancies = list()

    #client list
    if(user_def.trip_max > dftrips['TripID'].nunique()):
        user_def.trip_max = dftrips['TripID'].nunique()
    for id in range(user_def.trip_min, user_def.trip_max + 1):      
        dftrip = dftrips[dftrips['TripID']=='T-'+str(id)]
        vm_df = choose_vm(dfvm, user_def)
        client = clientclass(dftrip, vm_df, df_LTE, user_def.cone)
        clientlist.append(client)

    #serverlist 
    for id in range(dfstations['ID_LTE'].count()):
        server = serverclass((dfstations['lat'].values[id],dfstations['lon'].values[id]),dfvm)  
        stationlist.append(server)
    if(user_def.rem_cluster == 1):
        dfstations = remove_cluster(dfstations)
    
    #Plot Process
    if(user_def.dynamic_plot == 1):
        lock = multiprocessing.Lock()
        process = Process(target=plot_process, args=(dftrips,dfstations,lock))
        plt_dynamic = 0


    for client in clientlist:

        print(client.dftrip['TripID'].values[0])

        client.calc_triptime()
        client.calc_tripdistance()

        #print(client.vm_df)
        for i in range(0, client.vm_df['Migration ID'].count()):
        #for i in range(0, 10):

            client.vm = client.vm_df.iloc[[i]]
            print(i)

            client.reset_vars(user_def.cone)                        #reset vars do cliente

            get_client_source(client, dfstations)                   #give dfmigrations the first source 
            server = stationlist[client.get_origin_server_id()]     #find the first origin server for that client

            lte_connection(client, 0)                               #find the first lte_st for that client

            for coor_index in range(client.count_coordinates()):
                
                cone_determination(client, coor_index)
                lte_connection(client, coor_index)
                client.latencies[0] = get_latency(client, coor_index, client.get_server_origin_coor())
                client.distancies[0] = server.calc_distance(client.get_coordinates(coor_index), client.get_server_origin_coor())

                if(client.mig_under == 0):
                    ret_node = node_search(client, coor_index, dfstations, user_def)      #-1 correspondes to not finding a posible destination

                if(ret_node != -1):
                    client.latencies[1] = get_latency(client, coor_index, client.get_server_target_coor())
                    client.distancies[1] = server.calc_distance(client.get_coordinates(coor_index), client.get_server_target_coor())

                if(ret_node != -1 and client.mig_under == 0 and policy_evaluator(server, client, coor_index, user_def)):

                    client.mig_under = 1
                
                    Mt_est = math.ceil(server.migration_time_estimate(client, 2.5, 14.5)) # seconds
                    Mt_real = math.ceil(client.vm_time_mig(2.5, 14.5))  #seconds
                    if(user_def.mig_cost == 0):
                        Mt_est = 0
                        Mt_real = 0
                    elapsed = 0 
                    
                    if (Mt_est >= Mt_real):
                        elapsed = Mt_est
                    elif (Mt_real >= Mt_est):
                        elapsed = Mt_real
                    
                    if(user_def.timeout == 1):
                        client.timeout = Mt_real + user_def.timeout_multiplier * Mt_real
                    
                    client.mig_id_inc = client.mig_id_inc + 1

                    creatstats(client, server, coor_index)

                if(user_def.dynamic_plot == 1):    
                    dfnode = df_dynamic_plot(client, dfnode, coor_index, ret_node, lock)
                    if(plt_dynamic==0):
                        process.start()
                        plt_dynamic = 1

                dfpath = path_stats(dfpath, client, coor_index) 

                if(client.mig_under == 1 and ret_node != -1):

                    #function stats to collect all data during migration
                    stats_collect(Mt_real, Mt_est, server, client, user_def)
                    
                    if(elapsed == 0 ):
                        
                        client.mig_under = 0
                        
                        # Apagar primeira linha do dfmigrations -> same as saying: migration happend
                        client.dfmigrations = client.dfmigrations.drop([0], axis='index')
                        client.dfmigrations = client.dfmigrations.reset_index(drop=True)
                        server = stationlist[client.get_origin_server_id()]
                    
                    elapsed = elapsed - 1
                    Mt_est = Mt_est - 1
                    Mt_real = Mt_real - 1

    if(user_def.dynamic_plot == 1):
        process.join()   

    #Save statistics
    df_statistics = stats_df(clientlist)
    df_statistics.to_excel('./OUT/Statistics.xlsx', index=False, engine='xlsxwriter')

    df_stat_node = stats_df_node_dt(clientlist)
    df_stat_node.to_excel('./OUT/Node_Determination.xlsx', index=False, engine='xlsxwriter')

    dfpath.to_excel('./OUT/Client_path.xlsx', index=False, engine='xlsxwriter')

    #Copy data to digest path
    data_to_digest(user_def)

    print("Program Elapsed Time: %s " % str(datetime.timedelta(seconds = (time.time() - start_time))))

