import subprocess, os, json, random, asyncio, time

bicep_code = {
        "appserviceplan" : "module appserviceplan 'modules/appserviceplan.bicep' = {}",
        "appserviceblessedimage" : "module appservice 'modules/appserviceblessedimage.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname}}" 
    }
        
appservice_types = { 1 : "Blessed Image: ", 2 : "Web App for Container Public Image: ", 3: "Web App for Container Azure Container Registry Private Image: "}
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

account_name = 'placeholder'

def write_bicep(modules_list):
    f = open ('main.bicep', 'w')
    for module_name in modules_list: 
        f.write(bicep_code[module_name])
        f.write('\n')
    f.close()

def get_az_account_name():
    return "kedsouza"
    #Bug hanging output
    deploy_name = subprocess.run(["az", "account", "show"], capture_output=True)
    name = json.loads(deploy_name.stdout)['user']['name']
    user_name = name.split('@')[0]
    return user_name
    

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
            print("Not implemented Yet")
        case 2:
            print ("Not implemented Yet")
            exit()
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


deployment_times = {
    "blessed image" : "14:54:58 -14:56:10 - 1 minute 52 seconds"
}
def deploy_bicep(user_name):
    d_name = user_name + '-appserviceblessedimage-' + str(random.randint(0, 9))
    time.sleep(112))
    
    #az group create --name $name --location eastus
    #subprocess.run(["az", "group", "create", "--name", d_name, "--location", "eastus"])
    
    # Output {""""id": "/subscriptions/bf7728b1-4728-478d-96bc-db17b8ebc9ff/resourceGroups/kedsouza-appserviceblessedimage-9",
    #"location": "eastus",
    #"managedBy": null,
    #"name": "kedsouza-appserviceblessedimage-9",
    #"properties": {
    #  "provisioningState": "Succeeded"
    #},
    #"tags": null,
    #"type": "Microsoft.Resources/resourceGroups"
    #}
  
    # Link to create: https://ms.portal.azure.com/#@fdpo.onmicrosoft.com/resource/subscriptions/bf7728b1-4728-478d-96bc-db17b8ebc9ff/resourceGroups/kedsouza-appserviceblessedimage-9/overview

    #az deployment group create --resource-group $name --template-file main.bicep
    #output = subprocess.run(["az", "deployment", "group", "create", "--resource-group", d_name, "--template-file", "main.bicep"], capture_output=True)
    # Sample OutPut
    return """[CompletedProcess(args=['az', 'deployment', 'group', 'create', '--resource-group', 'kedsouza-appserviceblessedimage-9', '--template-file', 'main.bicep'], returncode=0, stdout=b'{\n  "id": "/subscriptions/bf7728b1-4728-478d-96bc-db17b8ebc9ff/resourceGroups/kedsouza-appserviceblessedimage-9/providers/Microsoft.Resources/deployments/main",\n  "location": null,\n  "name": "main",\n  "properties": {\n    "correlationId": "92f8249f-5165-4df5-a885-1568deba70ea",\n    "debugSetting": null,\n    "dependencies": [\n      {\n        "dependsOn": [\n          {\n            "id": "/subscriptions/bf7728b1-4728-478d-96bc-db17b8ebc9ff/resourceGroups/kedsouza-appserviceblessedimage-9/providers/Microsoft.Resources/deployments/appserviceplan-jthnm6xe6hucq",\n            "resourceGroup": "kedsouza-appserviceblessedimage-9",\n            "resourceName": "appserviceplan-jthnm6xe6hucq",\n            "resourceType": "Microsoft.Resources/deployments"\n          }\n        ],\n        "id": "/subscriptions/bf7728b1-4728-478d-96bc-db17b8ebc9ff/resourceGroups/kedsouza-appserviceblessedimage-9/providers/Microsoft.Resources/deployments/appservice-qbyz4gkcq5gg2",\n        "resourceGroup": "kedsouza-appserviceblessedimage-9",\n        "resourceName": "appservice-qbyz4gkcq5gg2",\n        "resourceType": "Microsoft.Resources/deployments"\n      }\n    ],\n    "duration": "PT43.828575S",\n    "error": null,\n    "mode": "Incremental",\n    "onErrorDeployment": null,\n    "outputResources": [\n      {\n        "id": "/subscriptions/bf7728b1-4728-478d-96bc-db17b8ebc9ff/resourceGroups/kedsouza-appserviceblessedimage-9/providers/Microsoft.Web/serverfarms/asp-qbvafpszw6svy",\n        "resourceGroup": "kedsouza-appserviceblessedimage-9"\n      },\n      {\n        "id": "/subscriptions/bf7728b1-4728-478d-96bc-db17b8ebc9ff/resourceGroups/kedsouza-appserviceblessedimage-9/providers/Microsoft.Web/sites/asp-qbvafpszw6svy",\n        "resourceGroup": "kedsouza-appserviceblessedimage-9"\n      }\n    ],\n    "outputs": null,\n    "parameters": null,\n    "parametersLink": null,\n    "providers": [\n      {\n        "id": null,\n        "namespace": "Microsoft.Resources",\n        "providerAuthorizationConsentState": null,\n        "registrationPolicy": null,\n        "registrationState": null,\n        "resourceTypes": [\n          {\n            "aliases": null,\n            "apiProfiles": null,\n            "apiVersions": null,\n            "capabilities": null,\n            "defaultApiVersion": null,\n            "locationMappings": null,\n            "locations": [\n              null\n            ],\n            "properties": null,\n            "resourceType": "deployments",\n            "zoneMappings": null\n          }\n        ]\n      }\n    ],\n    "provisioningState": "Succeeded",\n    "templateHash": "9091923867377092764",\n    "templateLink": null,\n    "timestamp": "2025-04-16T14:55:52.422158+00:00",\n    "validatedResources": null\n  },\n  "resourceGroup": "kedsouza-appserviceblessedimage-9",\n  "tags": null,\n  "type": "Microsoft.Resources/deployments"\n}\n', stderr=b'')]"""

