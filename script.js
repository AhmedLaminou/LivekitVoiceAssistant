// API Base URL
const API_BASE = 'http://127.0.0.1:8000';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkStatus();
    // Check status every 5 seconds
    setInterval(checkStatus, 5000);
});

/**
 * Check agent status
 */
async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        const startBtn = document.getElementById('startAgentBtn');
        const stopBtn = document.getElementById('stopAgentBtn');
        
        if (data.agent_running) {
            statusIndicator.classList.add('active');
            statusText.textContent = '✓ Agent is Running';
            statusText.style.color = '#10b981';
            startBtn.classList.add('hidden');
            stopBtn.classList.remove('hidden');
        } else {
            statusIndicator.classList.remove('active');
            statusText.textContent = '✗ Agent is Stopped';
            statusText.style.color = '#ef4444';
            startBtn.classList.remove('hidden');
            stopBtn.classList.add('hidden');
        }
    } catch (error) {
        console.error('Error checking status:', error);
        document.getElementById('statusText').textContent = '⚠️ Unable to check status';
    }
}

/**
 * Generate access token for LiveKit room
 */
async function generateToken() {
    const identityInput = document.getElementById('identity');
    const identity = identityInput.value.trim() || 'browser-user';
    
    if (!identity) {
        showMessage('Please enter a user identity', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/token?identity=${encodeURIComponent(identity)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display token results
        document.getElementById('tokenUrl').textContent = data.url;
        document.getElementById('tokenValue').textContent = data.token;
        document.getElementById('tokenResult').classList.remove('hidden');
        
        showMessage('Token generated successfully!', 'success');
    } catch (error) {
        console.error('Error generating token:', error);
        showMessage('Failed to generate token: ' + error.message, 'error');
    }
}

/**
 * Start the AI agent
 */
async function startAgent() {
    try {
        const response = await fetch(`${API_BASE}/start_agent`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        showMessage(data.message, 'success');
        
        // Update status after a short delay
        setTimeout(checkStatus, 500);
    } catch (error) {
        console.error('Error starting agent:', error);
        showMessage('Failed to start agent: ' + error.message, 'error');
    }
}

/**
 * Stop the AI agent (placeholder function)
 */
function stopAgent() {
    showMessage('Agent stop functionality coming soon', 'success');
    // You can implement actual stop endpoint in your FastAPI backend
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const button = event.target;
        const originalText = button.textContent;
        
        button.textContent = '✓ Copied!';
        button.style.background = 'rgba(16, 185, 129, 0.3)';
        button.style.borderColor = '#10b981';
        button.style.color = '#10b981';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '';
            button.style.borderColor = '';
            button.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        showMessage('Failed to copy to clipboard', 'error');
    });
}

/**
 * Show message feedback
 */
function showMessage(message, type = 'success') {
    const messageDiv = document.getElementById('agentMessage');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    messageDiv.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageDiv.classList.add('hidden');
    }, 5000);
}

/**
 * Handle Enter key in input fields
 */
document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        if (e.target.id === 'identity') {
            generateToken();
        }
    }
});
