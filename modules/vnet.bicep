param user string
param id string
param appservicename string

var location = resourceGroup().location


resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: '${user}-vnet-${id}'
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
