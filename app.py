bicep_code = {
    "appserviceplan" : "module appserviceplan 'modules/appserviceplan.bicep' = {}",
    "appserviceblessedimage" : "module appservice 'modules/appserviceblessedimage.bicep' = {params: {appServicePlanName: appserviceplan.outputs.appserviceplanname}}" 
}
    





x = ''
while x == '':
    try: 
        x =  input ('Choose App Service Type: Blessed Image (1), Web App for Container Public Image (2), Web App for Container Azure Container Registry Private Image (3): \n')
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
else:
    print ('Not implemented yet:')
# print('Add what feature you want to add')
# print('Vnet Intergration ? ')
# print('Private Endpoint')
# print('Storage Mount: Blob / File ')
# print('App GateWay')
# print('Azure Front Door')
# print('Azure KeyVault')