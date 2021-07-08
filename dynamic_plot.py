import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import math
import time
import matplotlib as mpl 
from matplotlib import rcParams

mpl.rcParams['animation.ffmpeg_path'] = r'C:\\Program Files\\ffmpeg\\ffmpeg.exe'

rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False


# First set up the figure, the axis, and the plot element we want to animate
#fig = plt.figure(figsize=(25.6,14.4))
#fig = plt.figure(figsize=(19.2,10.8))
fig = plt.figure()
ax = plt.axes()
ax.set(xlim=(-83.39,-82.82), ylim=(39.92, 40.29))
line, = ax.plot([], [], lw=2)




# initialization function: plot the background of each frame
def init():

    """ The init function initiates the data that will be plotted dynamically

        :return: Returns the line where the data will be plotted
        :rtype: List of Line2D
    """

    line.set_data([], [])
    return line,


def plot_process(dftrips,dfstations,lock):

    """ The plot_process function is responsible for starting the plotting
        procedure that it will then be animated.

        :param dftrips: Dataframe with the trips
        :type dftrips: Pandas dataframe
        :param dfstations: Dataframe with the edge server stations
        :type dfstations: Pandas dataframe
        :param lock: Multiprocessing lock for accessing memory
        :type lock: Multiprocessing lock

        :return: Returns 1 in case of success
        :rtype: Integer
    """ 

    ani = FuncAnimation(fig, Animate, init_func=init, fargs=(dftrips,dfstations,lock,), frames=5000, save_count=5000, interval=1000)
                                                                                                                     #interval=1000
    #FFwriter = animation.FFMpegWriter(fps=30, bitrate=30000, extra_args=['-vcodec', 'libx264'])
    #ani.save('C:\\Users\\Gonçalo\\Desktop\\PlotDynamic\\basic_animation.mp4', writer=FFwriter)
    #ani.save('Y:\\Área Comum\\Gonçalo (Simulation)\\Video OUT\\basic_animation.mp4', writer=FFwriter)

    plt.show()

    return 1


def Animate (i, dftrips, dfstations, lock):

    """ The Animate function is responsible for plotting the data 
        that is being saved in real time when running the simulation

        :param i: Frame number
        :type i: Integer
        :param dftrips: Dataframe with the trips
        :type dftrips: Pandas dataframe
        :param dfstations: Dataframe with the edge server stations
        :type dfstations: Pandas dataframe
        :param lock: Multiprocessing lock for accessing memory
        :type lock: Multiprocessing lock

        :return: Returns 1 in case of success
        :rtype: Integer
    """ 

    plt.cla()
    ax.set(xlim=(-83.39,-82.82), ylim=(39.92, 40.29))

    try: 
        lock.acquire()
        dfnode = pd.read_csv("./OUT/plot_dynamic.csv")
        lock.release()
    except:
        print('erro!')
    
    #Map
    plt.title("Migration Mechanism - Dynamic Plot")
    plt.scatter(dfstations.lon, dfstations.lat, s=5, label='Stations')
    plt.scatter(dftrips.Longitude, dftrips.Latitude, s=2, label='Mobility Path', color='black')

    #Client Path
    plt.scatter(dfnode['C_LON'], dfnode['C_LAT'], label='Client Coordinates', color='orange')
    
    #Origin
    lte_lon = dfstations.loc[dfstations.ID_LTE == dfnode.iloc[-1]['STO_ID']]['lon']
    lte_lat = dfstations.loc[dfstations.ID_LTE == dfnode.iloc[-1]['STO_ID']]['lat']
    plt.plot([dfnode.iloc[-1]['STO_LON'],dfnode.iloc[-1]['C_LON']],[dfnode.iloc[-1]['STO_LAT'], dfnode.iloc[-1]['C_LAT']], color='green', linewidth=3, label='Origin')
    plt.annotate("ID_LTE: " + str(int(dfnode.iloc[-1]['STO_ID'])), (lte_lon,lte_lat) )

    #Migration 
    if(dfnode['Migration Occurance'].values[-1] == 1):
        plt.plot([dfnode.iloc[-1]['C_LON'], dfnode.iloc[-1]['STT_LON']], [dfnode.iloc[-1]['C_LAT'], dfnode.iloc[-1]['STT_LAT']], color='red', linewidth=4, label='Migration')
       
    #Cone Min
    coor_cone_min = heading_to_coordinate(dfnode['C_LAT'].values[-1],dfnode['C_LON'].values[-1], dfnode['Cone_Min'].values[-1], 0.08)
    cone_min_lon = coor_cone_min[1]
    con_min_lat = coor_cone_min[0]
    plt.plot([cone_min_lon, dfnode.iloc[-1]['C_LON']],[con_min_lat, dfnode.iloc[-1]['C_LAT']], color='blue', label='Cone')

    #Cone Max
    coor_cone_max = heading_to_coordinate(dfnode['C_LAT'].values[-1],dfnode['C_LON'].values[-1], dfnode['Cone_Max'].values[-1], 0.08)
    cone_max_lon = coor_cone_max[1]
    con_max_lat = coor_cone_max[0]
    plt.plot([cone_max_lon, dfnode.iloc[-1]['C_LON']],[con_max_lat, dfnode.iloc[-1]['C_LAT']], color='blue')

    
    #Client Heading
    coor_heading = heading_to_coordinate(dfnode['C_LAT'].values[-1],dfnode['C_LON'].values[-1], dfnode['C_Heading'].values[-1], 0.06)
    coor_heading_lon = coor_heading[1]
    coor_heading_lat = coor_heading[0]
    plt.plot([coor_heading_lon, dfnode.iloc[-1]['C_LON']],[coor_heading_lat, dfnode.iloc[-1]['C_LAT']], color='pink', label='Heading')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    
    return 1


