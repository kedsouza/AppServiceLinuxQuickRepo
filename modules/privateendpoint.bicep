param name string
param appservicename string
param vnetname string

var location = resourceGroup().location


resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' existing = {
  name:vnetname
}

resource appservice 'Microsoft.Web/sites@2024-04-01' existing = {
  name: appservicename
}

resource appserviceprivateendpoint 'Microsoft.Web/sites/privateEndpointConnections@2024-04-01' = {
  parent: appservice
  kind: 'string'
  name: 'string'
  properties: {
    ipAddresses: [
      'string'
    ]
    privateEndpoint: {}
    privateLinkServiceConnectionState: {
      actionsRequired: 'string'
      description: 'string'
      status: 'string'
    }
  }
}
