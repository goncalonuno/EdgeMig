import pandas as pd
import haversine as hs
from haversine import Unit


class serverclass:

    def __init__(self,coordinates, dfvm):
        self.coordinates = coordinates      #tuple with coordinates lat, lon
        self.dfvm = dfvm


    def migration_time_estimate(self, client, Gpon_speed, backhaul_distance):    #(GPON 2.5GB/s)  #(Km)
 
        Vm_size = int(client.vm['VM_SIZE (MB)'].values[0])
        Vm_ptr = int(client.vm['Page transfer rate (MB/s)'].values[0])
        Vm_pdr = int(client.vm['Page Dirty Rate (4KB pages per second)'].values[0])
        #n = ?

        tp_td = (Vm_size *pow(10,6)) / (Vm_ptr*pow(10,6) - Vm_pdr *4*pow(10,3))

        ########

        lte_st_coor = [client.lte_st['lat'].values[0], client.lte_st['lon'].values[0]]
        server_coor = [client.dfmigrations['Latitude'].values[1], client.dfmigrations['Longitude'].values[1]]

        backhaul_time = (client.vm['Total Transferred Data (KB)'] * pow(10,3)) / (Gpon_speed * pow(10,9))  #seconds  
        travel_time = (( hs.haversine(lte_st_coor, server_coor, unit=Unit.METERS) + 2*backhaul_distance*1000 ) / (1.5*3*pow(10,8) ))  #seconds


        return tp_td + backhaul_time + travel_time  #seconds


    def calc_latency(self, client_coordinates, st_coordinates):

        Lat = (hs.haversine(client_coordinates,st_coordinates,unit=Unit.METERS) / (3*pow(10,8))) * 1000 # miliseconds

        return Lat


    def calc_distance(self, client_coordinates, st_coordinates):

        dist = hs.haversine(client_coordinates,st_coordinates,unit=Unit.METERS)

        return dist
        
        
    def predict_latency(self, Mte, client_velocity, lat_a, lat_b):
        
        distance = client_velocity * Mte  # dist(m) = m/s * s

        tau = (distance/ (3* pow(10,8))) * 1000  # tau(miliseconds) 

        lat_a_pred = lat_a + tau

        lat_b_pred = lat_b - tau 

        return lat_b_pred - lat_a_pred  # miliseconds




    def migration_average(self):
        pass

    def get_coordinate_server(self):
        
        return self.coordinates

