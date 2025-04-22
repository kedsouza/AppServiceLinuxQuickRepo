var location = resourceGroup().location

param appServicePlanName string
param azureContainerRegistryName string
@secure()
param azureContainerRegistryPassword string

resource appservice 'Microsoft.Web/sites@2024-04-01' = {
  name: appServicePlanName
  location: location
  properties : {
    serverFarmId: appServicePlanName
    siteConfig: {
      linuxFxVersion: 'DOCKER|${azureContainerRegistryName}.azurecr.io/library/httpd:latest'
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
}
