import pandas as pd
import haversine as hs
import math
from LTE import *


def get_client_source(client, dfstations):

    """The get_client_source function finds the closest edge server to the 
    user by comparing the distance between the client coordinates and the 
    coordinates of the edge server station. This is used to find the first edge server
    as it starts the trip

    :param client: The client object that has all the information about the client of that trip
    :type client: Object of class clientclass
    :param dfstations: Dataframe with the edge server stations
    :type dfstations: Pandas dataframe
    
    :return: Returns 1 in success
    :rtype: Integer
    """

    client_coor = client.get_coordinates(0)
    listaux = list()
    
    for j in range (dfstations['ID_LTE'].count()):

        Lat_s = dfstations['lat'].values[j]
        Lon_s = dfstations['lon'].values[j]

        loc2 = (Lat_s,Lon_s)

        #function to calculate distance in (km)
        distance = hs.haversine(client_coor,loc2)
        listaux.append(distance)

    index = listaux.index(min(listaux))

    Lat_m = dfstations['lat'].values[index]
    Lon_m = dfstations['lon'].values[index]

    if(client.dfmigrations.empty):

        client.dfmigrations = client.dfmigrations.append({
                                                        'TripID': str(client.dftrip['TripID'].values[0]),
                                                        'Latitude': float(Lat_m), 
                                                        'Longitude': float(Lon_m), 
                                                        'ID_LTE': int(dfstations['ID_LTE'].values[index]) 
                                                        },ignore_index=True)

        client.dfmigrations = client.dfmigrations.astype({
                                                        'TripID': str,
                                                        'Latitude': float, 
                                                        'Longitude': float, 
                                                        'ID_LTE': int 
                                                        })

    return 1


