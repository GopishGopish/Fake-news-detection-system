const BACKEND_URL = 'http://localhost:5000';

// Global variables
let currentUser = null;

// Determine page context
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
const protectedPages = ['predict.html', 'history.html', 'dashboard.html'];
const authPages = ['login.html', 'register.html'];

// Initial boot check
document.addEventListener('DOMContentLoaded', async () => {
    // Apply theme immediately
    applySavedTheme();
    
    // Check auth status
    await checkAuthStatus();
    
    // Render navbar if container exists
    if (document.getElementById('navbar-container')) {
        renderNavbar();
    }
    
    // Setup page-specific logic
    initPageLogic();
});

// Theme Management
function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
}

function setupThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        // Update icon based on current theme
        const updateIcon = (theme) => {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                if (theme === 'light') {
                    icon.classList.replace('fa-moon', 'fa-sun');
                } else {
                    icon.classList.replace('fa-sun', 'fa-moon');
                }
            }
        };
        
        updateIcon(document.body.getAttribute('data-theme'));
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateIcon(newTheme);
        });
    }
}

// Authentication Check
async function checkAuthStatus() {
    try {
        const res = await fetch(`${BACKEND_URL}/api/check-auth`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include' // crucial for sharing cookies across ports
        });
        const data = await res.json();
        
        if (data.authenticated) {
            currentUser = data.user;
            // If on login/register, redirect to predict.html
            if (authPages.includes(currentPage)) {
                window.location.href = 'predict.html';
            }
        } else {
            currentUser = null;
            // If on protected page, redirect to login.html
            if (protectedPages.includes(currentPage)) {
                window.location.href = 'login.html';
            }
        }
    } catch (err) {
        console.error("Auth check failed:", err);
        if (protectedPages.includes(currentPage)) {
            window.location.href = 'login.html';
        }
    }
}

// Render dynamic navbar to prevent duplicate code and ensure correct auth views
function renderNavbar() {
    const container = document.getElementById('navbar-container');
    if (!container) return;
    
    const isAdmin = currentUser && currentUser.role === 'admin';
    const isAuthenticated = currentUser !== null;
    
    let navItems = `
        <li class="nav-item"><a class="nav-link ${currentPage === 'index.html' || currentPage === '' ? 'active' : ''}" href="index.html">Home</a></li>
    `;
    
    if (isAuthenticated) {
        navItems += `
            <li class="nav-item"><a class="nav-link ${currentPage === 'predict.html' ? 'active' : ''}" href="predict.html">Analyze</a></li>
            <li class="nav-item"><a class="nav-link ${currentPage === 'history.html' ? 'active' : ''}" href="history.html">History</a></li>
        `;
        if (isAdmin) {
            navItems += `<li class="nav-item"><a class="nav-link ${currentPage === 'dashboard.html' ? 'active' : ''}" href="dashboard.html">Dashboard</a></li>`;
        }
        navItems += `<li class="nav-item"><a class="nav-link" href="#" id="logoutBtn">Logout</a></li>`;
    } else {
        navItems += `
            <li class="nav-item"><a class="nav-link ${currentPage === 'login.html' ? 'active' : ''}" href="login.html">Login</a></li>
            <li class="nav-item"><a class="nav-link btn btn-primary ms-lg-3 py-1 text-white" href="register.html">Join Now</a></li>
        `;
    }
    
    container.innerHTML = `
        <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
            <div class="container">
                <a class="navbar-brand" href="index.html">
                    <i class="fas fa-shield-alt me-2"></i>TruthVerify ${isAdmin ? 'Admin' : ''}
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto align-items-center">
                        ${navItems}
                        <li class="nav-item ms-lg-3">
                            <button class="nav-link btn btn-link" id="themeToggle" style="border: none; background: none; color: inherit; padding: 0;">
                                <i class="fas fa-moon"></i>
                            </button>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    `;
    
    // Bind listeners
    setupThemeToggle();
    
    if (isAuthenticated) {
        document.getElementById('logoutBtn').addEventListener('click', async (e) => {
            e.preventDefault();
            await performLogout();
        });
    }
}

