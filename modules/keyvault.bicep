var location = resourceGroup().location

param name string

resource kevyault 'Microsoft.KeyVault/vaults@2024-11-01' = {
  name: 'k${name}'
  location: location
  properties: {
    sku: {
      name: 'standard'
      family: 'A'
    }
    tenantId: tenant().tenantId
    accessPolicies: [
      
    ]
  }
}
