document.addEventListener('DOMContentLoaded', async function () {
    const message = document.getElementById('dashboardMessage');
    try {
        const response = await fetch('/api/dashboard', { cache: 'no-store' });
        if (!response.ok) throw new Error('Dashboard API returned HTTP ' + response.status);
        const data = await response.json();
        document.getElementById('totalAssessments').textContent = data.total_assessments ?? 0;
        document.getElementById('totalQuizzes').textContent = data.total_quizzes ?? 0;
        if (data.assessment) {
            document.getElementById('riskPercentage').textContent = data.assessment.risk_percentage + '%';
            document.getElementById('riskLevel').textContent = data.assessment.risk_level + ' Risk';
        }
        if (data.phishing) {
            document.getElementById('phishingPercentage').textContent = data.phishing.percentage + '%';
            document.getElementById('awarenessLevel').textContent = data.phishing.awareness_level;
        }
        const demoMode = document.querySelector('[data-demo-mode]')?.dataset.demoMode === 'true';
        message.textContent = data.assessment || data.phishing
            ? (demoMode ? 'Displaying fictional demonstration data.' : 'Displaying latest saved results.')
            : 'No saved results yet. Complete an assessment or phishing quiz.';
        if (typeof Chart === 'undefined') throw new Error('Chart.js did not load. Check your internet connection.');
        new Chart(document.getElementById('riskHistoryChart'), {
            type: 'line',
            data: {
                labels: (data.assessment_history || []).map(item => 'Assessment #' + item.id),
                datasets: [{
                    label: 'Risk Percentage',
                    data: (data.assessment_history || []).map(item => item.risk_percentage),
                    borderColor: '#f87171', backgroundColor: 'rgba(248,113,113,0.15)',
                    tension: 0.3, fill: true,
                }],
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { min: 0, max: 100 } } },
        });
        new Chart(document.getElementById('phishingHistoryChart'), {
            type: 'bar',
            data: {
                labels: (data.quiz_history || []).map(item => 'Quiz #' + item.id),
                datasets: [{
                    label: 'Awareness Percentage',
                    data: (data.quiz_history || []).map(item => item.percentage),
                    backgroundColor: '#60a5fa',
                }],
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { min: 0, max: 100 } } },
        });
    } catch (error) {
        message.textContent = 'Dashboard error: ' + error.message;
        console.error(error);
    }
});
