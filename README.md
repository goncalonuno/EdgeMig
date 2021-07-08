# EdgeMig
Python simulator for exploring migration policies of virtual machines over a network of edge servers based on the mobility of a user.

## Table of contents

- [Description](#description)
- [What's included](#whats-included)
- [Prerequisites](#prerequisites)
- [How to run the project](#how-to-run-the-project)
	- [How to run the simulation](#how-to-run-the-simulation)
	- [How to run the plotting program](#how-to-run-the-plotting-program)
	- [How the results presented were obtained? ](#how-the-results-presented-were-obtained)
- [Project Documentation](#project-documentation)
- [How to contribute to this project?](#how-to-contribute-to-this-project)
- [Creator](#creator)
- [Acknowledgments](#acknowledgments)
- [Citations](#citations)
- [Copyright and license](#copyright-and-license)


## Description

EdgeMig is a project that envisions a service that can let the user access and change between multiple operating systems through its smartphone or low powered laptop running in an offsite edge server, breaking the computation barrier created by the physical terminal in hand.  In addiction, the client can now access it's machines anywhere with the perceived sensation of accessing them locally with a low latency interaction.  This can be achieved by migrating the machines closer to the location of the client accordingly, while the user has its own mobility within the network. The 5G infrastructure will aid this kind of on-demand service by offering a low latency and high bandwidth experience to the user. 

However, a couple of problems can be found with this type of service such as the lag perceived by the user and the mobility between networks introduced by the given individual. These virtual machines need to be migrated accordingly, depending on the user location, so that the user has a seamless transition between Edge servers without interrupting the remote connection. Three main questions are brought up when it comes to the live migration of virtual machines: "Where to migrate?", "How to migrate?" and "When to migrate?". 

In order to solve and study these problems this simulator was developed, EdgeMig was created to explore migration policies, heuristics and migration mechanisms when associated to a mobility pattern of multiple users over a network of edge servers. The main principle of this project is to develop migration policies that can help determine the appropriate destination for the migration of virtual machines according to the path and movement of the user, as well as the time for realizing the migration.  

The simulator can be adapted to work with other mobility datasets, network datasets and VM's datasets from the ones provided.  In addiction, the simulator allows the possibility of modifying and implementing new policies and rules that can then be evaluated and compared between each other with some proposed metrics.

The required datasets and their structure will be described in further detail in the section [Prerequisites](#prerequisites). However, with a dataset for mobility, a dataset for the network and a dataset with migrations of virtual machines, the output generated from the simulator are multiple .csv files that contain the results of such migrations for multiple user trips in a city. This is the required information to be plotted in a separate python program that is also provided. The running procedure will be revealed with more detail in the section [How to run the project](#how-to-run-the-project). 

The main current migration policy implemented is based on the heading of the user with a search cone that suggest at each instant the destination of the migration, some flexibility to the size of the cone is provided and depending on the size of the cone the number of migrations change with a return of lower latency to the edge server, but with a higher backhaul overhead. 

Other migration policies were also added to provide some data to be compared and analyzed.  One of the policies was the introduction of a  timeout after each migration based on the cost of migration as the time required to realize such task. The other policy tries to remove some redundancy within the network of edge servers by removing neighbouring servers that are too close together.

The data created by the simulator is then treated by a python program that presents some statistics:
- Client latency to the source edge serve by trip
- Client distance to the source edge server  by trip
- Downtime to the client by trip
- Total migration time spent by trip
- Total number of migration performed            
- Total data transfered by trip 

Click in the GIF to the see full video on Youtube:

<p align="center">
	<a href="https://www.youtube.com/embed/EvU-FeJlyOg"><img src="https://i.imgflip.com/5b5oi3.gif" title="Youtube"/></a>
</p>

## What's included

In the following schematic it is possible to have a brief overview over the structure of the project.  The simulator is located in the root directory `./EdgeMig`  and it can be ran by executing the `Main.py`, for more details about the running procedure refer to the section [How to run the simulation](#how-to-run-the-simulation) . 

The datasets are located in the `./EdgeMig/Datasets` directory separated by single folders (`./Mobility`  `./Network`  `./Vm`) that carry the correspondent datasets. Important to note that the datasets must be inside these folders so that the simulator can use the data. For more details about the structure of the dataset refer to the section [Prerequisites](#prerequisites).

In the `./EdgeMig/Digest` path, the folders `./LoopVM` and `./SingleVM` will be created upon running the simulation and inside them new folders will be generated with a user defined name, in order to save the result of a given run of the simulation. Depending on the mode that the simulation is ran, the results generated will be copied from the path `./EdgeMig/OUT/` to either the  `./LoopVM` or `./SingleVM` folder within the user defined folder (`./EdgeMig/Digest/<SingleVM or LoopVM>/<user defined name>`). With this logic the most recent results will be saved in the `./EdgeMig/OUT/`, however  by the time the simulation is re-run the results inside the  `./EdgeMig/OUT/` path will be overwritten.  For that reason the path `./EdgeMig/Digest/<SingleVM or LoopVM>/`  has all the history of the results from the multiple runs of the simulations never to be overwritten. This done to then plot all the results from the simulations with the provided plotting program, providing a comparison view between different simulation runs. 

The plotting program can be found in the directory `./EdgeMig/Digest/Plot/` and it can be ran by executing the `plot_digest.py`program, for more information on how to run the plotting program refer to the section [How to run the plotting program](#how-to-run-the-plotting-program).

As refers previously the path `./EdgeMig/OUT` contains the current results after a single execution of a simulation. It is recommended to maintain this workflow structure to prevent failures while executing the provided programs.

```
EdgeMig/
|
└── Datasets/
|	|
|	├── Mobility/
|    	│    └── DACT_E-Dataset.csv
|    	|
|    	└── Network/
|    	|    ├── Network_Edge.csv
|    	|    └── Network_LTE.csv
|	|
|    	└── Vm/
|            └── Vm_dataset_raw.csv
|
└── Digest/
|	|
|	└── LoopVM/
|	|    └── <Multiple Result Folders>/
|	|
|	└── LoopVM/
|	|    └── <Multiple Result Folders>/
|	|
|	└── Plot/
|	     ├── LoopVm_plot.py
|	     ├── SingleVm_plot.py
|	     └── plot_digest.py 		 
|
└── OUT/
|      └── <Multiple Result Files>/
|
├── Main.py
├── Client.py
├── Server.py
├── policy.py
├── user.py
├── LTE.py
├── dynamic_plot.py
├── NodeDiscovery.py
└── Stats.py
```

## Prerequisites

For running this project some python libraries are required to be installed:

    pip install pandas
    pip install haversine
    pip install natsort
    pip install matplotlib

After the presented libraries are installed it is important to have the datasets required with the appropriate structure and inside the correct paths so that the simulation program can work properly.

For the mobility dataset [\[3\]](#citations) it is necessary to have the .csv file inside the directory `./EdgeMig/Datasets/Mobility/` and following columns names are required:
| Column name | Description |  Mandatory  |  
|--|--|--|
|TripID  | The id of a trajectory | Yes |
|TimeStep| The record number for a point of a trajectory | No |
|TimeStamp| The timestamp for a point of a trajectory (ex: Wed Jul 24 15:58:22 EDT 2013) | Yes|
|Speed| The ground velocity (mph)| Yes|
|Acceleration| The rate of change of speed ($m/s^2$)| Yes |
|Heading| The bearing which is a value between 0 and 359 | Yes |
|HeadingChange| The change of bearing from the last observation | Yes |
|Latitude| The latitude coordinate of GPS observation (Decimal Degrees) | Yes |
|Longitude| The longitude coordinate of GPS observation (Decimal Degrees) | Yes |
|Annotation| Expert annotation which specifies the end point of a segment | No |
|SegmentType| The type of a segment | No|

For the network and LTE dataset [\[4\]](#citations) it is necessary to have the .csv file inside the directory `./EdgeMig/Datasets/Network/`  and following columns names are required:
| Column name | Description |  Mandatory  |  
|--|--|--|
|ID_LTE | The id of the location | Yes |
|radio| The technology employed in that location  | Yes |
|lat| The latitude coordinate of GPS observation (Decimal Degrees) | Yes|
|lon| The longitude coordinate of GPS observation (Decimal Degrees)| Yes|

For the VM dataset [\[5\]](#citations) it is necessary to have the .csv file inside the directory `./EdgeMig/Datasets/Vm/`  and following columns names are required:
| Column name | Description |  Mandatory  |  
|--|--|--|
|Migration ID | The id of the virtual machine associated to the migration  | Yes |
|Migration Technique| Technique for migrating the vm (ex: original [pre-copy], compressed, etc...)  | Yes |
|Workload| The benchmark the machine was running when the migration occured | Yes|
|Available Network Bandwidth (mbps)| Available network Bandwidth when the migration occurred| No|
|Page Dirty Rate (4KB pages per second)| Page dirty rate of the virtual machine while migrating| Yes|
|VM_SIZE (MB)| The full size of the virtual machine | Yes|
|Page transfer rate (MB/s)| Page transfer rate of the virtual machine while migrating| Yes|
|Total Migration Time (ms)| Total time spent while migrating | Yes|
|Downtime (ms)| Total downtime for migrating the machine| Yes|
|Total Transferred Data (KB)| Total transferred data after completing the migration| Yes|


## How to run the project

>### How to run the simulation

To run the simulation in the default mode open a terminal in the path `./EdgeMig/`and enter the following command: 

    python Main.py -d

This will run the simulation with the default parameters and the result will be saved in the path `./EdgeMig/Digest/LoopVM/default`. This is a simulation that can be used as an example, however if the objective is to run a more custom simulation for testing different heuristics then the following command can be executed:

	python Main.py
	--VMmode <VMmode> 
	--trips <FileName.csv> 
	--stations <FileName.csv> 
	--lte <FileName.csv> 
	--vm <FileName.csv> 
	--dgst_folder <FolderName> 
	--vmid <VMid> 
	--cone <ConeAperture> 
	--tripmin <TripMin> 
	--tripmax <TripMax> 
	--migtype <MigType> 
	--benchmark <Benchmark> 
	--ptr <PageTransferingRate>
	--rm_cluster <RemoveCluster> 
	--dynamic_plot <DynamicPlot> 
	--mig_cost <MigrationCost> 
	--timeout <Timeout> 
	--timeout_mult <TimeoutMultipler> 
	--lat_dist <LatencyDistance> 

Note that it is advise to run the command inline, as follows:

    python Main.py --VMmode <VMmode> --trips <FileName.csv> --stations <FileName.csv> --lte <FileName.csv> --vm <FileName.csv> --dgst_folder <FolderName> --vmid <VMid> --cone <ConeAperture> --tripmin <TripMin> --tripmax <TripMax> --migtype <MigType> --benchmark <Benchmark> --ptr <PageTransferingRate> --rm_cluster <RemoveCluster> --dynamic_plot <DynamicPlot> --mig_cost <MigrationCost> --timeout <Timeout> --timeout_mult <TimeoutMultipler> --lat_dist <LatencyDistance>

For better readability the command was presented in a more comprehensive way by listing all the possible settings that can be adjusted to produce different results of the simulation. By changing some flags different migration policies can be tested and then compared once the data from the result is plotted by the program on the path `./EdgeMig/Digest/Plot/plot_digest.py`.  Important to note that when executing with the full command in the simulation program there are some flags that are obligatory, which are the following:

    --vm_mode <VMmode> 
    --trips <FileName.csv>
    --stations <FileName.csv> 
    --lte <FileName.csv> 
    --vm <FileName.csv> 
    --dsgt_folder <FolderName>

In the table below it's presented a more comprehensive view of each functionality that the flags provide with a more detailed description. 
|Flags  | Description |
|--|--|
| -\-vm_mode | **0** -> Runs Sim with only one VM with the ID given in the flag -\-vmid <br/> **1** -> Runs Sim with all the VM's from the dataset that follow the restrictions of the flags: -\-migtype -\-benchmark -\-ptr |
| -\-trips | Name of the file with the mobility dataset (ex: **DACT_E-Dataset.csv**)|
| -\-stations | Name of the file with the edge server dataset (ex: **Network_Edge.csv**)|
| -\-lte | Name of the file with the stations dataset (ex: **Network_LTE.csv**) |
| -\-vm |  Name of the file with the stations dataset (ex: **Vm_dataset_raw.csv**)|
| -\-dsgt_folder | Name of the folder with the results, depending on the -\-vm_mode, that will be created in the path:<br/>`./EdgeMig/Digest/<SingleVM or LoopVM>/`<**`default`**>|
| -\-vmid |  The ID of the virtual machine that the user wishes to run if flag the -\-vm_mode set to 0 (ex: **1463740276**)|
| -\-cone | The aperture of the searchcone that ranges from 0-359 (ex: **180**) |
| -\-tripmin | Define the starting trip (ex: **1**) i.e starts in the first trip of the dataset |
| -\-tripmax | Define the ending trip (ex: **10**) i.e ends when it reaches the 10th trip|
| -\-migtype | Defines the type of migration from the VM dataset (ex: **original**) i.e original means the migration is Pre-Copy |
| -\-benchmark | Defines the type of benchmark the vm was running at the time of migration from the VM dataset (ex: **mplayer**) |
| -\-ptr |  Defines the page transfering rate (MB/s) that it can be pulled from the VM dataset (ex: **150**) |
| -\-rm_cluster | **0** -> Does not remove clusters of edge servers that are too close together <br/> **1** -> Removes clusters of edge servers that are too close together|
| -\-dynamic_plot | **0** -> Does not launch the dynamic plot <br/> **1** -> Launches the dynamic plot  |
| -\-mig_cost | **0** -> The migration has no time cost <br/> **1** -> The migration has time cost |
| -\-timeout |  **0** -> There is no timeout after each migration occurs <br/> **1** -> There is a timeout after each migration occurs |
| -\-timeout_mult| If the flag -\-timeout is set to **1** then it is possible to change the multiplier of the timeout (ex: **7**) <br/> i.e if the cost of migration is 1 minute, then the timeout will be 7 min  |
| -\-lat_dist | **1** -> The migration decision is based on the latency to the source taking into account the backhaul overhead <br/> **2**-> The migration decision is based solely on the distance to the source |


>### How to run the plotting program

Once all the desired simulations are finished, the result can be plotted by opening a terminal in the directory `./EdgeMig/Digest/Plot/`  and run the following command:

    python plot_digest.py
    
 After this command is entered the terminal will display the following:

    Enter 0 for single plot or enter 1 for loop plot:
    
Depending on how the user ran the simulations it can choose either 0 or 1. If the simulation was done with the flag **-\-vm_mode** set to **0**, then the user should enter in this step the option **0** and if the user ran the simulation with the flag **-\-vm_mode** set to **1**, then it should enter at this step the option **1**.

After this command is entered the following prompt will appear:

    Enter the identifiers of each test seperated by a space (ex: Cone_180 Cone_60):

Here the user should type the name of the identifiers it wants to see in the plotting legend. Note that no spaces between identifiers is allowed.

After entering the desired identifiers the following command will appear in the terminal:

    Enter the name of the folders of each test seperated by a space (ex:test1 test2):

In this last prompt the user needs to enter the name of the folders that choose previously when running the simulation with the flag 
**-\-dgst_folder** . Important to note that the number of folder needs to match with the number of identifiers previously entered. 

>### How the results presented were obtained? 

Inside the path `./EdgeMig/Digest/LoopVM/` there are multiple folders with different results that can be used as an example to experiment with the simulator and plotting program as a away to reproduce the same results and get acquitted with both programs.
The folder `A` contains an experiment of 3 trips where the cone has an aperture of  180º degrees and the policy for migration is based on the latency equilibrium, without any timeout or cluster removing mechanism. The folder `B`  contains the results of the same simulation but with a smaller cone aperture of 60º degrees. The folder `C` contains a simulation equal to the first one presented in the folder `A` but with the cluster removing mechanism active. Finally the last folder, `D` contains a simulation equal to the first one here described but with a timeout associated to the migration policy.

To run the first simulation where 3 trips had the cone with an aperture of 180º degrees and the policy for migration is based on the latency equilibrium presented in the folder `A`, without any timeout or cluster removing mechanism the execution command was:

    python Main.py --VMmode 1 --trips DACT_E-Dataset.csv --stations Network_Edge.csv --lte Network_LTE.csv --vm Vm_dataset_raw.csv --dsgt_folder A --cone 180 --tripmin 1 --tripmax 3 --migtype original --benchmark mplayer --ptr 150 --rm_cluster 0 --dynamic_plot 0 --mig_cost 1 --timeout 0 --lat_dist 1

To run the simulation in the folder `B` that is  a similar simulation to the previous one present but with a aperture cone of 60º the command executed was:

     python Main.py --VMmode 1 --trips DACT_E-Dataset.csv --stations Network_Edge.csv --lte Network_LTE.csv --vm Vm_dataset_raw.csv --dsgt_folder B --cone 60 --tripmin 1 --tripmax 3 --migtype original --benchmark mplayer --ptr 150 --rm_cluster 0 --dynamic_plot 0 --mig_cost 1 --timeout 0 --lat_dist 1

To run the the simulation in the folder `C`, which contains the simulation equal to the first one presented in the folder `A` but with the cluster removing mechanism active, the command executed was:

    python Main.py --VMmode 1 --trips DACT_E-Dataset.csv --stations Network_Edge.csv --lte Network_LTE.csv --vm Vm_dataset_raw.csv --dsgt_folder C --cone 180 --tripmin 1 --tripmax 3 --migtype original --benchmark mplayer --ptr 150 --rm_cluster 1 --dynamic_plot 0 --mig_cost 1 --timeout 0 --lat_dist 1

To run the simulation in the folder `D` that contains a simulation equal to the first one here described but with a timeout associated to the migration policy, the command executed was:

    python Main.py --VMmode 1 --trips DACT_E-Dataset.csv --stations Network_Edge.csv --lte Network_LTE.csv --vm Vm_dataset_raw.csv --dsgt_folder D --cone 180 --tripmin 1 --tripmax 3 --migtype original --benchmark mplayer --ptr 150 --rm_cluster 0 --dynamic_plot 0 --mig_cost 1 --timeout 1 --timeout_mult 7 --lat_dist 1

With all the results acquired it is possible to plot them by using the plotting program with a terminal in the directory `./EdgeMig/Digest/Plot/` with the following commands:

	python plot_digest.py
    Enter 0 for single plot or enter 1 for loop plot:1
    Enter the identifiers of each test seperated by a space (ex: Cone_180 Cone_60):Cone_180 Cone_60 Rm_Cluster Timeout
    Enter the name of the folders of each test seperated by a space (ex:test1 test2):A B C D

## Project Documentation

For a more detailed documentation about the project refer to the link provided in order to get some knowledge about each function and file of the project and their inputs, outputs and descriptions to better understand the functionalities of the project.
[Documentation for the Simulator](https://goncalonuno.github.io/EdgeMig/)

## How to contribute to this project?

>### Node Determination Model
The node determination model of this project is presented in the `NodeDiscovery.py` file in the function `node_search`. The approach of choosing a possible destination for the virtual machine was developed. The main principle was to find a viable edge server that would be inside a given cone of vision depending on the heading of the user.  It is this function that suggests a viable destination and for that matter any developer can tweak or create a completely new mechanism or heuristic, in order to test if it is a viable solution to the problem. The current implementation would benefit of tracking the past heading history of the user to make a more predictable suggestion of the destination, or even develop some mechanism to mitigate potential candidates that might not be ideal since the user's heading has some level of uncertainty.  

>### Backhaul Latency Model
The backhaul latency model of this project is presented in the `LTE.py` which is composed of two functions, `latency_backhaul` and `get_latency`. The offered solution is a very simple interpretation of the backhaul model that it was proposed by an analysis done in a survey published by the IEEE [\[1\]](#citations) and the Small Cell Forum study [\[2\]](#citations) .  However developers can expand this model and improve it with more detail by approximating it to a more realistic model. This is one of the ares this project can be improved in order to get result closer to the reality. 
   
>### Policy Evaluator
In the file `policy.py` in the function `policy_evaluator` the analisis if the migration should happen is analyzed.  The policy evaluator is the next layer after the node determination process that tries to evaluate if such migration should actually be carried out. For now the proposed solution is very simple and basic, only letting the migration occur if there is an equilibrium of the latency between the source and the suggested target. However in this module can be developed to carry out a more detailed and rigorous tests with more heuristics to determine if in fact the migration should happen. As an example a model for estimating the migration time can be added and by doing it so try to anticipate the migration so that once such migration finishes the user is already connected to the better edge server in terms of latency. Other mechanism can be explored by adding a history of the migrations performed and attribute a classification to each migration. This classification can then be feed to the `policy_evaluator` function as a possibility to evaluate if such migration is worthwhile.  

>### Client
In the file `Client.py`the client class is presented and here new methods can be added to the client that might provide new functionalities. It is encourage to explorer the client class and add new features that could be beneficial to this class, improving the flexibility and extensibility of the client class.   

>### Server
In the file `Serve.py`the server class is presented and here new methods can be added to the server entity that might provide new functionalities. It is encourage to explorer the server class and add new features that could be beneficial to this class, improving the flexibility and extensibility of the server class.   

## Creator

**Gonçalo Tomás**
- https://github.com/goncalonuno
- https://www.linkedin.com/in/gonçalotomás

## Acknowledgments

ADD TEXT HERE

## Citations
- [1] Jaber, M., Imran, M. A., Tafazolli, R., & Tukmanov, A. (2016). 5G Backhaul Challenges and Emerging Research Directions: A Survey. IEEE Access, 4, 1743–1766. https://doi.org/10.1109/ACCESS.2016.2556011

- [2] ‘‘Backhaul technologies for small cells: Use cases, requirements and solution,’’ Small Cell Forum, Dursley, U.K., Tech. Rep. 049.01.01, Feb. 2013

- [3]Moosavi, Sobhan, Behrooz Omidvar-Tehrani, and Rajiv Ramnath. “Trajectory Annotation by Discovering Driving Patterns.” Proceedings of the 3rd ACM SIGSPATIAL Workshop on Smart Cities and Urban Analytics. ACM, 2017.

- [4] http://www.opencellid.org/

- [5] Jo, C., Cho, Y., & Egger, B. (2017). A machine learning approach to live migration modeling. SoCC 2017 - Proceedings of the 2017 Symposium on Cloud Computing, 351–364. https://doi.org/10.1145/3127479.3129262


## Copyright and license

UPDATE HERE
Code and documentation copyright 2011-2018 the authors. Code released under the [MIT License](https://reponame/blob/master/LICENSE).
