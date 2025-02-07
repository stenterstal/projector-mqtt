function updateTime(){
    const now = new Date();
    const time = now.toTimeString().slice(0, 8);
    document.getElementById('time').textContent = time
}

setInterval(updateTime, 1000)

updateTime()