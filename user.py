import sys, getopt
import os.path
import os


class UserDef:

    """The class UserDef is used to secure all the information entered by the 
    user when passing the arguments to run the program. This information will
    impact the way the simulation will run and directly affect the results.

    :param user_def_dict: Dictionary with all the user defined paramenters that were entered
    :type user_def_dict: Dictionary
    :param dftrips_path: Path for the trips dataset
    :type dftrips_path: String
    :param dfstations_path: Path for the dataset with the edge server stations
    :type dfstations_path: String
    :param df_LTE_path: Path for the dataset with the LTE stations
    :type df_LTE_path: String
    :param dfvm_path: Path for the dataset with the VMs
    :type dfvm_path: String   
    :param cone: Cone aperture
    :type cone: Integer
    :param digest_path: Path for outputting the results 
    :type digest_path: String
    :param trip_min: The starting trip ID number
    :type trip_min: Integer
    :param trip_max: The ending trip ID number 
    :type trip_max: Integer
    :param vm_mode: Defines if the simulation will run with all the user designated VMs or if it runs with a single VM depending on ID entered by the user 
    :type vm_mode: Integer
    :param vm_id: The ID of the VM if the simulation is ran in vm_mode=0 
    :type vm_id: Integer
    :param migtype: The type o migration that it was performed 
    :type migtype: String
    :param benchmark: The type of benchmark that was used while performing the migration 
    :type benchmark: String
    :param PTR: Page transfering rate while the migration happend 
    :type PTR: Integer
    :param rem_cluster: Defines if the simulation will remove edge servers that too close together
    :type rem_cluster: Integer
    :param dynamic_plot: Defines if the simulation will display the dynamic plot
    :type dynamic_plot: Integer
    :param mig_cost: Defines if the simulation will account the cost of migration
    :type mig_cost: Integer
    :param timeout: Defines if the simulation will add a timeout after each migration is performed as a cooldown
    :type timeout: Integer
    :param timeout_multiplier: Defines the timout multipler to be used if the user decides to use a timeout upon each migration 
    :type timeout_multiplier: Integer
    :param lat_dist: Defines if the simulation will use as a migration policy the distance or latency between the source and target 
    :type lat_dist: Integer
    
    """

    def __init__(self, user_def_dict):
        
        self.dftrips_path = user_def_dict['dftrips']
        self.dfstations_path = user_def_dict['dfstations']
        self.df_LTE_path = user_def_dict['df_LTE']
        self.dfvm_path = user_def_dict['dfvm']
        self.cone = user_def_dict['cone']
        self.digest_path = user_def_dict['digest_path']
        self.trip_min = user_def_dict['trip_min']
        self.trip_max = user_def_dict['trip_max']
        self.vm_mode = user_def_dict['VM_mode']
        self.vm_id = user_def_dict['vm_id']
        self.migtype = user_def_dict['migtype']
        self.benchmark = user_def_dict['benchmark']
        self.PTR = user_def_dict['PTR']
        self.rem_cluster = user_def_dict['rem_cluster']
        self.dynamic_plot = user_def_dict['dynamic_plot']
        self.mig_cost = user_def_dict['mig_cost']
        self.timeout = user_def_dict['timeout']
        self.timeout_multiplier = user_def_dict['timeout_multiplier']
        self.lat_dist = user_def_dict['lat_dist']


        