def node_search(client, coor_index, dfstations, user_def):

    """The node_search function suggest a possible destination 
    based on the client's heading through the use of a search cone 
    and by taking into account the latency or distance that possible destination. 

    :param client: The client object that has all the information about the client of that trip
    :type client: Object of class clientclass
    :param coor_index: Index of the trips dataframe
    :type coor_index: Integer
    :param dfstations: Dataframe with the edge server stations
    :type dfstations: Pandas dataframe
    :param user_def: User definitions
    :type user_def: Object of the class UserDef
    
    :return: Returns 1 it finds a possible destination or it returns -1 if it can't find a possible destination
    :rtype: Integer
    """

    client_coor = client.get_coordinates(coor_index)
    server_origin_coor = client.get_server_origin_coor()
    client_heading = client.dftrip['Heading'].values[coor_index]
    cone = client.cone
    cone_min = client.cone_min
    cone_max = client.cone_max
    df_aux = pd.DataFrame({'ID_LTE': pd.Series([], dtype='int'),
                            'lat': pd.Series([], dtype='float'),
                            'lon': pd.Series([], dtype='float'),
                            'Distance': pd.Series([], dtype='float'),
                            'Latency': pd.Series([], dtype='float'),
                            'Station Heading': pd.Series([], dtype='float')})

    for j in range (dfstations['ID_LTE'].count()):

        Lat_s = dfstations['lat'].values[j]
        Lon_s = dfstations['lon'].values[j]

        st_lat_lon = (Lat_s,Lon_s)
        st_lon_lat = (Lon_s - client_coor[1], Lat_s - client_coor[0])

        #Special case where client and station overlap: don't count with it
        if(st_lon_lat[0] == 0 and st_lon_lat[1] == 0):
            continue

        #1 First Quadrant
        if (st_lon_lat[0] >= 0 and st_lon_lat[1] >= 0):
            
            st_angle = math.degrees(math.atan2(st_lon_lat[1], st_lon_lat[0]))
            st_heading = 90 - st_angle

        #2 Second Quadrant
        if (st_lon_lat[0] < 0 and st_lon_lat[1] > 0):
            
            st_angle = math.degrees(math.atan2(st_lon_lat[1], abs(st_lon_lat[0])))
            st_heading = st_angle + 270

        #3 Third Quadrant
        if (st_lon_lat[0] <= 0 and st_lon_lat[1] <= 0):
            
            st_angle = math.degrees(math.atan2(abs(st_lon_lat[1]),abs(st_lon_lat[0])))
            st_heading = 270 - st_angle

        #4 Fouth Quadrant
        if (st_lon_lat[0] > 0 and st_lon_lat[1] < 0):
            
            st_angle = math.degrees(math.atan2(abs(st_lon_lat[1]), st_lon_lat[0]))
            st_heading = 90 + st_angle

        #Cone special cases (Discontinuation)
        if ( ( client_heading - (cone/2) ) < 0  or  ( client_heading + (cone/2) ) > 359 ):

            if ( ( client_heading - (cone/2) ) < 0 ):

                if ( st_heading > cone_min and st_heading < 360 or st_heading >=0 and st_heading < cone_max ):      #This station is inside the cone!!!!
                    
                    if ((user_def.lat_dist==1 and node_search_lat(client, coor_index, st_lat_lon) == 1) or
                        (user_def.lat_dist==2 and node_search_dist(client_coor, st_lat_lon, server_origin_coor) == 1)):

                        distance = hs.haversine(client_coor,st_lat_lon)
                        latency = get_latency(client, coor_index, st_lat_lon)
                        df_aux = df_aux.append({'ID_LTE': int(dfstations['ID_LTE'].values[j]), 'lat': Lat_s, 'lon': Lon_s ,'Distance': distance, 'Latency': latency, 'Station Heading': st_heading},ignore_index=True)

            if ( ( client_heading + (cone/2) ) > 359 ):

                if( st_heading >= 0 and st_heading < cone_max or st_heading > cone_min and st_heading < 360):   #This station is inside the cone!!!!
                    
                    if ((user_def.lat_dist==1 and node_search_lat(client, coor_index, st_lat_lon) == 1) or
                        (user_def.lat_dist==2 and node_search_dist(client_coor, st_lat_lon, server_origin_coor) == 1)):

                        distance = hs.haversine(client_coor,st_lat_lon)
                        latency = get_latency(client, coor_index, st_lat_lon)
                        df_aux = df_aux.append({'ID_LTE': int(dfstations['ID_LTE'].values[j]), 'lat': Lat_s, 'lon': Lon_s ,'Distance': distance, 'Latency': latency, 'Station Heading': st_heading},ignore_index=True)


        #Regular cone cases
        if (not(( client_heading - (cone/2) ) < 0  or  ( client_heading + (cone/2) ) > 359)):

            if (st_heading > cone_min and st_heading < cone_max):       #This station is inside the cone!!!!
                
                if ((user_def.lat_dist==1 and node_search_lat(client, coor_index, st_lat_lon) == 1) or
                    (user_def.lat_dist==2 and node_search_dist(client_coor, st_lat_lon, server_origin_coor) == 1)):

                    distance = hs.haversine(client_coor,st_lat_lon)
                    latency = get_latency(client, coor_index, st_lat_lon)
                    df_aux = df_aux.append({'ID_LTE': int(dfstations['ID_LTE'].values[j]), 'lat': Lat_s, 'lon': Lon_s ,'Distance': distance, 'Latency': latency, 'Station Heading': st_heading},ignore_index=True)


    if(df_aux.empty):
        return -1

    df_aux = df_aux.astype({'ID_LTE': int, 'lat': float, 'lon': float, 'Distance': float, 'Latency': float, 'Station Heading': float})

    if(user_def.lat_dist==1):
        df_aux = df_aux[df_aux.Latency == df_aux.Latency.min()]
    elif(user_def.lat_dist==2):
        df_aux = df_aux[df_aux.Distance == df_aux.Distance.min()]
    df_aux = df_aux.reset_index(drop=True)

    ### AQUI PARA BAIXO
    if( df_aux['ID_LTE'].values[0] == client.dfmigrations['ID_LTE'].values[0] ):
        return -1


    if (client.dfmigrations['ID_LTE'].count() == 2):
        
        client.dfmigrations = client.dfmigrations.drop([1], axis='index')
        client.dfmigrations = client.dfmigrations.reset_index(drop=True)

    client.dfmigrations = client.dfmigrations.append({
                                                    'TripID': str(client.dftrip['TripID'].values[0]),
                                                    'Latitude': float(df_aux['lat'].values[0]), 
                                                    'Longitude': float(df_aux['lon'].values[0]), 
                                                    'ID_LTE': int(df_aux['ID_LTE'].values[0]) 
                                                    },ignore_index=True)

    client.dfmigrations = client.dfmigrations.astype({
                                                    'TripID': str,
                                                    'Latitude': float, 
                                                    'Longitude': float, 
                                                    'ID_LTE': int 
                                                    })
    
    client.station_heading = df_aux['Station Heading'].values[0]

    return 1


def cone_determination(client, coor_index):

    """The cone_determination function determines the cone that the client
    will have when running the trip. 

    :param client: The client object that has all the information about the client of that trip
    :type client: Object of class clientclass
    :param coor_index: Index of the trips dataframe
    :type coor_index: Integer
    
    :return: Returns 1 in success
    :rtype: Integer
    """

    client_heading = client.dftrip['Heading'].values[coor_index]
    cone = client.cone

    #Cone special cases (Discontinuation)
    if ( ( client_heading - (cone/2) ) < 0  or  ( client_heading + (cone/2) ) > 359 ):

        if ( ( client_heading - (cone/2) ) < 0 ):

            cone_min = (client_heading - (cone/2)) + 360
            cone_max = client_heading + (cone/2)

        if ( ( client_heading + (cone/2) ) > 359 ):
            
            cone_min = client_heading - (cone/2)
            cone_max = (client_heading + (cone/2)) - 360

    #Regular cone cases
    if (not(( client_heading - (cone/2) ) < 0  or  ( client_heading + (cone/2) ) > 359)):

        cone_min = client_heading - (cone/2)
        cone_max = client_heading + (cone/2)

    client.cone_min = cone_min
    client.cone_max = cone_max

    return 1


