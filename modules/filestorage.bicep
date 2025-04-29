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
  kind: 'StorageV2'
}

resource filestorage 'Microsoft.Storage/storageAccounts/fileServices@2024-01-01' = {
  name: 'default'
  parent: storage
}


resource share 'Microsoft.Storage/storageAccounts/fileServices/shares@2024-01-01' = {
  name: 'testfileshare'
  parent: filestorage
}

resource appservice 'Microsoft.Web/sites@2024-04-01'existing = {
  name: appservicename
}

resource storagemount 'Microsoft.Web/sites/config@2024-04-01' = {
    name: 'azurestorageaccounts'
    parent: appservice
    properties: {
       'blob ': {
        type :'AzureFiles'
        shareName: share.name
        mountPath: '/storagefile'
        accountName: storage.name
        accessKey: storage.listKeys().keys[0].value
      }
    }

}
