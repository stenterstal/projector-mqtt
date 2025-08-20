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
        url = 'https://api.open-meteo.com/v1/forecast?latitude='+latitude+'&longitude='+longitude+'&daily=temperature_2m_max,temperature_2m_min,weather_code&forecast_days=1&hourly=temperature_2m,weather_code&models=knmi_seamless'
    }
    $.ajax({
        type: "GET",
        url: url,
        success: function (data){
            const slotData = processWeatherData(data);
            setData(data, slots)
        }
    })
}

function processWeatherData(data){
    // temperatures = data.hourly.temperature_2m.slice(6)
    slots = []
    for(i = 7; i < data.hourly.time.length; i+=3){
        // Calculate the average temperature for slot
        let temp_before = data.hourly.temperature_2m[i - 1];
        let temp_current = data.hourly.temperature_2m[i];
        let temp_after = data.hourly.temperature_2m[i + 1];

        temp_average = Math.ceil((temp_before + temp_current + temp_after) / 3)

        // Calculate the highest weather_code
        weather_code_subarray = data.hourly.weather_code.slice(i-1, i+2);
        weather_code_average = Math.max(...weather_code_subarray)
        icon = getWeatherIcon(weather_code_average)
        hour = i + ':00'

        slots.push({temp: temp_average, icon, hour})
    }
    return slots
}

function setData(data, slots){
    max_temp = Math.round(data.daily.temperature_2m_max);
    min_temp = Math.round(data.daily.temperature_2m_min)
    $('#daily_temp').html(max_temp + "° <span>"+min_temp+"°</span>")
    $('#main-weather-icon').attr('src', "/static/svg/"+getWeatherIcon(data.daily.weather_code)+'.svg')
    $('#weather-description-text').text(getWeatherDisplayName(data.daily.weather_code[0]))

    let parent = $('#weather-slot-container')
    slots.forEach(slot => {
        let container = $('<div class="slot">')
        container.append($('<p class="time">').text(slot.hour))
        container.append($('<img>').attr('src', "/static/svg/"+slot.icon+'.svg'))
        container.append($('<p class="temp">').text(slot.temp+'°'))
        parent.append(container)
    })
}

