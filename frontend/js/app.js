const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  loadDashboardData();
});

// Navigation Tab Switching
function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const tab = item.getAttribute('data-tab');
      
      navItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');

      document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
      });

      const activeView = document.getElementById(`view-${tab}`);
      if (activeView) {
        activeView.classList.add('active');
      }

      // Update Header Titles
      const pageTitle = document.getElementById('page-title');
      const pageSub = document.getElementById('page-subtitle');
      if (tab === 'dashboard') {
        pageTitle.textContent = 'Learning Dashboard';
        pageSub.textContent = 'Track study consistency, pandas analytics & ML exam readiness.';
      } else if (tab === 'timer') {
        pageTitle.textContent = 'Focus Timer & Session Logger';
        pageSub.textContent = 'Start a Pomodoro sprint and record completed study sessions.';
      } else if (tab === 'predictor') {
        pageTitle.textContent = 'AI Exam Readiness Predictor';
        pageSub.textContent = 'Scikit-Learn machine learning evaluation of student preparedness.';
        runDefaultPrediction();
      } else if (tab === 'analytics') {
        pageTitle.textContent = 'Pandas Analytics Hub';
        pageSub.textContent = 'Deep dive subject breakdown, peak productivity hours & stats.';
      } else if (tab === 'goals') {
        pageTitle.textContent = 'Goals & Consistency Streaks';
        pageSub.textContent = 'Monitor daily & weekly study targets and manage exam dates.';
      }
    });
  });
}

// Fetch Dashboard Data
async function loadDashboardData() {
  try {
    const res = await fetch(`${API_BASE}/dashboard`);
    const data = await res.json();
    
    if (data.status === 'success') {
      updateKPICards(data.summary, data.readiness);
      renderTrendChart(data.summary.daily_trend);
      renderSubjectChart(data.summary.subject_breakdown);
      renderHourlyChart(data.summary.hourly_distribution);
      renderRadarChart(data.readiness.feature_breakdown);
      populateRecentSessions();
      populateAIRecommendations(data.readiness.recommendations);
      populateSubjectAnalyticsTable(data.summary.subject_breakdown);
      updateGoalBars(data.summary);
    }
  } catch (err) {
    console.error('Failed to load dashboard data:', err);
  }
}

// Update KPI Cards
function updateKPICards(summary, readiness) {
  document.getElementById('kpi-total-hours').textContent = `${summary.total_hours} hrs`;
  document.getElementById('kpi-total-sessions').textContent = `${summary.total_sessions} logged sessions`;
  document.getElementById('kpi-current-streak').textContent = `${summary.current_streak} Days`;
  document.getElementById('kpi-longest-streak').textContent = `Longest: ${summary.longest_streak} Days`;
  document.getElementById('kpi-avg-prod').textContent = `${summary.avg_productivity} / 5`;
  
  document.getElementById('kpi-readiness-pct').textContent = `${readiness.readiness_pct}%`;
  document.getElementById('kpi-readiness-level').textContent = readiness.readiness_level;
  document.getElementById('kpi-readiness-level').style.color = readiness.level_color;

  // Banner
  document.getElementById('banner-exam-name').textContent = readiness.target_subject;
  document.getElementById('banner-readiness-pct').textContent = `${readiness.readiness_pct}%`;
  const badge = document.getElementById('banner-readiness-badge');
  badge.textContent = readiness.readiness_level;
  badge.style.background = readiness.level_color;
}

