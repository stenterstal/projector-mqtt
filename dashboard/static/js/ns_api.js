
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
            console.log(disruptions)
            updateView(disruptions)
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

function updateView(disruptions){
    // Clear all previous disruptions
    $('#disruptions').empty()
    // Add a view for each disruption
    $.each(disruptions, function (key, disruption) {
        if(disruption.type === "DISRUPTION" && disruption.isActive){
            addDisruptionView(disruption)
        }
    })
}

function addDisruptionView(disruption){
    var title = disruption.title
    var expectedDuration = disruption.expectedDuration.description

    // Construct element
    var containerElement = $('<div class="disruption">')
    // Exclamation icon (https://icons.getbootstrap.com/icons/exclamation-triangle-fill/)
    var iconElement = $('<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" class="bi bi-exclamation-triangle-fill" viewBox="0 0 16 16">\n<path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>\n</svg>')
    var textElement = $('<p>').html(
        title +
        '<br>' +
        '<span>' + expectedDuration + '</span>'
    )
    containerElement.append(iconElement)
    containerElement.append(textElement)

    // Add to container
    $('#disruptions').append(containerElement)
}