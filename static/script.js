const ctx = document.getElementById('telemetryChart').getContext('2d');
const telemetryChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Humidity (%)', borderColor: '#3498db', data: [] },
            { label: 'Temperature (°C)', borderColor: '#e74c3c', data: [] },
            // Two new lines for Rainfall and pH
            { label: 'Rainfall (mm)', borderColor: '#9b59b6', data: [] },
            { label: 'pH Level', borderColor: '#f1c40f', data: [] }
        ]
    },
    options: { responsive: true, maintainAspectRatio: false }
});

async function fetchTelemetry() {
    try {
        const response = await fetch('http://localhost:5000/api/telemetry');
        const data = await response.json();
        
        // Update Text UI
        document.getElementById('soil-state').innerText = data.state;
        document.getElementById('water-vol').innerText = data.volume_ml;
        document.getElementById('pump-status').innerText = data.pump;
        // Update the new cards
        document.getElementById('rain-val').innerText = data.rainfall;
        document.getElementById('ph-val').innerText = data.ph;
        
        // Update Chart
        const timeNow = new Date().toLocaleTimeString();
        telemetryChart.data.labels.push(timeNow);
        
        telemetryChart.data.datasets[0].data.push(data.humidity);
        telemetryChart.data.datasets[1].data.push(data.temperature);
        telemetryChart.data.datasets[2].data.push(data.rainfall);
        telemetryChart.data.datasets[3].data.push(data.ph);
        
        // Keep chart clean (max 10 points)
        if (telemetryChart.data.labels.length > 10) {
            telemetryChart.data.labels.shift();
            telemetryChart.data.datasets.forEach(dataset => dataset.data.shift());
        }
        telemetryChart.update();
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Fetch new data every 3 seconds
setInterval(fetchTelemetry, 3000);