def heading_to_coordinate(o_lat, o_lon, angle, dist):

    """ The heading_to_coordinate function is responsible for converting
        a heading value into a coordinate  

        :param o_lat: Latitude
        :type o_lat: Float
        :param o_lon: Longitude
        :type o_lon: Float
        :param angle: Heading angle
        :type angle: Float
        :param dist: Distance from the provided coordinate
        :type dist: Float

        :return: Returns a list with the converted latitude and longitude 
        :rtype: List
    """ 

    #1Q
    if(angle >= 0 and angle <= 90):
        lon = o_lon + math.sin(math.radians(angle)) * dist
        lat = o_lat + math.cos(math.radians(angle)) * dist
    #4Q
    if(angle > 90 and angle < 180):
        lon = o_lon + math.cos(math.radians(angle-90)) * dist 
        lat = o_lat - math.sin(math.radians(angle-90)) * dist
    #3Q
    if(angle >= 180 and angle <= 270):
        lon = o_lon - math.sin(math.radians(angle-180)) * dist
        lat = o_lat - math.cos(math.radians(angle-180)) * dist
    #2Q
    if(angle > 270 and angle < 360):
        lon = o_lon - math.cos(math.radians(angle-270)) * dist 
        lat = o_lat + math.sin(math.radians(angle-270)) * dist

    return [lat, lon]


def df_dynamic_plot(client, dfnode, coor_index, ret_node, lock):

    """ The df_dynamic_plot function is responsible adding the newly generated
        data to the dataframe that will be used by the dynamic plot.

        :param client: The client object that has all the information about the client of that trip
        :type client: Object of class clientclass
        :param dfnode: Dataframe used for saving the data required by the dynamic plot
        :type dfnode: Pandas dataframe
        :param coor_index: Index of the coordinates from the trips dataframe
        :type coor_index: Integer
        :param ret_node: Defines if the given coordinate has no possible migration destination
        :type ret_node: Integer
        :param lock: Multiprocessing lock for accessing memory
        :type lock: Multiprocessing lock

        :return: Returns a dataframe with the new data added at the end
        :rtype: Pandas Dataframe
    """ 

    if(ret_node == -1):
        lat_target = -1
        lon_target = -1
        ID_target = -1
    else:
        lat_target = client.dfmigrations['Latitude'].values[1]
        lon_target = client.dfmigrations['Longitude'].values[1]
        ID_target = client.dfmigrations['ID_LTE'].values[1]
    
    dfnode = dfnode.append({
                            'C_LAT': float(client.get_coordinates(coor_index)[0]),
                            'C_LON': float(client.get_coordinates(coor_index)[1]),
                            'STO_LAT': float(client.dfmigrations['Latitude'].values[0]),
                            'STO_LON': float(client.dfmigrations['Longitude'].values[0]),
                            'STO_ID': int(client.dfmigrations['ID_LTE'].values[0]),
                            'STT_LAT': float(lat_target),
                            'STT_LON': float(lon_target),
                            'STT_ID': int(ID_target), 
                            'Cone_Max': float(client.cone_max),
                            'Cone_Min': float(client.cone_min),
                            'Migration Occurance': int(client.mig_under),
                            'C_Heading': float(client.dftrip['Heading'].values[coor_index])
                            },ignore_index=True)

    dfnode = dfnode.astype({'C_LAT': float, 'C_LON': float, 'STO_LAT': float, 'STO_LON': float, 
                            'STO_ID': int, 'STT_LAT': float, 'STT_LON': float, 'STT_ID': int,
                            'Cone_Max': float, 'Cone_Min': float, 'Migration Occurance': int, 
                            'C_Heading': float})

    lock.acquire()
    dfnode.to_csv('./OUT/plot_dynamic.csv', index=False)
    lock.release()

    return dfnode