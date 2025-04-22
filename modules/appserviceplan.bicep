var location = resourceGroup().location

param name string

resource appserviceplan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: name
  location: location
  kind: 'linux'
  sku: {
    name: 'B3'
  }
  properties: {
    reserved: true
  }
}

@description('The name of the app service plan:')
output appserviceplanname string = appserviceplan.name
