import pandas as pd
import math
import matplotlib.pyplot as plt
from haversine import Unit
import haversine as hs
from natsort import index_natsorted, order_by_index


class statsclass:

    def __init__(self, Mt_real, Mt_est, DT_real, mig_id, trip_id, vm_id, lat_source_init, lat_target_init, id_lte_origin, id_lte_target, 
                dist_source_init, dist_target_init, client_heading, station_heading, cone, transferred_data, triptime, tripdistance):

        self.trip_id = trip_id
        self.vm_id = vm_id
        self.mig_id = mig_id
        self.mt_real = Mt_real
        self.mt_est = Mt_est
        self.DT_real = DT_real

        self.delta_lat_init = 0
        self.delta_lat_real_end = 0
        self.delta_lat_est_end = 0
        self.lat_source_init = lat_source_init
        self.lat_target_init = lat_target_init
        self.lat_source_end = 0
        self.lat_target_end = 0     

        self.delta_dist_init = 0
        self.delta_dist_real_end = 0 
        self.delta_dist_est_end = 0
        self.dist_source_init = dist_source_init
        self.dist_target_init = dist_target_init
        self.dist_source_end = 0
        self.dist_target_end = 0

        self.id_lte_origin = id_lte_origin
        self.id_lte_target = id_lte_target

        self.client_heading = client_heading
        self.station_heading = station_heading
        self.cone = cone

        self.transferred_data = transferred_data

        self.triptime = triptime
        self.tripdistance = tripdistance


#########################



def creatstats(client, server, coor_index):

    Mt_est = math.ceil(server.migration_time_estimate(client, 2.5, 14.5)) # seconds
    Mt_real = math.ceil(client.vm_time_mig(2.5, 14.5)) #seconds
    DT_real = math.ceil(client.vm['Downtime (ms)'].values[0])

    mig_id = client.mig_id_inc
    trip_id = client.dftrip['TripID'].values[0]
    vm_id = client.vm['Migration ID'].values[0]

    lat_source_init = client.latencies[0]
    lat_target_init = 0 - client.latencies[1]

    dist_source_init = client.distancies[0]
    dist_target_init = 0 - client.distancies[1]

    id_lte_origin = client.get_origin_server_id()
    id_lte_target = client.get_target_server_id()

    cone = client.cone
    client_heading = client.dftrip['Heading'].values[coor_index]
    station_heading = client.station_heading

    transferred_data = client.vm['Total Transferred Data (KB)'].values[0] * pow(10,-6)

    triptime = client.triptime
    tripdistance = client.tripdistance

    mig_stat = statsclass(Mt_real, Mt_est, DT_real, mig_id, trip_id, vm_id, lat_source_init, 
                          lat_target_init, id_lte_origin, id_lte_target, dist_source_init, 
                          dist_target_init, client_heading, station_heading, cone, transferred_data, 
                          triptime, tripdistance)

    client.liststats.append(mig_stat)

    return 1

def stats_collect(Mt_real, Mt_est, server, client, user_def):

    latencies = client.latencies
    distancies = client.distancies

    if(Mt_est == math.ceil(server.migration_time_estimate(client, 2.5, 14.5)) or user_def.mig_cost==0):

        delta_lat_init = latencies[1] - latencies[0]
        client.liststats[-1].delta_lat_init = delta_lat_init 

        delta_dist_init = distancies[1] - distancies[0]
        client.liststats[-1].delta_dist_init = delta_dist_init 
    
    if(Mt_real == 0):
        delta_lat_real_end = latencies[1] - latencies[0]
        client.liststats[-1].delta_lat_real_end = delta_lat_real_end
        client.liststats[-1].lat_source_end = latencies[0]
        client.liststats[-1].lat_target_end = 0 - latencies[1]

        delta_dist_real_end = distancies[1] - distancies[0]
        client.liststats[-1].delta_dist_real_end = delta_dist_real_end
        client.liststats[-1].dist_source_end = distancies[0]
        client.liststats[-1].dist_target_end = 0 - distancies[1]  

    if(Mt_est == 0):
        delta_lat_est_end = latencies[1] - latencies[0]
        client.liststats[-1].delta_lat_est_end = delta_lat_est_end

        delta_dist_est_end = distancies[1] - distancies[0]
        client.liststats[-1].delta_dist_est_end = delta_dist_est_end  

