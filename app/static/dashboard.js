/* globals Chart:false, feather:false */

function graphDailyProductivity(chartId, rate, goal, reality) {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  var ctx = document.getElementById(chartId)
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        "7:00",
        "8:00",
        "9:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00"
      ],
      datasets: [
        {
          label: 'Rate',
          tension: 0.1,
          backgroundColor: 'transparent',
          borderColor: '#1F68CB',
          borderWidth: 4,
          pointBackgroundColor: '#1F68CB',
          data: rate
        },
        {
          label: 'Goal',
          tension: 0.1,
          backgroundColor: 'transparent',
          borderColor: '#1FCB1F',
          borderWidth: 4,
          pointBackgroundColor: '#1FCB1F',
          data: goal
        },
        {
          label: 'Reality',
          tension: 0.1,
          backgroundColor: 'transparent',
          borderColor: '#B3AFA8',
          borderWidth: 4,
          pointBackgroundColor: '#B3AFA8',
          data: reality
        }                
      ]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })


}

function graphDailyDowntime(chartId, labels, data) {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  var ctx = document.getElementById(chartId)
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        label: 'Downtime by reason',
        data: data,
        backgroundColor: [],
        hoverOffset: 4
      }]
    }
  })


}