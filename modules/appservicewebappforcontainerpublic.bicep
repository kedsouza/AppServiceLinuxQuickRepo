var location = resourceGroup().location

param user string
param id string
param appServicePlanName string

resource appservice 'Microsoft.Web/sites@2024-04-01' = {
  name: '${user}-appsvc-${id}'
  location: location
  properties : {
    serverFarmId: appServicePlanName
    siteConfig: {
      linuxFxVersion: 'DOCKER|nginx:latest'
  }
  }
}

@description('The name of the app service:')
output appservicename string = appservice.name
