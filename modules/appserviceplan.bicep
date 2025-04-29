var location = resourceGroup().location

param id string
param user string

resource appserviceplan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: '${user}-asp-${id}'
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