def handle_user_def (usr_def):

    """The function handle_user_def is responsible to parse and check if the
    arguments entered by the user are valid. It returns a dictionary with all
    the arguments organized in order to then fill the object user_def with all
    the required definitions.

    :param usr_def: List with all the arguments the user entered in the argv
    :type usr_def: List

    :return: user_def_dict, a dictionary with all the arguments the user entered
    :rtype: Dictionary
    """

    user_def_dict = {'dftrips': 'DACT_E-Dataset.csv',                                                                                         
                    'dfstations': 'Network_Edge.csv',                                                                                         
                    'df_LTE': 'Network_LTE.csv',                                                                                              
                    'dfvm': 'Vm_dataset_raw.csv',                                                                                             
                    'cone': 180,                                          # between 0 and 359                                                 
                    'digest_path': './Digest/' + 'LoopVM/' + 'default',    # Handle second and third string                                    
                    'trip_min': 1,                                        # if (trip_min <=0): trip_min = 1                                   
                    'trip_max': 3,                                        # if (trip_max < trip_min): trip_max = trip_min                     
                    'VM_mode': 0,                                         # 1-> Loop VM , 0 -> Single VM                                      
                    'vm_id' : 1463740276,                                 # VM id for Single VM mode                                          
                    'migtype': 'original',                                                                                                    
                    'benchmark': 'mplayer',                                                                                                   
                    'PTR': 150,                                                                                                               
                    'rem_cluster': 0,                                     # 1-> Remove Clusters , 0 -> Don't remove clusters                  
                    'dynamic_plot': 1,                                    # 1-> Dynamic plot , 0 -> No dynamic plot                           
                    'mig_cost': 1,                                        # 1-> Migration with cost , 0 -> Migration with no cost             
                    'timeout': 0,                                         # 1-> With timeout , 0 -> No timeout                                
                    'timeout_multiplier': 7,                              # >= 0                                                              
                    'lat_dist': 1                                         # 1-> Migration based on lat , 2 -> Migration based on dist         
                    }

    try:
        opts, args = getopt.getopt(usr_def,'dh',['VMmode=','trips=','stations=','lte=','vm=','dgst_folder=', 
                                                'vmid=', 'cone=', 'tripmin=', 'tripmax=', 'migtype=', 'benchmark=', 
                                                'ptr=', 'rm_cluster=', 'dynamic_plot=', 'mig_cost=', 'timeout=', 
                                                'timeout_mult=', 'lat_dist='])  
    except getopt.GetoptError:
        print('\nInput Error:\n\tTo run in default mode enter: main.py -d\n\tFor help enter: main.py -h\n')
        print('\tTo run with custom parameters enter:')
        print ('\tMain.py --VMmode <VMmode> --trips <FileName.csv> --stations <FileName.csv> --lte <FileName.csv>\n\t' , \
               '--vm <FileName.csv> --dgst_folder <FolderName> --vmid <VMid> --cone <ConeAperture> --tripmin <TripMin>\n\t', \
               '--tripmax <TripMax> --migtype <MigType> --benchmark <Benchmark> --ptr <PageTransferingRate> --rm_cluster <RemoveCluster>\n\t' , \
               '--dynamic_plot <DynamicPlot> --mig_cost <MigrationCost> --timeout <Timeout> --timeout_mult <TimeoutMultipler> --lat_dist <LatencyDistance>\n\t')
        sys.exit(2)

    if(len(args) != 0):
        print('Invalid Parameters:\n\tTo run default mode enter: main.py -d\n\tTo get help enter: main.py -h')
        sys.exit(2)

    i=0
    help_default = 0
    for opt, arg in opts:

        if opt in ('-h'):
            help_default = 1
            break
        
        if opt in ('-d'):
            help_default = 1
            break

        if opt in ('--trips'):
            i = i + 1 

        elif opt in ('--stations'):
            i = i + 1 
        
        elif opt in ('--lte'):
            i = i + 1 
        
        elif opt in ('--vm'):
            i = i + 1

        elif opt in ('--dgst_folder'):
            i = i + 1
        
        elif opt in ('--VMmode'):
            i = i + 1 

    if(i!=6 and help_default == 0):
        print('Missing Parameters:\n\tObligatory fields: --trips --stations --lte --vm --dgst_folder --VMmode\n\tTo get help enter: main.py -h')
        sys.exit(1)

    for opt, arg in opts:

        if opt == '-h':
            print ('HELP')
            print ('\tmain.py --vm_mode <VMmode> --trips <FileName.csv> --stations <FileName.csv> --lte <FileName.csv>\n\t' , \
               '--vm <FileName.csv> --dsgt_folder <FolderName> --vmid <VMid> --cone <ConeAperture> --tripmin <TripMin>\n\t', \
               '--tripmax <TripMax> --migtype <MigType> --benchmark <Benchmark> --ptr <PageTransferingRate> --rm_cluster <RemoveCluster>\n\t' , \
               '--dynamic_plot <DynamicPlot> --mig_cost <MigrationCost> --timeout <Timeout> --timeout_mult <TimeoutMultipler> --lat_dist <LatencyDistance>\n\t')
            sys.exit()

        elif opt in ('-d'):
            if((not os.path.isfile('./Datasets/Mobility/DACT_E-Dataset.csv')) or 
               (not os.path.isfile('./Datasets/Network/Network_Edge.csv')) or 
               (not os.path.isfile('./Datasets/Network/Network_LTE.csv')) or 
               (not os.path.isfile('./Datasets/Vm/Vm_dataset_raw.csv'))):
                print('Missing Datasets!\n\t Make sure that the datasets are inside the directory: ./ Datasets / <Mobility/Network/Vm> / <DACT_E-Dataset.csv/Network_Edge.csv/Network_LTE.csv/Vm_dataset_raw.csv>')
                sys.exit(2)
            break

        elif opt in ('--trips'):

            if(not os.path.isfile('./Datasets/Mobility/' + str(arg))):
                print('Missing Mobility Dataset')
                sys.exit(2)

            user_def_dict['dftrips'] = arg

        elif opt in ('--stations'):

            if(not os.path.isfile('./Datasets/Network/' + str(arg))):
                print('Missing Network Stations Dataset')
                sys.exit(2)

            user_def_dict['dfstations'] = arg

        elif opt in ('--lte'):

            if(not os.path.isfile('./Datasets/Network/' + str(arg))):
                print('Missing Network LTE Dataset')
                sys.exit(2)

            user_def_dict['df_LTE'] = arg

        elif opt in ('--vm'):

            if(not os.path.isfile('./Datasets/Vm/' + str(arg))):
                print('Missing VM Dataset')
                sys.exit(2)

            user_def_dict['dfvm'] = arg
        
        elif opt in ('--dgst_folder'):

            dgst_folder = arg 
        
        elif opt in ('--VMmode'):

            if(int(arg)==0 or int(arg)==1):
                vm_mode = int(arg)
                user_def_dict['VM_mode'] = int(arg)
            else:   
                print('VMmode only takes values: 0 or 1')
                sys.exit(2)

        elif opt in ('--vmid'):

            if(int(arg)>=0):
               user_def_dict['vm_id'] = int(arg) 
            else:   
                print('VM ID only takes values: >=0')
                sys.exit(2)

        elif opt in ('--cone'):

            if(int(arg)>=0 and int(arg)<=359):
               user_def_dict['cone'] = int(arg) 
            else:   
                print('Cone only takes values between 0 and 359')
                sys.exit(2)

        elif opt in ('--tripmin'):
            
            if(int(arg)>0):
               user_def_dict['trip_min'] = int(arg)
            else:   
                print('Trip min only takes values: >0')
                sys.exit(2)

        elif opt in ('--tripmax'):
            
            if(int(arg)>0 and int(arg)<=50):
               user_def_dict['trip_max'] = int(arg)
            else:   
                print('Trip max only takes values between 1 and 50')
                sys.exit(2)
                
        elif opt in ('--migtype'):
        
            user_def_dict['migtype'] = arg

        elif opt in ('--benchmark'):
        
            user_def_dict['benchmark'] = arg
        
        elif opt in ('--ptr'):
        
            if(int(arg)>0 and int(arg)<=150):
                user_def_dict['PTR'] = int(arg)
            else:   
                print('PTR only takes values between 1 and 150')
                sys.exit(2)

        elif opt in ('--rm_cluster'):

            if(int(arg)==0 or int(arg)==1):
                user_def_dict['rem_cluster'] = int(arg)
            else:   
                print('Remove cluster only takes values: 0 or 1')
                sys.exit(2)

        elif opt in ('--dynamic_plot'):

            if(int(arg)==0 or int(arg)==1):
                user_def_dict['dynamic_plot'] = int(arg)
            else:   
                print('Dynamic Plot only takes values: 0 or 1')
                sys.exit(2)

        elif opt in ('--mig_cost'):

            if(int(arg)==0 or int(arg)==1):
                user_def_dict['mig_cost'] = int(arg)
            else:   
                print('Migration cost only takes values: 0 or 1')
                sys.exit(2)

        elif opt in ('--timeout'):

            if(int(arg)==0 or int(arg)==1):
                user_def_dict['timeout'] = int(arg)
            else:   
                print('Migration timeout only takes values: 0 or 1')
                sys.exit(2)

        elif opt in ('--timeout_mult'):

            if(int(arg)>=0):
                user_def_dict['timeout_multiplier'] = int(arg)
            else:   
                print('Timeout multiplier only takes values: >=0')
                sys.exit(2)

        elif opt in ('--lat_dist'):

            if(int(arg)==1 or int(arg)==2):
                user_def_dict['lat_dist'] = int(arg)
            else:   
                print('Policy latency/distance only takes values: 1 or 2')
                sys.exit(2)

    if (user_def_dict['trip_max'] < user_def_dict['trip_min']): 
        user_def_dict['trip_max'] = user_def_dict['trip_min'] 
        print('Warning user entered trip_max < trip_min -> trip_max = trip_min')

    if(help_default==0):

        if(vm_mode == 0):
            user_def_dict['digest_path'] = './Digest/' + 'SingleVM/' + str(dgst_folder)
            
        elif(vm_mode == 1):
            user_def_dict['digest_path'] = './Digest/' + 'LoopVM/' + str(dgst_folder)


    return user_def_dict 