def remove_cluster(dfstations):

    """The remove_cluster function removes clusters of edge servers.
    This is to prevent migrations between edge servers that are to close together
    and mitigate uncessary migrations. 

    :param dfstations: Dataframe with the edge server stations
    :type dfstations: Pandas dataframe
    
    :return: Returns the filtered edge server dataframe 
    :rtype: Pandas Dataframe
    """

    delete_list = list()

    for i in range(dfstations['ID_LTE'].count()):

        Lat_o = dfstations['lat'].values[i]
        Lon_o = dfstations['lon'].values[i]

        for i in range(dfstations['ID_LTE'].count()):

            Lat = dfstations['lat'].values[i]
            Lon = dfstations['lon'].values[i]
                                                                                                #raio = 500m
            if( (Lat_o != Lat and Lon_o != Lon) and ( pow(Lon-Lon_o,2) + pow(Lat-Lat_o,2) < pow(0.00753,2) ) ):

                delete_list.append(i)

    dfstations = dfstations.drop(delete_list)
    dfstations = dfstations.reset_index(drop=True)

    return dfstations


def lte_connection(client, coor_index):

    """The lte_connection function find the closest LTE station 
    to the client.

    :param client: The client object that has all the information about the client of that trip
    :type client: Object of class clientclass
    :param coor_index: Index of the trips dataframe
    :type coor_index: Integer
    
    :return: Returns 1 in success
    :rtype: Integer
    """

    client_coor = client.get_coordinates(coor_index)
    listaux = list()
    
    for j in range (client.lte_df['ID_LTE'].count()):

        Lat_s = client.lte_df['lat'].values[j]
        Lon_s = client.lte_df['lon'].values[j]

        loc2 = (Lat_s,Lon_s)

        #function to calculate distance in (km)
        distance = hs.haversine(client_coor,loc2)
        listaux.append(distance)

    index = listaux.index(min(listaux))

    client.lte_st = client.lte_df.iloc[[index]]

    return 1


#TESTING
"""
def node_search_close(client, coor_index, dfstations):

    client_coor = client.get_coordinates(coor_index)
    listaux = list()
    
    for j in range (dfstations['ID_LTE'].count()):

        Lat_s = dfstations['lat'].values[j]
        Lon_s = dfstations['lon'].values[j]

        loc2 = (Lat_s,Lon_s)

        #function to calculate distance in (km)
        distance = hs.haversine(client_coor,loc2)
        listaux.append(distance)

    index = listaux.index(min(listaux))

    if( dfstations['ID_LTE'].values[index] == client.dfmigrations['ID_LTE'].values[0] ):
        return -1

    if (client.dfmigrations['ID_LTE'].count() == 2):
        
        client.dfmigrations = client.dfmigrations.drop([1], axis='index')
        client.dfmigrations = client.dfmigrations.reset_index(drop=True)

    client.dfmigrations = client.dfmigrations.append({
                                                    'TripID': str(client.dftrip['TripID'].values[0]),
                                                    'Latitude': float(dfstations['lat'].values[index]), 
                                                    'Longitude': float(dfstations['lon'].values[index]), 
                                                    'ID_LTE': int(dfstations['ID_LTE'].values[index]) 
                                                    },ignore_index=True)

    client.dfmigrations = client.dfmigrations.astype({
                                                    'TripID': str,
                                                    'Latitude': float, 
                                                    'Longitude': float, 
                                                    'ID_LTE': int 
                                                    })

    return 1
"""

def node_search_dist(client_coor, st_lat_lon, server_origin_coor):

    """The node_search_dist function checks if the distance to 
    the target edge server is within range when comparing it to the distance
    that the client has to the source.

    :param client_coor: The client coordinates
    :type client_coor: Tuple of floats
    :param st_lat_lon: The target station coordinates
    :type st_lat_lon: Tuple of floats
    :param server_origin_coor: The source station coordinates
    :type server_origin_coor: Tuple of floats

    :return: Returns 1 if the destination is in range or it returns -1 if if the destination is not in range
    :rtype: Integer
    """

    distance_target = hs.haversine(client_coor,st_lat_lon)

    dist_origin = hs.haversine(client_coor,server_origin_coor)

    if(distance_target < dist_origin - 0.1):
        return -1 

    return 1


def node_search_lat(client, coor_index, st_lat_lon):

    """The node_search_lat function checks if the latency to 
    the target edge server is within range when comparing it to the lantecy
    that the client has to the source.

    :param client: The client object that has all the information about the client of that trip
    :type client: Object of class clientclass
    :param coor_index: Index of the trips dataframe
    :type coor_index: Integer
    :param st_lat_lon: The target station coordinates
    :type st_lat_lon: Tuple of floats

    :return: Returns 1 if the destination is in range or it returns -1 if if the destination is not in range
    :rtype: Integer
    """

    latency_target = get_latency(client, coor_index, st_lat_lon)

    latency_origin = client.latencies[0]

    if(latency_target < latency_origin - 0.015):    #latency_origin > latency_target + 0.015 
        return -1 

    return 1
