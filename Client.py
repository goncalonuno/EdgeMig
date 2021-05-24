import pandas as pd
from datetime import datetime
import haversine as hs
from haversine import Unit


class clientclass:

    def __init__(self,dftrip, vm_df, df_LTE, cone):
        self.dftrip = dftrip
        self.dfmigrations = pd.DataFrame({  
                                            'TripID': pd.Series([], dtype='str'),
                                            'Latitude': pd.Series([], dtype='float'),
                                            'Longitude': pd.Series([], dtype='float'),
                                            'ID_LTE': pd.Series([], dtype='int')
                                        })
        self.vm = 0  #dataframe vm with only one vm data
        self.vm_df = vm_df
        self.lte_st = 0  #dataframe station with only one station data
        self.lte_df = df_LTE
        self.latencies = [-1,-1]
        self.distancies = [-1,-1]
        self.liststats = list()
        self.mig_id_inc = 0          
        self.triptime = 0
        self.tripdistance = 0
        self.mig_under = 0
        self.timeout = 0
        self.station_heading = 0
        self.cone = cone
        self.cone_min = 0
        self.cone_max = 0



    def reset_vars(self, cone):

        self.dfmigrations = pd.DataFrame({  
                                            'TripID': pd.Series([], dtype='str'),
                                            'Latitude': pd.Series([], dtype='float'),
                                            'Longitude': pd.Series([], dtype='float'),
                                            'ID_LTE': pd.Series([], dtype='int')
                                        })
        self.mig_id_inc = 0          
        self.latencies = [-1,-1]
        self.distancies = [-1,-1]
        self.mig_under = 0
        self.timeout = 0
        self.station_heading = 0
        self.cone = cone
        self.cone_min = 0
        self.cone_max = 0

        return 1

    def count_coordinates(self):
        
        return self.dftrip['TripID'].count()

    def calc_triptime(self):
        
        date_init = (self.dftrip['TimeStamp'].values[0]).split()
        date_end = (self.dftrip['TimeStamp'].values[-1]).split()

        Timestamp_init = date_init[3]
        Timestamp_end = date_end[3]
        
        fmt = '%H:%M:%S'
        tstamp1 = datetime.strptime(Timestamp_init, fmt)
        tstamp2 = datetime.strptime(Timestamp_end, fmt)

        if tstamp1 > tstamp2:
            td = tstamp1 - tstamp2
        else:
            td = tstamp2 - tstamp1

        self.triptime = int(round(td.total_seconds()))  # trip time in seconds  
    
        return 1

    def calc_tripdistance(self):

        total_distance = 0

        for i in range(self.dftrip['TripID'].count()):

            lat1 = self.dftrip['Latitude'].values[i]
            lon1 = self.dftrip['Longitude'].values[i]

            if(i+1 != self.dftrip['TripID'].count()):
                lat2 = self.dftrip['Latitude'].values[i+1]
                lon2 = self.dftrip['Longitude'].values[i+1]

                dist = hs.haversine((lat1,lon1), (lat2,lon2))

                total_distance = total_distance + dist
        
        self.tripdistance = total_distance      # trip distance in KM 

        return 1
        
    def get_vm_client(self):

        return self.vm

    def vm_time_mig(self, Gpon_speed, backhaul_distance):  #(GPON 2.5GB/s)  #(Km)
        
        lte_st_coor = [self.lte_st['lat'].values[0], self.lte_st['lon'].values[0]]
        server_coor = [self.dfmigrations['Latitude'].values[1], self.dfmigrations['Longitude'].values[1]]

        mig_time = self.vm['Total Migration Time (ms)'].values[0] * pow(10,-3)  #seconds
        backhaul_time = (self.vm['Total Transferred Data (KB)'] * pow(10,3)) / (Gpon_speed * pow(10,9))  #seconds  
        travel_time = (( hs.haversine(lte_st_coor, server_coor, unit=Unit.METERS) + 2*backhaul_distance*1000 ) / (1.5*3*pow(10,8) ))  #seconds

        return mig_time + backhaul_time + travel_time

    def get_origin_server_id(self):

        return self.dfmigrations['ID_LTE'].values[0] 

    def get_target_server_id(self):
        return self.dfmigrations['ID_LTE'].values[1]

    def get_coordinates(self, index_coor):

        lat = self.dftrip['Latitude'].values[index_coor]
        lon = self.dftrip['Longitude'].values[index_coor]
        coordinates = (lat,lon)

        return coordinates

    def get_server_origin_coor(self):

        lat = self.dfmigrations['Latitude'].values[0]
        lon = self.dfmigrations['Longitude'].values[0]
        coordinates = (lat,lon)

        return coordinates

    def get_server_target_coor(self):

        lat = self.dfmigrations['Latitude'].values[1]
        lon = self.dfmigrations['Longitude'].values[1]
        coordinates = (lat,lon)

        return coordinates

    def get_velocity_from_coordinate(self, coor_index):
        
        velocity_mph = self.dftrip['Speed'].values[coor_index]

        velocity_ms = velocity_mph * 0.44704

        return velocity_ms




    def calc_avail_bandwidth(self, coordinate):
        pass