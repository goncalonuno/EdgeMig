import pandas as pd
import haversine as hs
from haversine import Unit


def latency_backhaul():

    """ The latency_backhaul function calculates the total amount of time
        the backhaul introduces as latency between the client and the source edge server.

        :return: Returns the total amount of time in milliseconds
        :rtype: Integer
    """

    Gpon = 4.5
    Ue = 2
    Radio_interface = 5.5
    eNodeB = 2
    Cell_backhaul = 5
    RAN_backhual = 2
    IPsec = 2
    Core = 1
    Epc = 0.5
    ServiceLAN = 1.5
    Isp = 0.5

    lat = Gpon + Ue + Radio_interface + eNodeB + Cell_backhaul + RAN_backhual + IPsec + Core + Epc + ServiceLAN + Isp # miliseconds

    return lat


def get_latency(client, coor_index, server_coor):

    """ The get_latency function returns the latency between
        the client and a given edge server depending on the provided 
        coordinates server_coor. Takes into account the latency introduced 
        by the backhaul wireless comunication and fiber optics

        :param client: The client object that has all the information about the client of that trip
        :type client: Object of class clientclass
        :param coor_index: Index of the trips dataframe
        :type coor_index: Integer
        :param server_coor: Index of the trips dataframe
        :type server_coor: Integer

        :return: Returns the total amount of latency between the client and the edge server  
        :rtype: Integer
    """ 

    client_coor = client.get_coordinates(coor_index)
    lte_st_coor = [client.lte_st['lat'].values[0], client.lte_st['lon'].values[0]]
    backhaul_distance = 14.5

    Lat_wireless = (hs.haversine(client_coor, lte_st_coor, unit=Unit.METERS) / (3*pow(10,8))) * 1000    # miliseconds

    Lat_FO = (( hs.haversine(lte_st_coor, server_coor, unit=Unit.METERS) + 2*backhaul_distance*1000 ) / (1.5*3*pow(10,8) )) * 1000  # miliseconds

    Latency = Lat_wireless + latency_backhaul() + Lat_FO    # miliseconds


    return Latency 