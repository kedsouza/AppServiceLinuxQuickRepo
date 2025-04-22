var location = resourceGroup().location

param appServicePlanName string

resource appservice 'Microsoft.Web/sites@2024-04-01' = {
  name: appServicePlanName
  location: location
  properties : {
    serverFarmId: appServicePlanName
    siteConfig: {
      linuxFxVersion: 'DOCKER|nginx:latest'
  }
  }
}
