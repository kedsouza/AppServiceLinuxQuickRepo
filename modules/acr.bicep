var location = resourceGroup().location

param id string
param user string

resource azurecontainerregistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: '${user}acr${id}'
  location: location
  sku: {
    name : 'Basic'
  }
  properties: {
    adminUserEnabled : true
  }
}


@description('The name of the acr:')
output acrname string = azurecontainerregistry.name

@description('Acr password')
output password  string = azurecontainerregistry.listCredentials().passwords[0].value
