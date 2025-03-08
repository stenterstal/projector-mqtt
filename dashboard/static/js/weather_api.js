if(weather_enabled && weather_enabled === 'True'){
    getWeather(weather_latitude, weather_longitude)
}

function getWeather(latitude, longitude){
    $.ajax({
        type: "GET",
        // url: "test/weather",
        url: 'https://api.open-meteo.com/v1/forecast?latitude='+latitude+'&longitude='+longitude+'&hourly=temperature_2m,rain,cloud_cover&timezone=auto&forecast_days=2',
        success: function (data){
            const chartData = getChartData(data)
            setWeatherChart(chartData)
        }
    })
}

function getChartData(data){
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

    setTimeCursor()

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
                    tension: 0.5
                }
            },
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                x: {
                    ticks: {
                        maxTicksLimit: 7
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function setTimeCursor(){
    // Clamp the percentage to a range between 5% min and 96% max to account for the chart padding
    const clampedPercentage = 5 + (getTimeAsPercentage() / 100) * (96 - 5)
    // Translate the cursor container on the X axis
    $('#weather-chart-time-cursor').css('transform', 'translateX(calc('+clampedPercentage+'%  - 8px))');
}

function getTimeAsPercentage() {
    const now = new Date(); // Get the current time
    const hours = now.getHours(); // Get the current hour
    const minutes = now.getMinutes(); // Get the current minutes

    // Convert current time to total minutes
    const totalMinutes = (hours * 60) + minutes;

    // Total minutes in a day (24 hours * 60 minutes)
    const totalMinutesInDay = 24 * 60;

    // Calculate the percentage
    return Math.round((totalMinutes / totalMinutesInDay) * 100);
}