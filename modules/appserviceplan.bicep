var location = resourceGroup().location

resource appserviceplan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: 'asp-${uniqueString(resourceGroup().id)}'
  location: location
  kind: 'linux'
  sku: {
    name: 'B2'
  }
  properties: {
    reserved: true
  }
}

@description('The name of the app service plan:')
output appserviceplanname string = appserviceplan.name
