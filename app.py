import subprocess, sys, io, os, json, random, asyncio, time, uuid

bicep_code = { 
<<<<<<< HEAD
    "param_name" : "param uid string",
    "appserviceplan" : "module appserviceplan 'modules/appserviceplan.bicep' = {params: {name: uid }}",
    "appserviceblessedimage" : "module appservice 'modules/appserviceblessedimage.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname}}",
    "appservicewebforcontainerpublic" : "module appservice 'modules/appservicewebappforcontainerpublic.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname}}",
    "appservicewebforcontainerprivate" : "module appservice 'modules/appservicewebappforcontainerprivate.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname, azureContainerRegistryName: acr.outputs.acrname, azureContainerRegistryPassword: acr.outputs.password }}",
    "acr" :"module acr 'modules/acr.bicep' = {params: {name: uid }}",
    "vnet":"module vnet 'modules/vnet.bicep' = {params: {name: uid, appservicename: appserviceplan.outputs.appserviceplanname}}",
    "privateendpoint" : "module privateendpoint 'modules/privateendpoint.bicep' = {params: {name: uid, appservicename: appserviceplan.outputs.appserviceplanname, vnetname: vnet.outputs.vnetname }}"
=======
    "param_id" : "param id string",
    "param_user" : "param user string",
    "appserviceplan" : "module appserviceplan 'modules/appserviceplan.bicep' = {params: {id : id, user: user}}",
    "appserviceblessedimage" : "module appservice 'modules/appserviceblessedimage.bicep' = {params: {id:id, user:user, appServicePlanName: appserviceplan.outputs.appserviceplanname}}",
    "appservicewacpublic" : "module appservice 'modules/appservicewebappforcontainerpublic.bicep' = {params: {id:id, user:user, appServicePlanName: appserviceplan.outputs.appserviceplanname}}",
    "appservicewacprivate" : "module appservice 'modules/appservicewebappforcontainerprivate.bicep' = {params: {id:id, user:user, appServicePlanName: appserviceplan.outputs.appserviceplanname, azureContainerRegistryName: acr.outputs.acrname, azureContainerRegistryPassword: acr.outputs.password }}",
    "acr" :"module acr 'modules/acr.bicep' = {params: {id: id, user: user }}",
    "vnet":"module vnet 'modules/vnet.bicep' = {params: {id: id, user: user, appservicename: appservice.outputs.appservicename}}",
    "blobstorage" :"module blobstorage 'modules/blobstorage.bicep' = {params: {id : id, user: user, appservicename: appservice.outputs.appservicename}}",
    "filestorage" :"module filestorage 'modules/filestorage.bicep' = {params: {id : id, user: user, appservicename: appservice.outputs.appservicename}}",
    "appgateway" :"module appgateway 'modules/appgateway.bicep' = {params: {name: uid }}",
    "keyvault" : "module keyvault 'modules/keyvault.bicep' = {params: {id : id, user: user, appservicename: appservice.outputs.appservicename}}"
>>>>>>> main
}

services_pretty = {
 "appserviceblessedimage" : "Blessed Image: ",
 "appservicewacpublic" : "Web App for Container: ",
 "acr" : "Azure Container Registry ",
 "vnet" : "Vnet Intergration        ",
 "privateendpoint" : "Private Endpoint         ",
 "blobstorage" : "Storage Mount Blob       ",
 "filestorage": "Storage Mount File Share ",
 "appgateway": "App GateWay              ",
 "keyvault" :  "KeyVault                 "
}

