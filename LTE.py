import pandas as pd
import haversine as hs
from haversine import Unit


def latency_backhaul():

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

    client_coor = client.get_coordinates(coor_index)
    lte_st_coor = [client.lte_st['lat'].values[0], client.lte_st['lon'].values[0]]
    backhaul_distance = 14.5

    Lat_wireless = (hs.haversine(client_coor, lte_st_coor, unit=Unit.METERS) / (3*pow(10,8))) * 1000    # miliseconds

    Lat_FO = (( hs.haversine(lte_st_coor, server_coor, unit=Unit.METERS) + 2*backhaul_distance*1000 ) / (1.5*3*pow(10,8) )) * 1000  # miliseconds

    Latency = Lat_wireless + latency_backhaul() + Lat_FO    # miliseconds


    return Latency 