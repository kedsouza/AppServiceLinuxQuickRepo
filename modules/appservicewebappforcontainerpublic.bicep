


var location = resourceGroup().location

param appServicePlanName string

resource appservice 'Microsoft.Web/sites@2024-04-01' = {
  name: 'asp-${uniqueString(resourceGroup().id)}'
  location: location
  properties : {
    serverFarmId: appServicePlanName
    siteConfig: {
      linuxFxVersion: 'DOCKER|nginx:latest'
  }
  }
}