def stats_df(clientlist):

    df_stats = pd.DataFrame(columns=['TripID', 'VmID', 'Mig_ID', 'Mt_real', 'Mt_est', 'DT_real', 'delta_lat_init', 'delta_lat_real_end', 'delta_lat_est_end',
                                    'triptime', 'tripdistance', 'lat_source_init', 'lat_source_end', 'lat_target_init', 'lat_target_end','id_lte_origin', 'id_lte_target',
                                    'delta_dist_init', 'delta_dist_real_end', 'delta_dist_est_end', 
                                    'dist_source_init', 'dist_target_init', 'dist_source_end', 'dist_target_end', 'transferred_dataGB'])

    for client in clientlist:

        for migration_stat in client.liststats:

            df_stats = df_stats.append({'TripID': migration_stat.trip_id,
                                        'VmID': migration_stat.vm_id,  
                                        'Mig_ID': migration_stat.mig_id, 
                                        'Mt_real': migration_stat.mt_real, 
                                        'Mt_est': migration_stat.mt_est,
                                        'DT_real': migration_stat.DT_real,
                                        'delta_lat_init': migration_stat.delta_lat_init,
                                        'delta_lat_real_end': migration_stat.delta_lat_real_end,
                                        'delta_lat_est_end': migration_stat.delta_lat_est_end,
                                        'triptime': migration_stat.triptime,
                                        'tripdistance': migration_stat.tripdistance,
                                        'lat_source_init' : migration_stat.lat_source_init,
                                        'lat_source_end' : migration_stat.lat_source_end,
                                        'lat_target_init' : migration_stat.lat_target_init,
                                        'lat_target_end' : migration_stat.lat_target_end,
                                        'id_lte_origin' : migration_stat.id_lte_origin, 
                                        'id_lte_target' : migration_stat.id_lte_target,
                                        'delta_dist_init' : migration_stat.delta_dist_init,
                                        'delta_dist_real_end' : migration_stat.delta_dist_real_end,
                                        'delta_dist_est_end' : migration_stat.delta_dist_est_end,
                                        'dist_source_init' : migration_stat.dist_source_init,
                                        'dist_target_init' : migration_stat.dist_target_init,
                                        'dist_source_end' : migration_stat.dist_source_end,
                                        'dist_target_end' : migration_stat.dist_target_end,
                                        'transferred_dataGB' : migration_stat.transferred_data
                                        }, ignore_index=True)
    
    df_stats.insert(0, 'INDEX', df_stats.index)

    df_stats = df_stats.astype({'INDEX': int,
                                'TripID': str,
                                'VmID': int, 
                                'Mig_ID': int,
                                'Mt_real': float,
                                'Mt_est': float,
                                'DT_real': float,
                                'delta_lat_init': float,
                                'delta_lat_real_end': float,
                                'delta_lat_est_end': float,
                                'triptime': int,
                                'tripdistance': float,
                                'lat_source_init' : float,
                                'lat_source_end' : float,
                                'lat_target_init' : float,
                                'lat_target_end' : float,
                                'id_lte_origin' : str, 
                                'id_lte_target' : str,
                                'delta_dist_init': float,
                                'delta_dist_real_end': float,
                                'delta_dist_est_end': float,
                                'dist_source_init' : float,
                                'dist_target_init' : float,
                                'dist_source_end' : float,
                                'dist_target_end' : float,
                                'transferred_dataGB' : float
                                })
              
    return df_stats



#########################

def stats_df_node_dt(clientlist):

    df_stats = pd.DataFrame(columns=['TripID', 'Mig_ID','id_lte_origin', 'id_lte_target', 'dist_source_init', 'dist_target_init', 
                                    'client_heading','station_heading', 'cone'])

    for client in clientlist:

        for migration_stat in client.liststats:

            df_stats = df_stats.append({'TripID': migration_stat.trip_id, 
                                        'Mig_ID': migration_stat.mig_id, 
                                        'id_lte_origin' : migration_stat.id_lte_origin, 
                                        'id_lte_target' : migration_stat.id_lte_target,
                                        'dist_source_init' : migration_stat.dist_source_init,
                                        'dist_target_init' : 0 - migration_stat.dist_target_init,
                                        'client_heading' : migration_stat.client_heading,
                                        'station_heading' : migration_stat.station_heading,
                                        'cone' : migration_stat.cone
                                        }, ignore_index=True)
    
    df_stats.insert(0, 'INDEX', df_stats.index)

    df_stats = df_stats.astype({'INDEX': int,
                                'TripID': str, 
                                'Mig_ID': int,
                                'id_lte_origin' : str, 
                                'id_lte_target' : str,
                                'dist_source_init' : float,
                                'dist_target_init' : float,
                                'client_heading' : float,
                                'station_heading' : float,
                                'cone' : float
                                })
              
    return df_stats


def path_stats(dfpath_lat, client, coor_index):

    dfpath_lat = dfpath_lat.append({
                                    'TripID': client.dftrip['TripID'].values[0],
                                    'VmID': client.vm['Migration ID'].values[0],
                                    'Coor_index': coor_index,
                                    'Latency': client.latencies[0],
                                    'Distance': client.distancies[0],
                                    'STO_ID': client.dfmigrations['ID_LTE'].values[0]
                                    },ignore_index=True)

    dfpath_lat = dfpath_lat.astype({'TripID': str, 'VmID': int, 'Coor_index': int, 'Latency': float, 'STO_ID': int})

    return dfpath_lat 