var location = resourceGroup().location


param id string
param user string

param vnetname string

 resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' existing = {
   name: vnetname
 }

resource publicIPAddress 'Microsoft.Network/publicIPAddresses@2023-09-01' = {
  name: '${user}-ip-${id}'
  location: location
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIPAddressVersion: 'IPv4'
    publicIPAllocationMethod: 'Static'
    idleTimeoutInMinutes: 4
  }
}

resource appgateway 'Microsoft.Network/applicationGateways@2024-05-01' = {
  
  name: '${user}-appgw-${id}'
  location: location
  properties: {
    sku: { 
     name: 'Standard_v2'
     tier: 'Standard_v2'
     family: 'Generation_2'
     capacity: 1
    }
    gatewayIPConfigurations: [
      {
        name: 'appGatewayIpConfig'
        properties: {
          subnet: {
            id: vnet.properties.subnets[2].id
          }
        }
      }
    ]
    frontendIPConfigurations: [
      {
        name: 'appGwPublicFrontendIp'
        properties: {
          privateIPAllocationMethod: 'Dynamic'
          publicIPAddress: {
            id: resourceId('Microsoft.Network/publicIPAddresses', publicIPAddress.name)
          }
        }
      }
    ]
    frontendPorts: [
      {
        name: 'port_80'
        properties: {
          port: 80
        }
      }
    ]
    backendAddressPools: [
      {
        name: 'myBackendPool'
        properties: {
          backendAddresses: [
            {fqdn: '${user}-appsvc-${id}.azurewebsites.net'}
          ]
        }
      }
    ]
    backendHttpSettingsCollection: [
      {
        name: 'mybackendHTTPSetting'
        properties: {
          port: 80
          protocol: 'Http'
          cookieBasedAffinity: 'Disabled'
          pickHostNameFromBackendAddress: true
          requestTimeout: 20
        }
      }
    ]
    httpListeners: [
      {
        name: 'myListener'
        properties: {
          frontendIPConfiguration: {
            id: resourceId('Microsoft.Network/applicationGateways/frontendIPConfigurations', '${user}-appgw-${id}', 'appGwPublicFrontendIp')
          }
          frontendPort: {
            id: resourceId('Microsoft.Network/applicationGateways/frontendPorts', '${user}-appgw-${id}', 'port_80')
          }
          protocol: 'Http'
          requireServerNameIndication: false
        }
      }
    ]
    requestRoutingRules: [
      {
        name: 'myRoutingRule'
        properties: {
          ruleType: 'Basic'
          priority: 1
          httpListener: {
            id: resourceId('Microsoft.Network/applicationGateways/httpListeners', '${user}-appgw-${id}', 'myListener')
          }
          backendAddressPool: {
            id: resourceId('Microsoft.Network/applicationGateways/backendAddressPools', '${user}-appgw-${id}' , 'myBackendPool')
          }
          backendHttpSettings: {
            id: resourceId('Microsoft.Network/applicationGateways/backendHttpSettingsCollection','${user}-appgw-${id}', 'mybackendHTTPSetting')
          }
        }
      }
    ]
  }
}

