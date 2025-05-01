var location = resourceGroup().location

param user string
param id string
param appServicePlanName string

var identity = false

resource appservice 'Microsoft.Web/sites@2024-04-01' = {
  name: '${user}-appsvc-${id}'
  location: location
  properties : {
    serverFarmId: appServicePlanName
    siteConfig: {
      linuxFxVersion: 'PHP|8.4'
      alwaysOn: true
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}

@description('The name of the app service:')
output appservicename string = appservice.name
