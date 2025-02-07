
getDisruption('ES')

function getDisruption(fromStationCode){
    $.ajax({
        type: "GET",
        url: "disruptions",
        // url: ' https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/disruptions/station/'+fromStationCode,
        headers: {
            'Ocp-Apim-Subscription-Key': ''
        },
        success: function (disruptions){
            // console.log(disruptions)
            addDisruption(disruptions)
        }
    })
}

// function filterDisruptions(disruptions){
//     relevant_disruptions = disruptions.filter((disruption) => {
//         // Get the array(s) of all the names of stations involved in the disruption
//         stationNamesArray = disruption.titleSections;
//
//     })
// }

function addDisruption(disruptions){
    // Add a view for each disruption
    $.each(disruptions, function (key, disruption) {
        if(disruption.type === "DISRUPTION" && disruption.isActive){
            var title = disruption.title
            var expectedDuration = disruption.expectedDuration.description
            addNotification(title, expectedDuration, 'disruption')
        }
    })
}