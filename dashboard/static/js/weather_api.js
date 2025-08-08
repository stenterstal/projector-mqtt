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
        url = 'https://api.open-meteo.com/v1/forecast?latitude='+latitude+'&longitude='+longitude+'&daily=temperature_2m_max,temperature_2m_min,weather_code&forecast_days=1&models=knmi_seamless'
    }
    $.ajax({
        type: "GET",
        url: url,
        success: function (data){
            const slotData = processWeatherData(data);
            setData(data, slotData)
        }
    })
}

function processWeatherData(data){
    // temperatures = data.hourly.temperature_2m.slice(6)
    averages = []
    for(i = 7; i < data.hourly.time.length; i+=3){
        // Calculate the average temperature for slot
        let temp_before = data.hourly.temperature_2m[i - 1];
        let temp_current = data.hourly.temperature_2m[i];
        let temp_after = data.hourly.temperature_2m[i + 1];

        temp_average = Math.ceil((temp_before + temp_current + temp_after) / 3)

        // Calculate the highest weather_code
        weather_code_subarray = data.hourly.weather_code.slice(i-1, i+2);
        weather_code_average = Math.max(...weather_code_subarray)

        averages.push({temp: temp_average, code: weather_code_average})
    }
    console.log(averages)
}

function setData(data, slotData){
    max_temp = Math.round(data.daily.temperature_2m_max);
    min_temp = Math.round(data.daily.temperature_2m_min)
    $('#daily_temp').html(max_temp + "° <span>"+min_temp+"°</span>")
    $('#main-weather-icon').attr('src', "/static/svg/"+getWeatherIcon(data.daily.weather_code)+'.svg')
    // slotData.forEach(slot => {
    //     print(slot)
    // })
}

function getWeatherIcon(wmo_code){
    wmoIconMappings = {
        0: "clear-day",
        1: "partly-cloudy-day",
        2: "overcast-day",
        3: "overcast",
        4: "",
    }
    return wmoIconMappings[wmo_code] || 'clear-day'
}