var location = resourceGroup().location

param appservicename string

param id string
param user string

resource storage 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: '${user}storage${id}'
  location: location
  sku: {
    name: 'Standard_LRS'	
  }
  kind: 'BlobStorage'
  properties: {
    accessTier: 'Cold'
  }
}

resource blobServices 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01' = {
  parent: storage
  name: 'default'
}

resource containers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' =  {
  parent: blobServices
  name: 'testblob'
}

resource appservice 'Microsoft.Web/sites@2024-04-01'existing = {
  name: appservicename
}

resource storagemount 'Microsoft.Web/sites/config@2024-04-01' = {
    name: 'azurestorageaccounts'
    parent: appservice
    properties: {
       'blob ': {
          type: 'AzureBlob'
          shareName: containers.name
          mountPath: '/storageblob'
          accountName: storage.name
          accessKey: storage.listKeys().keys[0].value
      }
    }

}