function getWeatherIcon(wmo_code){
    wmoIconMappings = {
        // Codes for no precipitation or light weather phenomena
        0: 'clear-day', // Cloud development not observed
        1: 'clear-day', // Clouds dissolving
        2: 'clear-day', // No change in state of sky
        3: 'partly-cloudy-day', // Clouds forming
        4: 'partly-cloudy-day-smoke', // Reduced visibility due to smoke
        5: 'haze', // Haze
        6: 'dust-day', // Dust in suspension (not wind-driven)
        7: 'dust-wind', // Dust or sand raised by wind
        8: 'dust-wind', // Dust whirl or sand whirl
        9: 'dust-day', // Duststorm or sandstorm in sight
        10: 'mist', // Mist
        11: 'fog', // Shallow fog (not more than 2m on land)
        12: 'fog', // Continuous fog (more than 2m)
        13: 'thunderstorms-day', // Lightning visible but no thunder
        14: 'drizzle', // Precipitation within sight but not reaching the surface
        15: 'drizzle', // Precipitation within sight but distant
        16: 'drizzle', // Precipitation within sight near but not at the station
        17: 'thunderstorms-day', // Thunderstorm, no precipitation
        18: 'thunderstorms-day', // Squalls observed
        19: 'thunderstorms-day', // Funnel clouds (tornado or waterspout)

        // Codes for precipitation or thunderstorms
        20: 'drizzle', // Drizzle or snow grains (not as showers)
        21: 'overcast-day-rain', // Rain (not freezing)
        22: 'snow', // Snow
        23: 'overcast-day-rain', // Rain and snow or ice pellets
        24: 'overcast-day-rain', // Freezing drizzle or freezing rain
        25: 'overcast-day-rain', // Shower(s) of rain
        26: 'overcast-day-snow', // Shower(s) of snow or rain and snow
        27: 'hail', // Shower(s) of hail or rain and hail
        28: 'fog', // Fog or ice fog
        29: 'thunderstorms-day', // Thunderstorm (with or without precipitation)

        // Codes for duststorms, sandstorms, and snow
        30: 'dust-wind', // Moderate duststorm or sandstorm
        31: 'dust-wind', // Duststorm or sandstorm (no appreciable change)
        32: 'dust-wind', // Duststorm or sandstorm increasing
        33: 'dust-wind', // Severe duststorm or sandstorm (decreasing)
        34: 'dust-wind', // Duststorm or sandstorm (no change)
        35: 'dust-wind', // Duststorm or sandstorm increasing
        36: 'snow', // Slight/moderate blowing snow (low level)
        37: 'snow', // Heavy drifting snow
        38: 'snow', // Slight/moderate blowing snow (high level)
        39: 'snow', // Heavy drifting snow

        // Codes for fog or ice fog
        40: 'fog', // Fog at a distance
        41: 'fog', // Fog in patches
        42: 'fog', // Fog with visible sky, thinning
        43: 'fog', // Fog with invisible sky
        44: 'fog', // Fog with visible sky, no change
        45: 'fog', // Fog with invisible sky
        46: 'fog', // Fog with visible sky, thickening
        47: 'fog', // Fog with invisible sky, thickening
        48: 'fog', // Fog, depositing rime
        49: 'fog', // Fog, depositing rime, sky invisible

        // Codes for precipitation at the station
        50: 'drizzle', // Intermittent drizzle (slight)
        51: 'drizzle', // Continuous drizzle (slight)
        52: 'drizzle', // Intermittent drizzle (moderate)
        53: 'drizzle', // Continuous drizzle (moderate)
        54: 'drizzle', // Intermittent drizzle (heavy)
        55: 'drizzle', // Continuous drizzle (heavy)
        56: 'drizzle', // Freezing drizzle (slight)
        57: 'drizzle', // Freezing drizzle (moderate or heavy)
        58: 'drizzle', // Drizzle and rain (slight)
        59: 'drizzle', // Drizzle and rain (moderate or heavy)

        // Codes for rain
        60: 'overcast-rain', // Intermittent rain (slight)
        61: 'overcast-rain', // Continuous rain (slight)
        62: 'overcast-rain', // Intermittent rain (moderate)
        63: 'overcast-rain', // Continuous rain (moderate)
        64: 'overcast-rain', // Intermittent rain (heavy)
        65: 'overcast-rain', // Continuous rain (heavy)
        66: 'overcast-rain', // Freezing rain (slight)
        67: 'overcast-rain', // Freezing rain (moderate or heavy)
        68: 'overcast-rain', // Rain or drizzle and snow (slight)
        69: 'overcast-rain', // Rain or drizzle and snow (moderate or heavy)

        // Codes for solid precipitation (snow and ice)
        70: 'snow', // Slight intermittent snowflakes
        71: 'snow', // Continuous fall of snowflakes
        72: 'snow', // Moderate intermittent snowflakes
        73: 'snow', // Continuous moderate snowflakes
        74: 'snow', // Heavy intermittent snowflakes
        75: 'snow', // Continuous heavy snowflakes
        76: 'snow', // Diamond dust (with or without fog)
        77: 'snow', // Snow grains (with or without fog)
        78: 'snow', // Star-like snow crystals (with or without fog)
        79: 'snow', // Ice pellets

        // Codes for showery precipitation or thunderstorms
        80: 'overcast-rain', // Slight rain showers
        81: 'overcast-rain', // Moderate or heavy rain showers
        82: 'overcast-rain', // Violent rain showers
        83: 'overcast-rain', // Rain and snow mixed showers (slight)
        84: 'overcast-rain', // Rain and snow mixed showers (moderate or heavy)
        85: 'snow', // Snow showers (slight)
        86: 'snow', // Snow showers (moderate or heavy)
        87: 'hail', // Hail showers (slight)
        88: 'hail', // Hail showers (moderate or heavy)
        89: 'hail', // Hail showers (no thunder)
        90: 'hail', // Hail showers (moderate or heavy, no thunder)
        91: 'thunderstorms-day', // Slight rain, thunderstorm (no precipitation)
        92: 'thunderstorms-day', // Moderate or heavy rain, thunderstorm
        93: 'snow', // Slight snow, rain and snow mixed, hail
        94: 'snow', // Moderate or heavy snow, rain and snow mixed, hail
        95: 'thunderstorms-day', // Slight or moderate thunderstorm (with rain/snow)
        96: 'thunderstorms-day', // Slight or moderate thunderstorm (with hail)
        97: 'thunderstorms-day', // Heavy thunderstorm (no hail)
        98: 'dust-wind', // Thunderstorm with duststorm/sandstorm
        99: 'thunderstorms-day', // Heavy thunderstorm with hail
    }
    return wmoIconMappings[wmo_code] || 'clear-day'
}

function getWeatherDisplayName(code) {
    if (code === 0) return "Helder";
    if (code === 1 || code === 2) return "Soms bewolkt";
    if (code === 3) return "Bewolkt";
    if ((code >= 10 && code <= 12) || (code >= 40 && code <= 49)) return "Mist";
    if ((code >= 13 && code <= 17) || (code >= 50 && code <= 59)) return "Motregen";
    if ((code >= 18 && code <= 20) || (code >= 60 && code <= 69)) return "Regen";
    if ((code >= 21 && code <= 24) || (code >= 70 && code <= 79)) return "Sneeuw";
    if (code >= 25 && code <= 27) return "IJzel";
    if ((code >= 28 && code <= 29) || (code >= 80 && code <= 84)) return "Buien";
    if ((code >= 30 && code <= 35) || (code >= 85 && code <= 99)) return "Onweer";

    return "Onbekend";
}
