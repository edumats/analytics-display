document.addEventListener('DOMContentLoaded', () => {
    const sessions = document.querySelector('#sessions');
    getData();
    setInterval(getData, 60000);
})

function getData() {
    fetch('/report')
    .then(response => response.json())
    .then(data => {
        let sessionsValue = data.reports[0].data.totals[0].values[0];
        sessions.innerHTML = sessionsValue;
    })
}
