param name string
param appservicename string

var location = resourceGroup().location


resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: name
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    
    subnets: [
      {
        name: 'appservice'
        properties: {
          addressPrefix: '10.0.2.0/27'
          delegations: [
            {
              name: 'delegation'
              properties: {
                serviceName: 'Microsoft.Web/serverFarms'
              }
            }
          ]
        }
      }
      { 
        name: 'privateendpointsubnet'
        properties: {
          addressPrefix: '10.0.3.0/27'}
      }
    ]
  }
}

resource appservice 'Microsoft.Web/sites@2024-04-01' existing = {
  name: appservicename
}

resource appservicevnetconfig 'Microsoft.Web/sites/networkConfig@2024-04-01' = {
  name: 'virtualNetwork'
  parent: appservice
  properties: {
    subnetResourceId: vnet.properties.subnets[0].id
  }
}

@description('The name of the vnet:')
output vnetname string = vnet.name
