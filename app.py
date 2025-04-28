import subprocess, sys, io, os, json, random, asyncio, time, uuid

bicep_code = { 
    "param_name" : "param uid string",
    "appserviceplan" : "module appserviceplan 'modules/appserviceplan.bicep' = {params: {name: uid }}",
    "appserviceblessedimage" : "module appservice 'modules/appserviceblessedimage.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname}}",
    "appservicewebforcontainerpublic" : "module appservice 'modules/appservicewebappforcontainerpublic.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname}}",
    "appservicewebforcontainerprivate" : "module appservice 'modules/appservicewebappforcontainerprivate.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname, azureContainerRegistryName: acr.outputs.acrname, azureContainerRegistryPassword: acr.outputs.password }}",
    "acr" :"module acr 'modules/acr.bicep' = {params: {name: uid }}",
    "vnet":"module vnet 'modules/vnet.bicep' = {params: {name: uid, appservicename: appserviceplan.outputs.appserviceplanname}}",
    "blobstorage" :"module blobstorage 'modules/blobstorage.bicep' = {params: {name: uid, appservicename: appserviceplan.outputs.appserviceplanname}}",
    "filestorage" :"module filestorage 'modules/filestorage.bicep' = {params: {name: uid, appservicename: appserviceplan.outputs.appserviceplanname}}",
    "appgateway" :"module appgateway 'modules/appgateway.bicep' = {params: {name: uid }}",
}