def countdown_timer(wait_time):
    count  = 0
    for i in range (0, wait_time):
        print("Estimated deployment time:", wait_time - i)
        time.sleep(1)
    return "done"


async def main():
    
    a = await asyncio.gather(
        asyncio.to_thread(get_az_account_name),
        asyncio.to_thread(download_bicep_modules),
        asyncio.to_thread(run_input_loop),
    )

    print(a)

    print(f"started at {time.strftime('%X')}")
    b = await asyncio.gather(
        asyncio.to_thread(deploy_bicep, a[0]),
        asyncio.to_thread(countdown_timer,112),
    )

    print(f"finished at {time.strftime('%X')}")
    print(b)

    print ("Your depeployment seems complete: here is the resource group link")
    print(bcolors.OKBLUE + "https://ms.portal.azure.com/#@fdpo.onmicrosoft.com/resource/subscriptions/bf7728b1-4728-478d-96bc-db17b8ebc9ff/resourceGroups/kedsouza-appserviceblessedimage-9/overview" + bcolors.ENDC)



    

asyncio.run(main())

# Commented out for testing.

# Refactor start at beginning of the program and make async.

# deploy_name = subprocess.run(["az", "account", "show"], capture_output=True)
# name = json.loads(deploy_name.stdout)['user']['name']
# user_name = name.split('@')[0]
# d_name = user_name + '-appserviceblessedimage-' + str(random.randint(0, 9))

# #az group create --name $name --location eastus
# subprocess.run(["az", "group", "create", "--name", d_name, "--location", "eastus"])
# #az deployment group create --resource-group $name --template-file main.bicep
# subprocess.run(["az", "deployment", "group", "create", "--resource-group", d_name, "--template-file", "main.bicep"])


