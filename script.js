const form = document.getElementById("predictForm");
const studentNameInput = document.getElementById("studentName");
const subjectInput = document.getElementById("subject");
const marksInput = document.getElementById("marks");

const predictBtn = document.getElementById("predictBtn");
const spinner = document.getElementById("spinner");
const resultCard = document.getElementById("resultCard");
const performanceTitle = document.getElementById("performanceTitle");
const performanceSubtitle = document.getElementById("performanceSubtitle");
const performanceMessage = document.getElementById("performanceMessage");
const progressBar = document.getElementById("progressBar");
const themeToggle = document.getElementById("themeToggle");

let chartInstance = null;

const chartConfigDefaults = {
  type: "bar",
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 550,
      easing: "easeOutQuad",
    },
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
        max: 100,
        grid: {
          color: "rgba(255, 255, 255, 0.12)",
        },
        ticks: {
          color: "rgba(255, 255, 255, 0.75)",
          stepSize: 10,
        },
      },
    },
  },
};

function formatTitle(score) {
  if (score < 40) return "Weak Student";
  if (score <= 75) return "Average Student";
  return "Top Student";
}

function formatSubtitle(score, name, subject) {
  if (score < 40) {
    return `${name} needs targeted support in ${subject}.`;
  }
  if (score <= 75) {
    return `${name} is on the right track but can improve further.`;
  }
  return `${name} is performing very well in ${subject}!`;
}

function formatMessage(score) {
  if (score < 40) {
    return "Weak Student – Provide Important Questions and focused practice sets to build confidence and foundational skills.";
  }

  if (score <= 75) {
    return "Average Student – Provide Simplified Notes and structured exercises to strengthen concepts and increase consistency.";
  }

  return "Top Student – Provide Advanced Notes and challenge problems to maintain momentum and deepen understanding.";
}

function computeProgressWidth(score) {
  const clamped = Math.max(0, Math.min(100, score));
  return `${clamped}%`;
}

function showSpinner() {
  spinner.classList.remove("hidden");
  resultCard.classList.add("hidden");
}

function showResultCard() {
  spinner.classList.add("hidden");
  resultCard.classList.remove("hidden");
  resultCard.classList.add("fade-in");
  window.setTimeout(() => resultCard.classList.remove("fade-in"), 520);
}

function updateResult({ name, subject, marks }) {
  const score = Number(marks);
  const title = formatTitle(score);
  const subtitle = formatSubtitle(score, name, subject);
  const message = formatMessage(score);

  performanceTitle.textContent = title;
  performanceSubtitle.textContent = subtitle;
  performanceMessage.textContent = message;
  progressBar.style.width = computeProgressWidth(score);

  updateChart({ name, subject, score });
}

function updateChart({ name, subject, score }) {
  const canvas = document.getElementById("marksChart");

  const chartData = {
    labels: [subject || "Subject"],
    datasets: [
      {
        label: "Marks",
        data: [score],
        backgroundColor: "rgba(243, 195, 79, 0.8)",
        borderColor: "rgba(243, 195, 79, 1)",
        borderWidth: 2,
        borderRadius: 8,
      },
    ],
  };

  if (chartInstance) {
    chartInstance.data = chartData;
    chartInstance.update();
    return;
  }

  chartInstance = new Chart(canvas, {
    ...chartConfigDefaults,
    data: chartData,
  });
}

function setTheme(darkMode) {
  document.body.classList.toggle("dark", darkMode);
  const icon = darkMode ? "☀️" : "🌙";
  const label = darkMode ? "Light Mode" : "Dark Mode";
  themeToggle.querySelector(".toggle-icon").textContent = icon;
  themeToggle.querySelector(".toggle-label").textContent = label;
  localStorage.setItem("aiPredictorDarkMode", darkMode ? "1" : "0");
}

function initTheme() {
  const saved = localStorage.getItem("aiPredictorDarkMode");
  const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  const darkMode = saved === null ? prefersDark : saved === "1";
  setTheme(darkMode);
}

function setFormEnabled(enabled) {
  [studentNameInput, subjectInput, marksInput, predictBtn].forEach((el) => {
    el.disabled = !enabled;
  });
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const name = studentNameInput.value.trim();
  const subject = subjectInput.value.trim();
  const marks = marksInput.value.trim();

  if (!name || !subject || marks === "" || isNaN(Number(marks))) {
    alert("Please fill out all fields with valid values.");
    return;
  }

  const numericMarks = Number(marks);
  if (numericMarks < 0 || numericMarks > 100) {
    alert("Marks must be between 0 and 100.");
    return;
  }

  setFormEnabled(false);
  showSpinner();

  window.setTimeout(() => {
    updateResult({ name, subject, marks: numericMarks });
    showResultCard();
    setFormEnabled(true);
  }, 2000);
});

themeToggle.addEventListener("click", () => {
  const isDark = document.body.classList.contains("dark");
  setTheme(!isDark);
});

window.addEventListener("DOMContentLoaded", () => {
  initTheme();
});
