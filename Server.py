import pandas as pd
import haversine as hs
from haversine import Unit


class serverclass:

    """The class serverclass is used to secure all the information required 
    by each server. In this class, methods were added so that 
    the server object could perform some functionalities.

    :param coordinates: Server coordinates
    :type coordinates: Tuple of floats
    :param dfvm: Dataframe with all the user defined VMs
    :type dfvm: Pandas Dataframe
    """

    def __init__(self,coordinates, dfvm):

        self.coordinates = coordinates      #tuple with coordinates lat, lon
        self.dfvm = dfvm


    def migration_time_estimate(self, client, Gpon_speed, backhaul_distance):    #(GPON 2.5GB/s)  #(Km)

        """ The migration_time_estimate function returns the total amout of time that 
            the migration of the virtual machine takes based on an estimation formula.
            Takes into account the latency introduced by the backhaul and travel of the fiber optics.
            In addiction it also considers the time of transfering all the VM data over the speed on a GPON network

            :param client: The client object that has all the information about the client of that trip
            :type client: Object of class clientclass
            :param Gpon_speed: The bandwidth used in the Gpon infrastructure 
            :type Gpon_speed: Integer
            :param backhaul_distance: The average distance from the radio acess to the backhaul equipment 
            :type backhaul_distance: Integer

            :return: Returns the total amount of time the migration takes 
            :rtype: Integer
        """ 

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


    def calc_distance(self, client_coordinates, st_coordinates):

        """ The calc_distance function returns the distance between the 
            client and the edge server

            :param client_coordinates: The client coordinates, latitude and longitude
            :type client_coordinates: Tuple of floats
            :param st_coordinates: The edge server coordinates, latitude and longitude
            :type st_coordinates: Tuple of floats

            :return: Returns the distance between the client and the edge server station
            :rtype: Integer
        """ 

        dist = hs.haversine(client_coordinates,st_coordinates,unit=Unit.METERS)

        return dist
        
    
    def get_coordinate_server(self):

        """ The get_coordinate_server function returns edge server coordinates in a Tuple

            :return: Returns the edge server coordinates
            :rtype: Tuple
        """ 

        return self.coordinates


    #def predict_latency(self, Mte, client_velocity, lat_a, lat_b):
        
    #    distance = client_velocity * Mte  # dist(m) = m/s * s

    #    tau = (distance/ (3* pow(10,8))) * 1000  # tau(miliseconds) 

    #    lat_a_pred = lat_a + tau

    #    lat_b_pred = lat_b - tau 

    #    return lat_b_pred - lat_a_pred  # miliseconds


    #def migration_average(self):
    #    pass


