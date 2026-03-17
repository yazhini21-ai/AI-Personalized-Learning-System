const form = document.getElementById("predictForm");
const studentNameInput = document.getElementById("studentName");
const subjectInput = document.getElementById("subject");
const marksInput = document.getElementById("marks");
const syllabusFileInput = document.getElementById("syllabusFile");

const predictBtn = document.getElementById("predictBtn");
const spinner = document.getElementById("spinner");
const resultCard = document.getElementById("resultCard");
const performanceTitle = document.getElementById("performanceTitle");
const performanceSubtitle = document.getElementById("performanceSubtitle");
const studentNameResult = document.getElementById("studentNameResult");
const subjectResult = document.getElementById("subjectResult");
const marksResult = document.getElementById("marksResult");
const generatedNotes = document.getElementById("generatedNotes");
const progressBar = document.getElementById("progressBar");
const outputDiv = document.getElementById("output");
const themeToggle = document.getElementById("themeToggle");
const fileError = document.getElementById("fileError");
const syllabusPreview = document.getElementById("syllabusPreview");
const syllabusContent = document.getElementById("syllabusContent");
const downloadNotesBtn = document.getElementById("downloadNotes");

const PDF_JS_WORKER_CDN = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.16.135/pdf.worker.min.js";
let chartInstance = null;
let lastGeneratedNotes = [];

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

function showFileError(message) {
  fileError.textContent = message;
  fileError.classList.toggle("hidden", !message);
}

function showPreview(text) {
  if (!text) {
    syllabusPreview.classList.add("hidden");
    syllabusContent.textContent = "";
    return;
  }

  syllabusPreview.classList.remove("hidden");
  syllabusContent.textContent = text.trim();
}

function displayOutput({ name, subject, marks, notes, category }) {
  if (!outputDiv) return;

  outputDiv.classList.remove("hidden");
  const items = notes.map((note) => `<li>${note}</li>`).join("");

  outputDiv.innerHTML = `
    <div class="output-inner">
      <h3>Prediction Result</h3>
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Subject:</strong> ${subject}</p>
      <p><strong>Marks:</strong> ${marks}/100</p>
      <p><strong>Category:</strong> ${category}</p>
      <h4>Generated Notes</h4>
      <ul>${items}</ul>
    </div>
  `;
}

function readTextFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(new Error("Failed to read file."));
    reader.readAsText(file, "UTF-8");
  });
}

async function readPdfFile(file) {
  if (!window.pdfjsLib) {
    throw new Error("PDF.js library not loaded.");
  }

  // Configure worker if not already set
  if (!window.pdfjsLib.GlobalWorkerOptions.workerSrc) {
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = PDF_JS_WORKER_CDN;
  }

  const arrayBuffer = await file.arrayBuffer();
  const pdf = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;

  const totalPages = pdf.numPages;
  const pageTexts = [];

  for (let pageIndex = 1; pageIndex <= totalPages; pageIndex += 1) {
    const page = await pdf.getPage(pageIndex);
    const content = await page.getTextContent();
    const text = content.items.map((item) => (item.str || "")).join(" ");
    pageTexts.push(text);
  }

  return pageTexts.join("\n");
}

async async function readSyllabusContent(file) {
  const name = file.name.toLowerCase();
  if (name.endsWith(".txt")) {
    return await readTextFile(file);
  }

  if (name.endsWith(".pdf")) {
    return await readPdfFile(file);
  }

  throw new Error("Unsupported file type. Use .txt or .pdf");
}

function parseSyllabusLines(rawText) {
  if (!rawText) return [];
  return rawText
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.length > 0);
}

function buildNotesFromLines(lines, score, subject) {
  const maxItems = score < 40 ? 3 : score <= 75 ? 5 : 8;
  const notes = lines.slice(0, maxItems);

  if (notes.length >= maxItems) {
    return notes;
  }

  const topic = subject || "the subject";
  const fallback = [];

  if (score < 40) {
    fallback.push(
      `Focus on core ${topic} concepts with short practice sets.`,
      `Work through important questions for ${topic} to build confidence.`,
      `Identify weak areas and revisit foundational material step-by-step.`
    );
  } else if (score <= 75) {
    fallback.push(
      `Review key ${topic} points and summarize concepts in your own words.`,
      `Use simplified notes and flashcards to reinforce understanding.`,
      `Practice moderate-difficulty problems to build consistency.`,
      `Build quick reference notes for ${topic} and revise them regularly.`,
      `Try simple past questions for ${topic} to reinforce learning.`
    );
  } else {
    fallback.push(
      `Explore advanced ${topic} topics and challenge yourself with harder problems.`,
      `Create comprehensive notes and try teaching concepts to someone else.`,
      `Attempt project-style questions to deepen your mastery of ${topic}.`,
      `Compare solutions and optimize your approach to ${topic} problems.`,
      `Research recent trends in ${topic} and apply them in practice.`
    );
  }

  return [...notes, ...fallback].slice(0, maxItems);
}

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

