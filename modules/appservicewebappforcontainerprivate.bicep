var location = resourceGroup().location


param user string
param id string
param appServicePlanName string
param azureContainerRegistryName string
@secure()
param azureContainerRegistryPassword string

resource appservice 'Microsoft.Web/sites@2024-04-01' = {
  name: '${user}-appsvc-${id}'
  location: location
  properties : {
    serverFarmId: appServicePlanName
    
    siteConfig: {
      linuxFxVersion: 'DOCKER|${azureContainerRegistryName}.azurecr.io/appsvcphp:latest'
      appSettings: [
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://${azureContainerRegistryName}.azurecr.io'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_USERNAME'
          value: azureContainerRegistryName
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_PASSWORD'
          value: azureContainerRegistryPassword
        }
      ]
    }
    
  
  }
  identity: {
    type: 'SystemAssigned'
  }
}

@description('The name of the app service:')
output appservicename string = appservice.name
