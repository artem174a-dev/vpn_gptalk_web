var chartOptions = {
    legend: {
        display: false
    },
    scales: {
        xAxes: [{
            gridLines: {
                display: false
            }
        }],
        yAxes: [{
            gridLines: {
                display: false
            }
        }]
    }
};

var lineChart = new Chart(document.getElementById("line-chart"), {
    type: 'line',
    data: generateRandomData('День'),
    options: chartOptions
});

function generateRandomData(timeframe) {
    var labels, data;

    if (timeframe === 'День') {
        labels = ['00:00', '06:00', '12:00', '18:00', '00:00'];
        data = JSON.parse(document.getElementById('data_day').dataset.dayJson);
    } else if (timeframe === 'Неделя') {
        labels = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
        data = Array.from({ length: 7 }, () => Math.random());
    } else if (timeframe === 'Месяц') {
        labels = ['1', '5', '10', '15', '20', '25', '30'];
        data = Array.from({ length: 30 }, () => Math.random());
    }

    return {
        labels: labels,
        datasets: [{
            data: data,
            label: "Usage",
            borderColor: "#3e95cd",
            fill: true
        }]
    };
}

function updateChart(timeframe) {
    lineChart.data.labels = generateRandomData(timeframe).labels;
    lineChart.data.datasets[0].data = generateRandomData(timeframe).datasets[0].data;
    document.querySelector('.chart-title').innerText = timeframe;
    lineChart.update();
}