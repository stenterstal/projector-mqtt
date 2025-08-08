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
        url = 'https://api.open-meteo.com/v1/forecast?latitude='+latitude+'&longitude='+longitude+'&daily=temperature_2m_max,temperature_2m_min,weather_code&forecast_days=1'
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