service_name_short = {
 "acr"  : "acr",
 "vnet" : "vnet",
 "privateendpoint" : "pe",
 "blobstorage" : "blobmnt",
 "filestorage": "filemnt",
 "appgateway": "appgw",
 "keyvault" :  "kv"
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

def generate_rg_name(user_name, services, id):
    print(services)
    if len(services) < 2:
        return user_name + '-repo-' + id 
    name = user_name + "-"
    for service in services:
        if (service not in ['appserviceblessedimage', 'appservicewacpublic']):
            name += service_name_short[service]
            name += '-'
    return name + id
    
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
            print(services_pretty['appservicewacpublic'] + bcolors.WARNING + "[2]" + bcolors.ENDC)
            appservice_type = int(input("Enter 1 or 2: "))
            if int(appservice_type) not in ([1,2]):
                appservice_type = ''
                print('\n' + bcolors.FAIL + 'Incorrect value, enter: 1, 2, or 3' + bcolors.ENDC)
        except ValueError:
            print('\n' + bcolors.FAIL + 'Incorrect value, enter: 1, 2, or 3' + bcolors.ENDC)

    match appservice_type:
        case 1:
            service_selection.add('appserviceblessedimage')
        case 2:
            service_selection.add('appservicewacpublic')
           

    done = False
    while done == False:

        print("\nEnter space seperated numbers of the options, if done type: " + bcolors.OKGREEN + "[Y]" + bcolors.ENDC)
        print("Select additional services to add: \n")
        print( bcolors.FAIL + "!" +  bcolors.ENDC +  'Private Endpoint, AppGateway, KeyVault are still in development.')


        print ('Service                     | Added')
        
        selection_list = ['acr', 'vnet', 'privateendpoint', 'blobstorage', 'filestorage', 'appgateway', 'keyvault']

        for i, s in enumerate(selection_list):
            if s not in service_selection:
                print ("{0:18}| {1}".format(services_pretty[s] + bcolors.WARNING + "[" + str(i + 1) + "]" + bcolors.ENDC, "False"))
            else:
                print ("{0:18}| {1}".format(services_pretty[s] + bcolors.WARNING + "[" + str(i + 1) + "]" + bcolors.ENDC, (bcolors.OKGREEN + "True" + bcolors.ENDC + " - Re-enter number to remove")))

        y = input()
        input_string = y.split(" ")
        for i in input_string:
            if i in ['1', '2', '3', '4', '5', '6', '7']:
                service  = selection_list[int(i) - 1]
                if service not in service_selection:
                    service_selection.add(service)
                else:
                    service_selection.remove(service)
            elif i == "Y":
                done = True

    return service_selection

def deploy_bicep(deployment_name, user, id):
    # az group create --name $name --location eastus
    stream_output(["az", "group", "create", "--verbose", "--name", deployment_name, "--location", "eastus"])
    
    #az deployment group create --verbose --resource-group $name --template-file main.bicep --parameters id="32" user="kedsouza"
    stream_output(["az", "deployment", "group", "create", "--verbose", "--resource-group", deployment_name, "--template-file", "main.bicep", "--parameters", ("id=" + id), ("user=" + user) ])
    #subprocess.run(["az", "deployment", "group", "create", "--verbose", "--resource-group", deployment_name, "--template-file", "main.bicep"], capture_output=True, shell=True)


def print_subscription_information(user_name, subscription_name, subscription_id):
    print("\nThis is the account information you are running with. If this is not correct please use `az account set` to correct this before continuing.")
    print("--------------------------------------------------------------------------------")
    print("User: " + bcolors.OKCYAN +  " {0}".format(user_name) + bcolors.ENDC)
    print("Subscription Name: " + bcolors.OKCYAN + "{0}".format(subscription_name) + bcolors.ENDC) 
    print("Subscription Id: " + bcolors.OKCYAN + "{0}".format(subscription_id) + bcolors.ENDC)
    print("--------------------------------------------------------------------------------\n")

def print_deployment_complete(subscription_id, deploy_name):
    print ("Your deployment is running view progress by clicking on this link")
    print(bcolors.OKBLUE + "https://ms.portal.azure.com/#@fdpo.onmicrosoft.com/resource/subscriptions/{0}/resourceGroups/{1}/deployments".format(subscription_id, deploy_name) + bcolors.ENDC)

def run_any_outstanding_az_cli_commands(services, user, id):
    if "acr" in services:
        #az acr import --name kedsouzaacr03 --source mcr.microsoft.com/appsvc/php:latest_20221101.1 -t nginx:latest
        stream_output(["az", "acr", "import", "--name", (user + 'acr' + id), "--source", "mcr.microsoft.com/appsvc/php:latest_20221101.1", "-t", "appsvcphp:latest"])

def initalize_main_bicep():
    try:
        with open('main.bicep', 'x') as file:
            # Add default options to the bicep file.
            write_bicep(["param_id"])
            write_bicep(["param_user"])
            write_bicep(["appserviceplan"])
    except FileExistsError:
        with open('main.bicep', 'w') as file:
            # Add default options to the bicep file.
            write_bicep(["param_id"])
            write_bicep(["param_user"])
            write_bicep(["appserviceplan"])     


def main():
    
<<<<<<< HEAD
    account_data = get_az_account_data()
    subscription, user_name = account_data['id'], account_data['user']['name'].split('@')[0]
    print("User: {0}".format(user_name))
    print("Subscription: {0}".format(subscription))

    #download_bicep_modules()
    a = run_input_loop()
    print(a)
   

    # Need to rewrite ! 
    if a[1][1][1] == True:
        print ("Adding VNET")
        write_bicep(['vnet'])

    if a[1][2][1] == True:
        print("Adding private endpoint")
        write_bicep(['vnet', 'privateendpoint' ])
       


    deploy_name = user_name + '-appserviceblessedimage-' + str(random.randint(0, 99))
    print("Your deployment will approximately take 78 seconds")
    deploy_bicep(deploy_name, name)

    if int(a[0]) == 3:
        #az acr import --name kedsouzabicepacr --source mcr.microsoft.com/dotnet/framework/samples:aspnetapp
        stream_output(["az", "acr", "import", "--name", name , "--source", "docker.io/library/httpd:latest"])

=======
    user_name, subscription_name, subscription_id = get_az_account_data()
    print_subscription_information(user_name, subscription_name, subscription_id)
>>>>>>> main
    
    services = run_input_loop()

    id = str(random.randint(0, 9)) + str(random.randint(0, 9))
    resource_group_name = generate_rg_name(user_name, services, id)

    initalize_main_bicep()
    if "acr" in services:
        services.remove('appservicewacpublic')
        services.add('appservicewacprivate')
        print (services)
    for service in services:
        write_bicep([service])
    
    print_deployment_complete(subscription_id, resource_group_name)

    deploy_bicep(resource_group_name, user_name, id)
    run_any_outstanding_az_cli_commands(services, user_name, id)
    
    print("Done ! ")

if __name__ == "__main__":
    main()



