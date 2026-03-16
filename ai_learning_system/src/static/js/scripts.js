// This file contains JavaScript code for client-side interactivity on the dashboard, enhancing user experience with dynamic content.

// Function to fetch student performance data and update the dashboard
function fetchStudentData() {
    fetch('/api/student_data')
        .then(response => response.json())
        .then(data => {
            updateDashboard(data);
        })
        .catch(error => console.error('Error fetching student data:', error));
}

// Function to update the dashboard with student performance data
function updateDashboard(data) {
    document.getElementById('student-name').innerText = data.name;
    document.getElementById('student-marks').innerText = data.marks;
    document.getElementById('student-attendance').innerText = data.attendance;
    document.getElementById('student-study-hours').innerText = data.study_hours;

    // Update performance category
    const performanceCategory = classifyPerformance(data.marks);
    document.getElementById('performance-category').innerText = performanceCategory;

    // Update recommendations
    document.getElementById('recommendations').innerText = data.recommendations.join(', ');
}

// Function to classify student performance based on marks
function classifyPerformance(marks) {
    if (marks < 50) {
        return 'Weak Student';
    } else if (marks >= 50 && marks <= 75) {
        return 'Average Student';
    } else {
        return 'Top Student';
    }
}

// Event listener for document ready
document.addEventListener('DOMContentLoaded', function() {
    fetchStudentData();
});