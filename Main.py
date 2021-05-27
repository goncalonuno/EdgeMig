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

    """The choose_vm function filters the dataset which has multiple vm migrations 
    by the user defined proprieties. Depending on the mode the simulation
    is running the resulting dataframe may be a set of VMs that follow the 
    specifications or a single VM from a given ID that the user introduced.
    The first situation being vm_mode = 1 and the second situation being vm_mode = 0   

    :param dfvm: Dataframe with the VMs
    :type dfvm: Pandas dataframe
    :param user_def: User definitions
    :type user_def: Object of the class UserDef
    
    :return: Returns a filtered dataframe with the VMs that will be used
    :rtype: Pandas dataframe
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

    """The setup_folders function generates the correct folders for
    outputting the results of the simulation.  

    :param user_def: User definitions
    :type user_def: Object of the class UserDef
    
    :return: Returns 1 in success
    :rtype: Integer
    """

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

    """The data_to_digest function copies the results of the simulation
    to the correct digest folders.

    :param user_def: User definitions
    :type user_def: Object of the class UserDef
    
    :return: Returns 1 in success
    :rtype: Integer
    """

    sh.copy2('./OUT/Node_Determination.xlsx', user_def.digest_path)
    sh.copy2('./OUT/Statistics.xlsx', user_def.digest_path)
    sh.copy2('./OUT/Client_path.xlsx', user_def.digest_path)

    return 1

def check_dataframes(dftrips, dfstations, df_LTE, dfvm, user_def):

    """The check_dataframes function verifies if all datasets provided exist
    and have a correct structure based on the provided header of each .csv file.
    This function is used to prevent program errors futher in the execution process
    by checking if all the information that the user used to run the simulation can actually 
    be used. 

    :param dftrips: Dataframe with the trips
    :type dftrips: Pandas dataframe
    :param dfstations: Dataframe with the edge server stations
    :type dfstations: Pandas dataframe
    :param df_LTE: Dataframe with the LTE stations
    :type df_LTE: Pandas dataframe
    :param dfvm: Dataframe with the VMs
    :type dfvm: Pandas dataframe    
    :param user_def: User definitions
    :type user_def: Object of the class UserDef
    
    :return: Returns 1 in success
    :rtype: Integer
    """

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

def simulation(user_def, dfstations, dfnode, dfpath, clientlist, stationlist): 
    
    """The simulation function is responsible for checking the main sequence of events
    that evaluates each step of the client by iterating through the multiple trips and 
    virutal machines for each coordinate of the client. On each coordinate analyzed an evaluation 
    is done to see if the migration is viable. If the suggested destination is approved by the 
    policy evaluator then the migration process occurs. Otherwise, the next coordinate will be 
    analyzed the same way, until the right opportunity appears. In the process of running the simulation 
    some data is saved and acquired, so that in the future some results about the migration mechanism can be studied.

    :param user_def: User definitions
    :type user_def: Object of the class UserDef
    :param dfstations: Dataframe with the edge server stations
    :type dfstations: Pandas dataframe
    :param dfnode: Dataframe used for saving the data required by the dynamic plot
    :type dfnode: Pandas dataframe
    :param dfvm: Dataframe used for saving the latency and distance data to the user throughout the path
    :type dfvm: Pandas dataframe
    :param clientlist: List with all the clients
    :type clientlist: List
    :param clientlist: List with all the edge server stations
    :type clientlist: List     

    :return: Returns 1 in success
    :rtype: Integer
    """

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

    return 1







if __name__ == "__main__":

    start_time = time.time()

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
                            'STO_ID': pd.Series([], dtype='int'), 'LTEO_ID': pd.Series([], dtype='int')}) 

    clientlist = list()
    stationlist = list()

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

    simulation(user_def, dfstations, dfnode, dfpath, clientlist, stationlist)

    print("Program Elapsed Time: %s " % str(datetime.timedelta(seconds = (time.time() - start_time))))

