param id string
param user string

param appservicename string
param vnetname string

var location = resourceGroup().location


resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' existing = {
  name:vnetname
}

resource appservice 'Microsoft.Web/sites@2024-04-01' existing = {
  name: appservicename
}


resource privateendpoint 'Microsoft.Network/privateEndpoints@2021-05-01' = {
  name: '${user}-pe-${id}'
  location: location
  
  properties: {
    subnet: {
      id: vnet.properties.subnets[1].id
    }
    privateLinkServiceConnections: [
      {
        name: 'appservicelink'
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


// resource appserviceprivateendpoint 'Microsoft.Web/sites/privateEndpointConnections@2024-04-01' = {
//   parent: appservice
//   name: 
//   properties: {
//     privateEndpoint: privateendpoint
//     privateLinkServiceConnectionState: {
//       status: 'Approved'
//     }
//   }
// }
