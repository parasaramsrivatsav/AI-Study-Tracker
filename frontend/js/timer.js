let timerInterval = null;
let totalSeconds = 25 * 60;
let remainingSeconds = totalSeconds;
let isTimerRunning = false;

function updateTimerDisplay() {
  const display = document.getElementById('timer-display');
  if (!display) return;
  
  const mins = Math.floor(remainingSeconds / 60);
  const secs = remainingSeconds % 60;
  display.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function setTimerMinutes(minutes) {
  if (isTimerRunning) {
    toggleTimer();
  }
  totalSeconds = minutes * 60;
  remainingSeconds = totalSeconds;
  updateTimerDisplay();
}

function toggleTimer() {
  const btn = document.getElementById('start-timer-btn');
  if (isTimerRunning) {
    clearInterval(timerInterval);
    isTimerRunning = false;
    if (btn) btn.textContent = '▶ Start Timer';
  } else {
    isTimerRunning = true;
    if (btn) btn.textContent = '⏸ Pause Timer';
    
    timerInterval = setInterval(() => {
      if (remainingSeconds > 0) {
        remainingSeconds--;
        updateTimerDisplay();
      } else {
        clearInterval(timerInterval);
        isTimerRunning = false;
        if (btn) btn.textContent = '▶ Start Timer';
        alert("🎉 Pomodoro Focus Session Complete! Great job!");
      }
    }, 1000);
  }
}

function resetTimer() {
  if (isTimerRunning) {
    toggleTimer();
  }
  remainingSeconds = totalSeconds;
  updateTimerDisplay();
}

document.addEventListener('DOMContentLoaded', () => {
  updateTimerDisplay();
});
