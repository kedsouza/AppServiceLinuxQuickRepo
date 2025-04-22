import subprocess, sys, io, os, json, random, asyncio, time

bicep_code = {
    "appserviceplan" : "module appserviceplan 'modules/appserviceplan.bicep' = {}",
    "appserviceblessedimage" : "module appservice 'modules/appserviceblessedimage.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname}}",
    "appservicewebforcontinaerpublic" : "module appservice 'modules/appservicewebappforcontainerpublic.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname}}" 
}

appservice_types = { 
    1 : "Blessed Image: ",
    2 : "Web App for Container Public Image: ",
    3: "Web App for Container Azure Container Registry Private Image: "
}

hash_additional_services = {
    1 : ["Vnet Intergration        ", False],
    2 : ["Private Endpoint         ", False],
    3 : ["Storage Mount Blob       ", False],
    4:  ["Storage Mount File Share ", False],
    5 : ["App GateWay              ", False],
    6 : ["KeyVault                 ", False]
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def stream_output(command):
    subprocess_use_shell = True if len(sys.argv) > 1  and sys.argv[1] == 'DEBUG' else False
    filename = "stream.log"
    with io.open(filename, "w") as writer, io.open(filename, "r") as reader:
        process = subprocess.Popen(command, shell=subprocess_use_shell, stdout=writer)
        while process.poll() is None:
            sys.stdout.write(reader.read())
        # Read the remaining
        sys.stdout.write(reader.read())

def write_bicep(modules_list):
    f = open ('main.bicep', 'w')
    for module_name in modules_list: 
        f.write(bicep_code[module_name])
        f.write('\n')
    f.close()

def get_az_account_data():
    subprocess_use_shell = True if len(sys.argv) > 1  and sys.argv[1] == 'DEBUG' else False
    deploy_name = subprocess.run(["az", "account", "show"], capture_output=True, shell=subprocess_use_shell)
    return json.loads(deploy_name.stdout)


def download_bicep_modules():
    # Download and extract the necessary modules to run the script
    subprocess.run(["wget", "-q", "https://github.com/kedsouza/AppServiceLinuxQuickRepo/raw/refs/heads/main/modules.zip"])
    subprocess.run(["unzip", "-qo", "modules.zip"])
    subprocess.run(["rm","modules.zip"])

def run_input_loop():
    appservice_type = ''
    while appservice_type == '':
        try: 
            print("Choose App Service Type:\n")
            print(appservice_types[1] + bcolors.WARNING + "[1]" + bcolors.ENDC)
            print(appservice_types[2] + bcolors.WARNING + "[2]" + bcolors.ENDC)
            print(appservice_types[3] + bcolors.WARNING + "[3]" + bcolors.ENDC)
            appservice_type = int(input("Enter 1,2, or 3: "))
            if int(appservice_type) not in ([1,2,3]):
                appservice_type = ''
                print('\n' + bcolors.FAIL + 'Incorrect value, enter: 1, 2, or 3' + bcolors.ENDC)
        except ValueError:
            print('\n' + bcolors.FAIL + 'Incorrect value, enter: 1, 2, or 3' + bcolors.ENDC)

    match appservice_type:
        case 1:
            write_bicep(["appserviceplan", "appserviceblessedimage"])
        case 2:
            write_bicep(["appserviceplan", "appservicewebforcontinaerpublic"])
        case 3:
            print ("Not implemented Yet")
            exit()

    done = False
    while done == False:
        print("\nEnter space seperated numbers of the options, if done type: " + bcolors.OKGREEN + "[Y]" + bcolors.ENDC)
        print("Select additional services to add: \n")

        print ('Service                     | Added')
        
        for i in range (1,7):
            service = hash_additional_services.get(i)
            if service[1] == False:
                print ("{0:18}| {1}".format(service[0] + bcolors.WARNING + "[" + str(i) + "]" + bcolors.ENDC, str(service[1])))
            else:
                print ("{0:18}| {1}".format(service[0] + bcolors.WARNING + "[" + str(i) + "]" + bcolors.ENDC, (bcolors.OKGREEN + str(service[1]) + bcolors.ENDC + " - Re-enter number to remove")))
    
        y = input()
        input_string = y.split(" ")
        for i in input_string:
            if i in ['1', '2', '3', '4', '5', '6']:
                service = hash_additional_services.get(int(i))
                if service[1] == False:
                    hash_additional_services[int(i)] = [hash_additional_services[int(i)][0], True]
                else:
                    hash_additional_services[int(i)] = [hash_additional_services[int(i)][0], False]
            elif i == "Y":
                done = True

    return hash_additional_services

def deploy_bicep(deployment_name):
    # az group create --name $name --location eastus
    #subprocess.run(["az", "group", "create", "--name", deployment_name, "--location", "eastus"], shell=True)
    stream_output(["az", "group", "create", "--verbose", "--name", deployment_name, "--location", "eastus"])
    
    #az deployment group create --verbose --resource-group $name --template-file main.bicep
    stream_output(["az", "deployment", "group", "create", "--verbose", "--resource-group", deployment_name, "--template-file", "main.bicep"])
    #subprocess.run(["az", "deployment", "group", "create", "--verbose", "--resource-group", deployment_name, "--template-file", "main.bicep"], capture_output=True, shell=True)

def main():
    account_data = get_az_account_data()
    subscription, user_name = account_data['id'], account_data['user']['name'].split('@')[0]
    print("User: {0}".format(user_name))
    print("Subscription: {0}".format(subscription))

    #download_bicep_modules()
    run_input_loop()

    deploy_name = user_name + '-appserviceblessedimage-' + str(random.randint(0, 99))
    print("Your deployment will approximately take 78 seconds")
    deploy_bicep(deploy_name)

    print ("Your depeployment seems complete here is the resource group link")
    print(bcolors.OKBLUE + "https://ms.portal.azure.com/#@fdpo.onmicrosoft.com/resource/subscriptions/{0}/resourceGroups/{1}/overview".format(subscription, deploy_name) + bcolors.ENDC)


main()    