// Logout action
async function performLogout() {
    try {
        const res = await fetch(`${BACKEND_URL}/api/logout`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        });
        const data = await res.json();
        if (data.success) {
            window.location.href = 'index.html';
        }
    } catch (err) {
        console.error("Logout failed:", err);
        window.location.href = 'index.html'; // Fallback
    }
}

// Page-specific initialization logic
function initPageLogic() {
    if (currentPage === 'login.html') {
        initLoginLogic();
    } else if (currentPage === 'register.html') {
        initRegisterLogic();
    } else if (currentPage === 'predict.html') {
        initPredictLogic();
    } else if (currentPage === 'history.html') {
        initHistoryLogic();
    } else if (currentPage === 'dashboard.html') {
        initDashboardLogic();
    }
}

// Login Controller
function initLoginLogic() {
    const form = document.getElementById('loginForm');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = form.email.value;
        const password = form.password.value;
        
        try {
            const res = await fetch(`${BACKEND_URL}/api/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
                credentials: 'include'
            });
            const data = await res.json();
            if (res.ok && data.success) {
                window.location.href = 'predict.html';
            } else {
                showAlert(data.message || 'Login failed.', 'danger');
            }
        } catch (err) {
            showAlert('Network error. Please try again.', 'danger');
        }
    });
}

// Register Controller
function initRegisterLogic() {
    const form = document.getElementById('registerForm');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = form.username.value;
        const email = form.email.value;
        const password = form.password.value;
        
        try {
            const res = await fetch(`${BACKEND_URL}/api/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password }),
                credentials: 'include'
            });
            const data = await res.json();
            if (res.ok && data.success) {
                showAlert(data.message + ' Redirecting to login...', 'success');
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 2000);
            } else {
                showAlert(data.message || 'Registration failed.', 'danger');
            }
        } catch (err) {
            showAlert('Network error. Please try again.', 'danger');
        }
    });
}

// Predict Controller
function initPredictLogic() {
    const form = document.getElementById('predictForm');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const newsContent = document.getElementById('news_content').value;
        const btnText = document.getElementById('btnText');
        const btnLoading = document.getElementById('btnLoading');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const resultSection = document.getElementById('result-section');
        
        // Start loading state
        btnText.classList.add('d-none');
        btnLoading.classList.remove('d-none');
        analyzeBtn.disabled = true;
        resultSection.classList.add('d-none');
        
        try {
            const res = await fetch(`${BACKEND_URL}/api/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ news_content: newsContent }),
                credentials: 'include'
            });
            const data = await res.json();
            
            if (res.ok && data.success) {
                // Render results
                const badge = document.getElementById('result-badge');
                const badgeIcon = document.getElementById('result-badge-icon');
                const badgeText = document.getElementById('result-badge-text');
                const progressBar = document.getElementById('confidence-bar');
                const confidenceText = document.getElementById('confidence-text');
                
                badgeText.textContent = `${data.prediction} NEWS`;
                confidenceText.textContent = `${data.confidence.toFixed(2)}%`;
                progressBar.style.width = `${data.confidence}%`;
                
                if (data.prediction === 'REAL') {
                    badge.className = 'result-badge badge-real';
                    badgeIcon.className = 'fas fa-check-circle me-2';
                    progressBar.className = 'progress-bar bg-success';
                } else {
                    badge.className = 'result-badge badge-fake';
                    badgeIcon.className = 'fas fa-times-circle me-2';
                    progressBar.className = 'progress-bar bg-danger';
                }
                
                resultSection.classList.remove('d-none');
            } else {
                showAlert(data.message || 'Prediction failed.', 'danger');
            }
        } catch (err) {
            showAlert('Network error. Please try again.', 'danger');
        } finally {
            // Stop loading state
            btnText.classList.remove('d-none');
            btnLoading.classList.add('d-none');
            analyzeBtn.disabled = false;
        }
    });
}

// History Controller
async function initHistoryLogic() {
    const tableBody = document.getElementById('history-table-body');
    if (!tableBody) return;
    
    try {
        const res = await fetch(`${BACKEND_URL}/api/history`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        });
        const data = await res.json();
        
        if (res.ok) {
            if (data.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="text-center py-5 text-white-50">
                            No history found. <a href="predict.html" class="text-primary">Start analyzing</a>
                        </td>
                    </tr>
                `;
            } else {
                tableBody.innerHTML = data.map(item => `
                    <tr>
                        <td class="px-4 py-3">
                            <small class="text-white-50">${escapeHtml(item.news_text.substring(0, 100))}...</small>
                        </td>
                        <td class="py-3">
                            <span class="badge ${item.prediction === 'REAL' ? 'bg-success' : 'bg-danger'} ps-2 pe-2 pt-1 pb-1">
                                ${item.prediction}
                            </span>
                        </td>
                        <td class="py-3">
                            <span class="fw-bold">${item.confidence.toFixed(1)}%</span>
                        </td>
                        <td class="py-3 text-white-50">
                            <small>${item.timestamp}</small>
                        </td>
                    </tr>
                `).join('');
            }
        } else {
            showAlert('Failed to load history.', 'danger');
        }
    } catch (err) {
        showAlert('Network error loading history.', 'danger');
    }
}

