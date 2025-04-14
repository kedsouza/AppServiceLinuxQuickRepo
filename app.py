import subprocess, os, json, random

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



# Download and extract the necessary modules to run the script
subprocess.run(["wget", "-q", "https://github.com/kedsouza/AppServiceLinuxQuickRepo/raw/refs/heads/main/modules.zip"])
subprocess.run(["unzip", "-q", "modules.zip"])
subprocess.run(["rm","modules.zip"])


bicep_code = {
    "appserviceplan" : "module appserviceplan 'modules/appserviceplan.bicep' = {}",
    "appserviceblessedimage" : "module appservice 'modules/appserviceblessedimage.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname}}" 
}
    
x = ''
while x == '':
    try: 
        print("Choose App Service Type:")
        print()
        print("Blessed Image: " + bcolors.WARNING + "[1]" + bcolors.ENDC)
        print("Web App for Container Public Image: " + bcolors.WARNING + "[2]" + bcolors.ENDC)
        print("Web App for Container Azure Container Registry Private Image: "  + bcolors.WARNING + "[3]" + bcolors.ENDC)
        x = input("Enter 1,2, or 3: ")
        if int(x) not in ([1,2,3]):
            x = ''
            print('Incorrect value, enter: 1, 2, or 3')
    except ValueError:
        print('Incorrect Value, enter: 1, 2, or 3')

if int(x) == 1:
    f = open ('main.bicep', 'w')
    f.write(bicep_code['appserviceplan'])
    f.write('\n')
    f.write(bicep_code['appserviceblessedimage'])
    f.close()
    deploy_name = subprocess.run(["az", "account", "show"], capture_output=True)
    name = json.loads(deploy_name.stdout)['user']['name']
    user_name = name.split('@')[0]
    d_name = user_name + '-appserviceblessedimage-' + str(random.randint(0, 9))
elif (int(x) == 2):
    print('Not implemented')
elif (int(x) == 3):
    print('Not implemented')

done = False
additional_services = []
while done == False:
    print("Select additional services to add: ")
    print('Vnet Intergration [1] ')
    print('Private Endpoint [2]')
    print('Storage Mount Blob [3]')
    print('Storage Mount File [4]')
    print('App GateWay [5]')
    print('KeyVault [6]')
 
    y = input()
    additional_services.append(y)
    print(additional_services)






# #az group create --name $name --location eastus
# subprocess.run(["az", "group", "create", "--name", d_name, "--location", "eastus"])
# #az deployment group create --resource-group $name --template-file main.bicep
# subprocess.run(["az", "deployment", "group", "create", "--resource-group", d_name, "--template-file", "main.bicep"])


