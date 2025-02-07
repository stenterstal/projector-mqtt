// Get the disruptions from NS API for station Enschede
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

random()

function random(){
    $.ajax({
        url: 'https://randomuser.me/api/',
        dataType: 'json',
        success: function(data) {
            let title = data.results[0].email
            let subtitle = data.results[0].phone
            addNotification(title, subtitle)
        }
    });
}