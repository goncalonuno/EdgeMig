import pandas as pd
from datetime import datetime
import haversine as hs
from haversine import Unit


class clientclass:

    """The class clientclass is used to secure all the information required 
    by each client for doing a trip. In this class, methods were added so that 
    the client object could perform some functionalities.

    :param dftrip: Dataframe with the trips
    :type dftrip: Pandas Dataframe
    :param vm_df: Dataframe with all the user defined VMs
    :type vm_df: Pandas Dataframe
    :param df_LTE: Dataframe with all the LTE stations
    :type df_LTE: Pandas Dataframe
    :param cone: Cone aperture
    :type cone: Integer
    :param dfmigrations: Dataframe with the source and suggested destination for migration
    :type dfmigrations: Pandas Dataframe
    :param vm: Dataframe with the current virtual machine running 
    :type vm: Pandas Dataframe
    :param lte_st: Dataframe with the current LTE station that the client is connected with
    :type lte_st: Pandas Dataframe
    :param lte_df: Dataframe with all the LTE stations
    :type lte_df: Pandas Dataframe
    :param latencies: List with the latency that the user has to the source and to the target
    :type latencies: List
    :param distancies: List with the distance that the user has to the source and to the target
    :type distancies: List
    :param liststats: List with all the statistics from the migrations that occured for that client on that trip
    :type liststats: List
    :param mig_id_inc: The number of migrations that occured in that trip for that client
    :type mig_id_inc: Integer
    :param triptime: The time that the whole trip took
    :type triptime: Integer
    :param tripdistance: The distance of the whole trip
    :type tripdistance: Integer
    :param mig_under: Defines if the client is under a migration or not
    :type mig_under: Integer
    :param timeout: The current time of timeout that the client is serving
    :type timeout: Integer
    :param station_heading: The heading the station has relative to the client
    :type station_heading: Integer
    :param cone: The cone aperture
    :type cone: Integer
    :param cone_min: The minimum value for the cone aperture
    :type cone_min: Integer
    :param cone_max: The maximum value for the cone aperture
    :type cone_max: Integer

    """

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

        """The reset_vars function is responsible for cleaning up
        the variables used for each iteration from the set of virtual machine
        while evaluating each individual trip

        :param cone: Cone aperture
        :type cone: Integer
        
        :return: Returns 1 in success
        :rtype: Integer
        """

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

        """The count_coordinates function returns the 
        number of trips from the dataframe of trips. 

        :return: Returns the number of trips in the dataset
        :rtype: Integer
        """

        return self.dftrip['TripID'].count()

    def calc_triptime(self):

        """The calc_triptime function is responsible for
            calculating the total time the trip takes and update
            the triptime value of that object 

            :return: Returns the 1 in success
            :rtype: Integer
        """    

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

        """The calc_tripdistance function is responsible for
            calculating the total distance of the trip and update
            the tripdistance value of that object 

            :return: Returns the 1 in success
            :rtype: Integer
        """    

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

        """The get_vm_client function returns the virtual machine 
        that is associated to that client at that given moment

        :return: Returns the current VM of the client 
        :rtype: Pandas Dataframe
        """

        return self.vm

    def vm_time_mig(self, Gpon_speed, backhaul_distance):  #(GPON 2.5GB/s)  #(Km)

        """The vm_time_mig function is responsible for calculating
        the total time of migration taking into account the backhaul infrastructure

        :param Gpon_speed: The bandwidth used in the Gpon infrastructure 
        :type Gpon_speed: Integer
        :param backhaul_distance: The average distance from the radio acess to the backhaul equipment 
        :type backhaul_distance: Integer
        
        :return: Returns the total time the migration costs 
        :rtype: Integer
        """

        lte_st_coor = [self.lte_st['lat'].values[0], self.lte_st['lon'].values[0]]
        server_coor = [self.dfmigrations['Latitude'].values[1], self.dfmigrations['Longitude'].values[1]]

        mig_time = self.vm['Total Migration Time (ms)'].values[0] * pow(10,-3)  #seconds
        backhaul_time = (self.vm['Total Transferred Data (KB)'] * pow(10,3)) / (Gpon_speed * pow(10,9))  #seconds  
        travel_time = (( hs.haversine(lte_st_coor, server_coor, unit=Unit.METERS) + 2*backhaul_distance*1000 ) / (1.5*3*pow(10,8) ))  #seconds

        return mig_time + backhaul_time + travel_time

    def get_origin_server_id(self):

        """The get_origin_server_id function returns the 
        ID of the source edge server in which the client is currently hosted. 

        :return: Returns the ID of the edge server where the client is hosted 
        :rtype: Integer
        """

        return self.dfmigrations['ID_LTE'].values[0] 

    def get_target_server_id(self):

        """The get_target_server_id function returns the 
        ID of the target edge server to which the client 
        might actualy migrate to. 

        :return: Returns the ID of the edge server where the client might end up migrating
        :rtype: Integer
        """

        return self.dfmigrations['ID_LTE'].values[1]

    def get_coordinates(self, index_coor):

        """The get_coordinates function returns the client
        coordinates in a tuple with the latitude and longitude
        depending on the index of the mobility dataset. This makes 
        the iteration between coordinates easier. 

        :param index_coor: Index of the trips dataframe
        :type index_coor: Integer

        :return: Returns the latitude and longitude of the client
        :rtype: Tuple with floats
        """

        lat = self.dftrip['Latitude'].values[index_coor]
        lon = self.dftrip['Longitude'].values[index_coor]
        coordinates = (lat,lon)

        return coordinates

    def get_server_origin_coor(self):
        
        """The get_server_origin_coor function returns the source edge server
        coordinates in a tuple with the latitude and longitude

        :return: Returns the latitude and longitude of source edge server
        :rtype: Tuple with floats
        """

        lat = self.dfmigrations['Latitude'].values[0]
        lon = self.dfmigrations['Longitude'].values[0]
        coordinates = (lat,lon)

        return coordinates

    def get_server_target_coor(self):

        """The get_server_target_coor function returns the target edge server
        coordinates in a tuple with the latitude and longitude

        :return: Returns the latitude and longitude of target edge server
        :rtype: Tuple with floats
        """

        lat = self.dfmigrations['Latitude'].values[1]
        lon = self.dfmigrations['Longitude'].values[1]
        coordinates = (lat,lon)

        return coordinates

    def get_velocity_from_coordinate(self, coor_index):

        """The get_velocity_from_coordinate function returns the client
        velocity in meters per second depending on the index of the mobility dataset. 
        This transforms the velocity from the dataset that natively is in miles per hour
        to meters per second

        :param index_coor: Index of the trips dataframe
        :type index_coor: Integer

        :return: Returns the client velocity in meters per second
        :rtype: Integer
        """

        velocity_mph = self.dftrip['Speed'].values[coor_index]

        velocity_ms = velocity_mph * 0.44704

        return velocity_ms




   # def calc_avail_bandwidth(self, coordinate):
   #     pass