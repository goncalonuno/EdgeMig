import pandas as pd
import haversine as hs
from haversine import Unit


def policy_evaluator(server, client, coor_index, user_def):

    latencies = client.latencies
    distancies = client.distancies

    #Predict Latency (pre_lat <= 0) TODO 
    #Mte = server.migration_time_estimate(client, 2.5, 14.5)
    #pred_lat = server.predict_latency(Mte, client.get_velocity_from_coordinate(coor_index), latencies[0], latencies[1])
    
    # TODO: Add more policies:
    #                           Migration time threshold
    #                           Migration time AVG / ARIMA / FIRST DERIVITIVE
    #                           Check if migration is worthwhile (remove clustered servers, migration cost)
    #                           Improve Predict lat by adding AVG or ARIMA
    #                           Add bandwith to user as concern in qos
    

    if(user_def.timeout == 1):
        if(client.timeout!= 0):
            client.timeout = client.timeout - 1
        elif(client.timeout == 0):
            client.timeout = 0
    

    if ( (user_def.lat_dist==1 and (latencies[1] - latencies[0]) <= 0) or ( user_def.lat_dist==2 and (distancies[1] - distancies[0]) <= 0)):

        if(user_def.timeout==1 and client.timeout==0):
            return True         #Migrate

        if(user_def.timeout==0):
            return True         #Migrate

    else:
        return False        #Don't Migrate