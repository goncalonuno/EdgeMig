import pandas as pd
import haversine as hs
import math
from LTE import *


def get_client_source(client, dfstations):

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


def remove_cluster(df_aux):

    delete_list = list()

    for i in range(df_aux['ID_LTE'].count()):

        Lat_o = df_aux['lat'].values[i]
        Lon_o = df_aux['lon'].values[i]

        for i in range(df_aux['ID_LTE'].count()):

            Lat = df_aux['lat'].values[i]
            Lon = df_aux['lon'].values[i]
                                                                                                #raio = 500m
            if( (Lat_o != Lat and Lon_o != Lon) and ( pow(Lon-Lon_o,2) + pow(Lat-Lat_o,2) < pow(0.00753,2) ) ):

                delete_list.append(i)

    df_aux = df_aux.drop(delete_list)
    df_aux = df_aux.reset_index(drop=True)

    return df_aux


def lte_connection(client, coor_index):

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


def node_search_dist(client_coor, st_lat_lon, server_origin_coor):

    distance_target = hs.haversine(client_coor,st_lat_lon)

    dist_origin = hs.haversine(client_coor,server_origin_coor)

    if(distance_target < dist_origin - 0.1):
        return -1 

    return 1


def node_search_lat(client, coor_index, st_lat_lon):

    latency_target = get_latency(client, coor_index, st_lat_lon)

    latency_origin = client.latencies[0]

    if(latency_target < latency_origin - 0.015):
        return -1 

    return 1
