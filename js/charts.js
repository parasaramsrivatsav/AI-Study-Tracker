let trendChartInstance = null;
let subjectChartInstance = null;
let hourlyChartInstance = null;
let radarChartInstance = null;

const chartColors = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'];

function renderTrendChart(dailyData) {
  const ctx = document.getElementById('trendChart');
  if (!ctx) return;

  const labels = dailyData.map(d => d.label);
  const data = dailyData.map(d => d.hours);

  if (trendChartInstance) {
    trendChartInstance.destroy();
  }

  trendChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Study Hours',
        data: data,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.15)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#6366f1',
        pointRadius: 4,
        borderWidth: 3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          titleColor: '#fff',
          bodyColor: '#cbd5e1',
          borderColor: 'rgba(255,255,255,0.1)',
          borderWidth: 1
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' }
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' },
          beginAtZero: true
        }
      }
    }
  });
}

function renderSubjectChart(subjectData) {
  const ctx = document.getElementById('subjectChart');
  if (!ctx) return;

  const labels = subjectData.map(s => s.subject);
  const data = subjectData.map(s => s.total_hours);

  if (subjectChartInstance) {
    subjectChartInstance.destroy();
  }

  subjectChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: chartColors.slice(0, subjectData.length),
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { color: '#cbd5e1', font: { size: 12 }, padding: 12 }
        }
      },
      cutout: '70%'
    }
  });
}

function renderHourlyChart(hourlyData) {
  const ctx = document.getElementById('hourlyChart');
  if (!ctx) return;

  const labels = hourlyData.map(h => `${h.hour}:00`);
  const data = hourlyData.map(h => h.hours);

  if (hourlyChartInstance) {
    hourlyChartInstance.destroy();
  }

  hourlyChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Hours Studied',
        data: data,
        backgroundColor: '#06b6d4',
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 10 } } },
        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' }, beginAtZero: true }
      }
    }
  });
}

function renderRadarChart(featureBreakdown) {
  const ctx = document.getElementById('radarChart');
  if (!ctx) return;

  const labels = featureBreakdown.map(f => f.feature);
  const data = featureBreakdown.map(f => f.score);

  if (radarChartInstance) {
    radarChartInstance.destroy();
  }

  radarChartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Preparedness Score',
        data: data,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.25)',
        pointBackgroundColor: '#10b981',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        r: {
          angleLines: { color: 'rgba(255,255,255,0.1)' },
          grid: { color: 'rgba(255,255,255,0.1)' },
          pointLabels: { color: '#cbd5e1', font: { size: 10 } },
          ticks: { display: false },
          suggestedMin: 0,
          suggestedMax: 100
        }
      }
    }
  });
}
