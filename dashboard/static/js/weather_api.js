//
// ONLY 
//
if(weather_enabled && weather_enabled === 'True'){
    getWeather(weather_latitude, weather_longitude, debug_mode == "True")
}

function getWeather(latitude, longitude, debug_mode){
    if (debug_mode){
        url = "test/weather"
    } else {
        url = 'https://api.open-meteo.com/v1/forecast?latitude='+latitude+'&longitude='+longitude+'&hourly=temperature_2m,rain,cloud_cover&timezone=auto&daily=weather_code&forecast_days=2'
    }
    $.ajax({
        type: "GET",
        url: url,
        success: function (data){
            const chartData = getChartData(data)
            setWeatherChart(chartData)
        }
    })
}

function getChartData(data){
    console.log(data)
    const labels = data.hourly.time
        .slice(0, 24)
        .map(timestamp => {
            return timestamp.slice(-5)
        });
    labels.push('24:00')

    const dataset = data.hourly.rain.slice(0, 25)
    return [labels, dataset]
}

function setWeatherChart(weather){
    const [labels, dataset] = weather
    const ctx = document.getElementById('weather-chart');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: dataset,
                borderWidth: 3,
                fill: 'start',
                pointStyle: false
            }]
        },
        options: {
            elements: {
                line: {
                    tension: 0.4
                }
            },
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                x: {
                    position: 'top',
                    ticks: {
                        maxTicksLimit: 7,
                        font: {
                            family: 'Open Sans',
                            size: 14,
                            weight: 'bold'
                        },
                        autoSkip: true,
                        callback: function(value, index, values) {
                            if (index === 0 || index === values.length - 1) {
                            return ''; // Hide the first and last ticks
                            }
                            return value
                        },
                    },
                    grid: { display: false },
                    axis: { display: false },
                    border: { display: false }
                },
                y: {
                    beginAtZero: true,
                    position: 'right',
                    ticks: {
                        maxTicksLimit: 3,
                        crossAlign: 'center',
                        font: {
                            family: 'Open Sans',
                            size: 14,
                            weight: 'bold'
                        },
                    },
                    grid: { display: false },
                    axis: { display: false },
                    border: { display: false }
                }
            }
        }
    });
}