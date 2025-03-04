if(ns_enabled && ns_enabled === 'True'){
    getDisruption(ns_station_code)
}

function getDisruption(fromStationCode){
    $.ajax({
        type: "GET",
        // url: "test/disruptions",
        url: ' https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/disruptions/station/'+fromStationCode,
        headers: {
            'Ocp-Apim-Subscription-Key': ns_api_key
        },
        success: function (disruptions){
            addDisruption(disruptions)
        }
    })
}

function addDisruption(disruptions){
    // Add a view for each disruption
    $.each(disruptions, function (key, disruption) {
        let disruptionType = disruption.type
        if(["DISRUPTION", "MAINTENANCE", "WERKZAAMHEDEN"].includes(disruptionType) && disruption.isActive){
            var title = disruption.title
            var expectedDuration = getSubtitle(disruption)
            addNotification(title, expectedDuration, disruptionType)
        }
    })
}

function getSubtitle(disruption){
    var subtitle = null
    if(disruption?.expectedDuration?.description){
        subtitle = disruption.expectedDuration.description
    } else if(disruption?.summaryAdditionalTravelTime?.shortLabel){
        subtitle = disruption.summaryAdditionalTravelTime.shortLabel
    }
    return subtitle
}