// Recent Sessions Table
async function populateRecentSessions() {
  try {
    const res = await fetch(`${API_BASE}/sessions`);
    const data = await res.json();
    const tbody = document.getElementById('recent-sessions-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';
    const recent = data.sessions.slice(0, 5);

    recent.forEach(s => {
      const tr = document.createElement('tr');
      const stars = '⭐'.repeat(s.productivity_rating);
      tr.innerHTML = `
        <td><span class="badge badge-primary">${s.subject}</span></td>
        <td>${s.topic}</td>
        <td>${s.duration} mins</td>
        <td>${stars}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error('Error fetching recent sessions:', err);
  }
}

// AI Recommendations List
function populateAIRecommendations(recs) {
  const container = document.getElementById('ai-recommendations-list');
  if (!container) return;

  container.innerHTML = '';
  recs.forEach(rec => {
    const item = document.createElement('div');
    item.style.padding = '0.75rem 1rem';
    item.style.background = 'rgba(15, 23, 42, 0.6)';
    item.style.borderRadius = '8px';
    item.style.borderLeft = '4px solid var(--primary)';
    item.style.fontSize = '0.85rem';
    item.style.color = '#cbd5e1';
    item.textContent = rec;
    container.appendChild(item);
  });
}

// Subject Analytics Table
function populateSubjectAnalyticsTable(subjects) {
  const tbody = document.getElementById('analytics-subject-tbody');
  if (!tbody) return;

  tbody.innerHTML = '';
  subjects.forEach(s => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="badge badge-primary">${s.subject}</span></td>
      <td><strong>${s.total_hours} hrs</strong></td>
      <td>${s.session_count}</td>
      <td>${s.share_pct}%</td>
      <td>⭐ ${s.avg_rating}</td>
    `;
    tbody.appendChild(tr);
  });
}

// Goals Bar Updates
function updateGoalBars(summary) {
  const dailyText = document.getElementById('goal-daily-text');
  const dailyBar = document.getElementById('goal-daily-bar');
  const weeklyText = document.getElementById('goal-weekly-text');
  const weeklyBar = document.getElementById('goal-weekly-bar');

  if (dailyText && dailyBar) {
    const today = summary.today_hours || 0.0;
    const target = summary.daily_target_hours || 4.0;
    dailyText.textContent = `${today} / ${target} Hours`;
    const pct = Math.min(100, Math.round((today / target) * 100));
    dailyBar.style.width = `${pct}%`;
  }

  if (weeklyText && weeklyBar) {
    const total = summary.total_hours || 0.0;
    const target = 25.0;
    weeklyText.textContent = `${Math.min(25.0, total)} / ${target} Hours`;
    const pct = Math.min(100, Math.round((total / target) * 100));
    weeklyBar.style.width = `${pct}%`;
  }
}

// Predictor Submission Handler
async function handlePredictorSubmit(e) {
  e.preventDefault();
  const subject = document.getElementById('pred-subject').value;
  const days = document.getElementById('pred-days').value;

  try {
    const res = await fetch(`${API_BASE}/predict-readiness`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_subject: subject, days_until_exam: days })
    });
    const data = await res.json();

    document.getElementById('ml-readiness-pct').textContent = `${data.readiness_pct}%`;
    const levelEl = document.getElementById('ml-readiness-level');
    levelEl.textContent = data.readiness_level;
    levelEl.style.color = data.level_color;

    renderRadarChart(data.feature_breakdown);

    const recBox = document.getElementById('ml-recommendations-box');
    recBox.innerHTML = '';
    data.recommendations.forEach(r => {
      const div = document.createElement('div');
      div.style.padding = '0.6rem 0.8rem';
      div.style.background = 'rgba(15, 23, 42, 0.6)';
      div.style.borderRadius = '6px';
      div.style.fontSize = '0.85rem';
      div.style.color = '#cbd5e1';
      div.textContent = `💡 ${r}`;
      recBox.appendChild(div);
    });

  } catch (err) {
    console.error('Error running ML prediction:', err);
  }
}

async function runDefaultPrediction() {
  handlePredictorSubmit({ preventDefault: () => {} });
}

// Session Submission Handler
async function handleSessionSubmit(e) {
  e.preventDefault();
  const session = {
    subject: document.getElementById('log-subject').value,
    topic: document.getElementById('log-topic').value,
    duration: parseInt(document.getElementById('log-duration').value),
    productivity_rating: parseInt(document.getElementById('log-rating').value),
    notes: document.getElementById('log-notes').value
  };

  try {
    const res = await fetch(`${API_BASE}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(session)
    });
    if (res.ok) {
      alert('✅ Session logged successfully!');
      document.getElementById('session-form').reset();
      loadDashboardData();
    }
  } catch (err) {
    console.error('Error saving session:', err);
  }
}

// Modal Log Session Handler
function openLogModal() {
  document.getElementById('logModal').classList.add('active');
}

function closeLogModal() {
  document.getElementById('logModal').classList.remove('active');
}

function openGoalModal() {
  document.querySelector('.nav-item[data-tab="goals"]').click();
}

async function handleModalSessionSubmit(e) {
  e.preventDefault();
  const session = {
    subject: document.getElementById('modal-subject').value,
    topic: document.getElementById('modal-topic').value,
    duration: parseInt(document.getElementById('modal-duration').value),
    productivity_rating: parseInt(document.getElementById('modal-rating').value)
  };

  try {
    const res = await fetch(`${API_BASE}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(session)
    });
    if (res.ok) {
      closeLogModal();
      loadDashboardData();
      alert('✅ Study Session logged!');
    }
  } catch (err) {
    console.error('Error saving session:', err);
  }
}

// Goal Settings Handler
async function handleGoalSubmit(e) {
  e.preventDefault();
  const goals = {
    daily_target_hours: parseFloat(document.getElementById('target-daily-input').value),
    weekly_target_hours: parseFloat(document.getElementById('target-weekly-input').value),
    target_exam: document.getElementById('target-exam-input').value,
    exam_date: document.getElementById('target-date-input').value
  };

  try {
    const res = await fetch(`${API_BASE}/goals`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(goals)
    });
    if (res.ok) {
      alert('🎯 Target goals updated!');
      loadDashboardData();
    }
  } catch (err) {
    console.error('Error updating goals:', err);
  }
}
