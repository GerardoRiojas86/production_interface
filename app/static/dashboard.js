/* globals Chart:false, feather:false */

function setFieldValue(field_id, value) {
  document.getElementById(field_id).value = value;
}

function getLineChartDataSet(label, color, data) {
  return         {
    label: label,
    tension: 0.1,
    backgroundColor: 'transparent',
    borderColor: color,
    borderWidth: 4,
    pointBackgroundColor: color,
    data: data
  }
}

// Draws a timeline for rate, goal and reality of production
// Rate, goal and reality are expect to provide attributes: label, color and data
// Label: string
// Color: string (hex code)
// Data: Array of values
// Labels: List of strings to be used on the X-axis
function graphProductionTimeline(chartId, rate, goal, reality, labels) {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  var ctx = document.getElementById(chartId)

  var datasets = []

  datasets.push(getLineChartDataSet(rate['label'], rate['color'], rate['data']))
  datasets.push(getLineChartDataSet(goal['label'], goal['color'], goal['data']))
  datasets.push(getLineChartDataSet(reality['label'], reality['color'], reality['data']))

  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets
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
        display: true
      }
    }
  })


}

function graphDoughnut(chartId, labels, data, colors, title) {
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
        label: title,
        data: data,
        backgroundColor: colors,
        hoverOffset: 4
      }]
    }
  })


}