services_pretty = {
 "appserviceblessedimage" : "Blessed Image: ",
 "appservicewebforcontainerpublic" : "Web App for Container Public Image: ",
 "appservicewebforcontainerprivate" : "Web App for Container Azure Container Registry Private Image: ",
 "vnet" : "Vnet Intergration        ",
 "privateendpoint" : "Private Endpoint         ",
 "blobstorage" : "Storage Mount Blob       ",
 "filestorage": "Storage Mount File Share ",
 "appgateway": "App GateWay              ",
 "privateendpoint" : "Private Endpoint         ",
 "keyvault" :  "KeyVault                 "
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

def generate_random_name():
    with open('foodnames.json', 'r') as file:
        names_data = json.load(file)
        foodnames = names_data['foods']
    food = foodnames[random.randint(0, len(foodnames)-1)]
    return food + str(random.randint(0,999))

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
    f = open ('main.bicep', 'a')
    for module_name in modules_list: 
        f.write(bicep_code[module_name])
        f.write('\n')
    f.close()

def get_az_account_data():
    subprocess_use_shell = True if len(sys.argv) > 1  and sys.argv[1] == 'DEBUG' else False
    data = subprocess.run(["az", "account", "show"], capture_output=True, shell=subprocess_use_shell)
    account_data = json.loads(data.stdout)
    subscription_id = account_data['id']
    subscription_name = account_data['name']
    user_name = account_data['user']['name'].split('@')[0]

    return [user_name, subscription_name, subscription_id]

def run_input_loop():
    service_selection = set()

    appservice_type = ''
    while appservice_type == '':
        try: 
            print("Choose App Service Type:\n")
            print(services_pretty['appserviceblessedimage'] + bcolors.WARNING + "[1]" + bcolors.ENDC)
            print(services_pretty['appservicewebforcontainerpublic'] + bcolors.WARNING + "[2]" + bcolors.ENDC)
            print(services_pretty['appservicewebforcontainerprivate'] + bcolors.WARNING + "[3]" + bcolors.ENDC)
            appservice_type = int(input("Enter 1,2, or 3: "))
            if int(appservice_type) not in ([1,2,3]):
                appservice_type = ''
                print('\n' + bcolors.FAIL + 'Incorrect value, enter: 1, 2, or 3' + bcolors.ENDC)
        except ValueError:
            print('\n' + bcolors.FAIL + 'Incorrect value, enter: 1, 2, or 3' + bcolors.ENDC)

    match appservice_type:
        case 1:
            service_selection.add('appserviceblessedimage')
        case 2:
            service_selection.add('appservicewebforcontainerpublic')
        case 3:
            service_selection.add('appservicewebforcontainerprivate')
            service_selection.add('acr')
    

    done = False
    while done == False:
        print("\nEnter space seperated numbers of the options, if done type: " + bcolors.OKGREEN + "[Y]" + bcolors.ENDC)
        print("Select additional services to add: \n")

        print ('Service                     | Added')
        
        selection_list = ['vnet', 'privateendpoint', 'blobstorage', 'filestorage', 'appgateway', 'keyvault']

        for i, s in enumerate(selection_list):
            if s not in service_selection:
                print ("{0:18}| {1}".format(services_pretty[s] + bcolors.WARNING + "[" + str(i + 1) + "]" + bcolors.ENDC, "False"))
            else:
                print ("{0:18}| {1}".format(services_pretty[s] + bcolors.WARNING + "[" + str(i + 1) + "]" + bcolors.ENDC, (bcolors.OKGREEN + "True" + bcolors.ENDC + " - Re-enter number to remove")))

        y = input()
        input_string = y.split(" ")
        for i in input_string:
            if i in ['1', '2', '3', '4', '5', '6']:
                service  = selection_list[int(i) - 1]
                if service not in service_selection:
                    service_selection.add(service)
                else:
                    service_selection.remove(service)
            elif i == "Y":
                done = True

    return service_selection

def deploy_bicep(deployment_name, name):
    print(name)
    # az group create --name $name --location eastus
    #subprocess.run(["az", "group", "create", "--name", deployment_name, "--location", "eastus"], shell=True)
    stream_output(["az", "group", "create", "--verbose", "--name", deployment_name, "--location", "eastus"])
    
    #az deployment group create --verbose --resource-group $name --template-file main.bicep --parameters name="uid"
    stream_output(["az", "deployment", "group", "create", "--verbose", "--resource-group", deployment_name, "--template-file", "main.bicep", "--parameters", ("uid=" + name ) ])
    #subprocess.run(["az", "deployment", "group", "create", "--verbose", "--resource-group", deployment_name, "--template-file", "main.bicep"], capture_output=True, shell=True)


def print_subscription_information(user_name, subscription_name, subscription_id):
    print("\nThis is the account information you are running with. If this is not correct please use `az account set` to correct this before continuing.")
    print("--------------------------------------------------------------------------------")
    print("User: {0}".format(user_name))
    print("Subscription Name: {0}".format(subscription_name))
    print("Subscription Id: {0}".format(subscription_id))
    print("--------------------------------------------------------------------------------\n")

def print_deployment_complete(subscription_id, deploy_name):
    print ("Your depeployment seems complete here is the resource group link")
    print(bcolors.OKBLUE + "https://ms.portal.azure.com/#@fdpo.onmicrosoft.com/resource/subscriptions/{0}/resourceGroups/{1}/overview".format(subscription_id, deploy_name) + bcolors.ENDC)

def run_any_outstanding_az_cli_commands():
    if "acr" in services:
        #az acr import --name kedsouzabicepacr --source mcr.microsoft.com/dotnet/framework/samples:aspnetapp
        stream_output(["az", "acr", "import", "--name", name , "--source", "docker.io/library/httpd:latest"])


def main():
    
    user_name, subscription_name, subscription_id = get_az_account_data()
    print_subscription_information(user_name, subscription_name, subscription_id)
    name = generate_random_name()
    services = run_input_loop()

    # Add default options to the bicep file.
    write_bicep(["param_name"])
    write_bicep(["appserviceplan"])
    for service in services:
        write_bicep([service])

    deploy_name = user_name + '-' + name
    deploy_bicep(deploy_name, name)

    run_any_outstanding_az_cli_commands()

    print_deployment_complete(subscription_id, deploy_name)


if __name__ == "__main__":
    main()