// Dashboard Controller
async function initDashboardLogic() {
    const dashboardContainer = document.getElementById('dashboard-container');
    if (!dashboardContainer) return;
    
    try {
        const res = await fetch(`${BACKEND_URL}/api/dashboard`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        });
        const data = await res.json();
        
        if (res.ok && data.success) {
            // Update stats
            document.getElementById('total-analyses').textContent = data.total_analyses;
            document.getElementById('real-count').textContent = data.real_count;
            document.getElementById('fake-count').textContent = data.fake_count;
            document.getElementById('total-users').textContent = data.total_users;
            
            // Render recent activity table
            const tableBody = document.getElementById('activity-table-body');
            if (data.recent_activity.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="4" class="text-center py-4 text-white-50">No recent activity.</td></tr>`;
            } else {
                tableBody.innerHTML = data.recent_activity.map(act => `
                    <tr>
                        <td class="px-4 text-white-50">User #${act.user_id}</td>
                        <td>
                            <span class="badge ${act.prediction === 'REAL' ? 'bg-success' : 'bg-danger'} ps-2 pe-2 pt-1 pb-1">
                                ${act.prediction}
                            </span>
                        </td>
                        <td>${act.confidence.toFixed(1)}%</td>
                        <td class="text-white-50"><small>${act.timestamp}</small></td>
                    </tr>
                `).join('');
            }
            
            // Render distributions
            const realPct = data.total_analyses > 0 ? (data.real_count / data.total_analyses * 100) : 0;
            const fakePct = data.total_analyses > 0 ? (data.fake_count / data.total_analyses * 100) : 0;
            
            document.getElementById('real-percent').textContent = `${realPct.toFixed(1)}%`;
            document.getElementById('real-progress').style.width = `${realPct}%`;
            document.getElementById('fake-percent').textContent = `${fakePct.toFixed(1)}%`;
            document.getElementById('fake-progress').style.width = `${fakePct}%`;
            
        } else {
            showAlert(data.message || 'Access denied or failed to load statistics.', 'danger');
        }
    } catch (err) {
        showAlert('Network error loading dashboard statistics.', 'danger');
    }
}

// Helper to show dynamic alert messages
function showAlert(message, type = 'danger') {
    const alertBox = document.getElementById('alert-box');
    if (!alertBox) return;
    alertBox.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show animate-fade" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Auto-dismiss after 5s
    setTimeout(() => {
        const alerts = alertBox.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}
