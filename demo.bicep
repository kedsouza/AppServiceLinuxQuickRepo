
module appserviceplan 'modules/appserviceplan.bicep' = {}

module appservice 'modules/appserviceblessedimage.bicep' = {
  params: {
    appServicePlanName: appserviceplan.outputs.appserviceplanname
  }
}