function updateChart({ subject, score }) {
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

function updateResult({ name, subject, score, notes, category }) {
  performanceTitle.textContent = category;
  performanceSubtitle.textContent = formatSubtitle(score, name, subject);
  studentNameResult.textContent = name;
  subjectResult.textContent = subject;
  marksResult.textContent = score;

  lastGeneratedNotes = notes.slice();
  generatedNotes.innerHTML = notes.map((note) => `<li>${note}</li>`).join("");
  progressBar.style.width = computeProgressWidth(score);

  updateChart({ subject, score });
  showResultCard();
}

function downloadNotes() {
  if (!lastGeneratedNotes.length) {
    alert("No notes to download. Generate notes first.");
    return;
  }

  const header = [
    `Student: ${studentNameResult.textContent}`,
    `Subject: ${subjectResult.textContent}`,
    `Marks: ${marksResult.textContent}/100`,
    `Category: ${performanceTitle.textContent}`,
    "",
    "Notes:",
  ];

  const text = [...header, ...lastGeneratedNotes.map((note) => `- ${note}`)].join("\n");
  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "notes.txt";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
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
  [studentNameInput, subjectInput, marksInput, syllabusFileInput, predictBtn].forEach((el) => {
    el.disabled = !enabled;
  });
}

async function handleFileChange() {
  showFileError("");
  const file = syllabusFileInput.files[0];
  if (!file) {
    showPreview("");
    return;
  }

  try {
    const raw = await readSyllabusContent(file);
    const previewText = raw
      .split(/\r?\n/)
      .slice(0, 12)
      .join("\n");
    showPreview(previewText);
  } catch (err) {
    showFileError(err.message);
    showPreview("");
  }
}

async function handleSubmit(event) {
  // allow being called directly (without an event)
  if (event && typeof event.preventDefault === "function") {
    event.preventDefault();
  }

  showFileError("");
  const name = studentNameInput.value.trim();
  const subject = subjectInput.value.trim();
  const marks = marksInput.value.trim();
  const file = syllabusFileInput.files[0];

  if (!name || !subject || marks === "" || isNaN(Number(marks))) {
    alert("Please fill out all fields with valid values.");
    return;
  }

  if (!file) {
    alert("Please upload a syllabus file (.txt or .pdf) before generating notes.");
    return;
  }

  if (file.name.toLowerCase().endsWith(".pdf") && !window.pdfjsLib) {
    alert("PDF.js library not loaded. Please make sure the PDF.js script is available.");
    return;
  }

  const numericMarks = Number(marks);
  if (numericMarks < 0 || numericMarks > 100) {
    alert("Marks must be between 0 and 100.");
    return;
  }

  setFormEnabled(false);
  showSpinner();

  try {
    const rawSyllabus = await readSyllabusContent(file);
    const lines = parseSyllabusLines(rawSyllabus);
    const notes = buildNotesFromLines(lines, numericMarks, subject);
    const category = formatTitle(numericMarks);

    updateResult({
      name,
      subject,
      score: numericMarks,
      notes,
      category,
    });

    displayOutput({
      name,
      subject,
      marks: numericMarks,
      notes,
      category,
    });
  } catch (err) {
    alert(err.message);
  } finally {
    setFormEnabled(true);
  }
}

// Prevent the form from submitting and reloading the page when pressing Enter
form.addEventListener("submit", (event) => {
  event.preventDefault();
});

// Expose an explicit global handler for the button's onclick attribute
window.generatePrediction = function () {
  // This is the entry point for the button click
  handleSubmit();
};

predictBtn.addEventListener("click", handleSubmit);
syllabusFileInput.addEventListener("change", handleFileChange);
downloadNotesBtn.addEventListener("click", downloadNotes);

themeToggle.addEventListener("click", () => {
  const isDark = document.body.classList.contains("dark");
  setTheme(!isDark);
});

function initPdfJs() {
  if (!window.pdfjsLib) {
    console.warn("pdfjsLib is not available; PDF upload will not work.");
    return false;
  }

  if (!window.pdfjsLib.GlobalWorkerOptions.workerSrc) {
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = PDF_JS_WORKER_CDN;
  }

  return true;
}

window.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initPdfJs();
});
