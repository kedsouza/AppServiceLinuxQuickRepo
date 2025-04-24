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

// resource privateendpointsubnet 'Microsoft.Network/virtualNetworks/subnets@2024-05-01' = {
//     name: '${vnet.name}/privateendpointsubnet'
//     properties: {
//       addressPrefix: '10.0.3.0/27'
//     }
//   }

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2021-05-01' = {
  name: name
  location: location
  
  properties: {
    subnet: {
      id: vnet.properties.subnets[1].id
    }
    privateLinkServiceConnections: [
      {
        name: name
        properties: {
          privateLinkServiceId: appservice.id
          groupIds: [
            'sites'
          ]
        }
      }
    ]
  }
}


resource appserviceprivateendpoint 'Microsoft.Web/sites/privateEndpointConnections@2024-04-01' = {
  parent: appservice
  name: 'appserviceprivateendpointconnection'
  properties: {
    privateEndpoint: privateEndpoint
    privateLinkServiceConnectionState: {
      status: 'Approved'
      
    }
  }
}
