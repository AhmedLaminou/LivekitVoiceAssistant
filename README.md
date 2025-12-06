# 🎙️ LiveKit Voice Assistant

A real-time AI voice communication platform built with **FastAPI**, **LiveKit**, and modern web technologies. This project enables seamless voice interactions with an AI agent in a live video/audio room.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Core Functionality
- **Real-time Voice Communication** - Seamless audio streaming with LiveKit
- **AI Agent Integration** - Intelligent voice assistant powered by LiveKit agents
- **Token-based Authentication** - Secure room access with JWT tokens
- **Agent Status Monitoring** - Real-time tracking of agent state
- **Multi-user Support** - Multiple users can join the same room

### Frontend
- **Modern Web Interface** - Responsive, dark-themed dashboard
- **Live Status Updates** - Real-time agent status with visual indicators
- **Token Management** - Easy token generation and copying
- **One-Click Agent Control** - Simple start/stop interface
- **Mobile Responsive** - Works on desktop, tablet, and mobile devices

### Backend
- **FastAPI Framework** - High-performance async Python web framework
- **CORS Support** - Cross-origin requests enabled for frontend
- **Static File Serving** - Integrated HTML/CSS/JS serving
- **Async/Await Support** - Non-blocking operations for scalability

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Browser Client                          │
│  (HTML, CSS, JavaScript - Modern UI Dashboard)              │
└──────────────┬──────────────────────────────────────────────┘
               │ HTTP/WebSocket
┌──────────────▼──────────────────────────────────────────────┐
│                     FastAPI Backend                         │
│  ├─ /token endpoint (token generation)                      │
│  ├─ /start_agent endpoint (agent control)                   │
│  ├─ /status endpoint (status checking)                      │
│  └─ Static file serving                                     │
└──────────────┬──────────────────────────────────────────────┘
               │ LiveKit SDK
┌──────────────▼──────────────────────────────────────────────┐
│              LiveKit Cloud/Server                           │
│  ├─ Room Management                                         │
│  ├─ Media Routing                                           │
│  └─ Participant Tracking                                    │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│             AI Voice Agent Process                          │
│  (Python Agent Runner with LiveKit Agents SDK)              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Git** - [Download Git](https://git-scm.com/)
- **LiveKit Account** - [Create free account](https://livekit.io/)
- **LiveKit Server** - Self-hosted or cloud instance

### Required Accounts & Services
1. **LiveKit Cloud** - For room management and media routing
2. **LiveKit API Credentials** - API Key and Secret
3. **LiveKit Server URL** - Connection endpoint

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/LivekitVoiceAssistant.git
cd LivekitVoiceAssistant
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `livekit==0.8.1` - LiveKit Python SDK
- `livekit-agents==1.3.5` - Agent framework
- `python-dotenv==1.0.0` - Environment variable management

### 4. Create `.env` File

Create a `.env` file in the project root with your LiveKit credentials:

```env
# LiveKit Server Configuration
LIVEKIT_URL=ws://your-livekit-server:7880
LIVEKIT_API_KEY=your_api_key_here
LIVEKIT_API_SECRET=your_api_secret_here

# Optional: AI Model Configuration
OPENAI_API_KEY=your_openai_key_here
```

⚠️ **Security Note:** Never commit `.env` to version control. Add it to `.gitignore`.

---

## ⚙️ Configuration

### LiveKit Server Setup

1. **Self-hosted Option:**
   ```bash
   docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882 \
     -e LIVEKIT_API_KEY=your_key \
     -e LIVEKIT_API_SECRET=your_secret \
     livekit/livekit-server
   ```

2. **Cloud Option:**
   - Sign up at [livekit.io](https://livekit.io/)
   - Create a workspace
   - Copy credentials to `.env`

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LIVEKIT_URL` | WebSocket URL to LiveKit server | `ws://localhost:7880` |
| `LIVEKIT_API_KEY` | API key for authentication | `devkey` |
| `LIVEKIT_API_SECRET` | API secret for token generation | `secret` |
| `OPENAI_API_KEY` | (Optional) OpenAI API key for advanced features | `sk-...` |

---

## 💻 Usage

### Starting the Application

```bash
# Make sure your virtual environment is activated
uvicorn main:app --reload

# Or with custom host/port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/project']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Accessing the Application

1. Open your browser
2. Navigate to `http://127.0.0.1:8000`
3. You should see the LiveKit Voice Assistant dashboard

### Using the Interface

#### 1. **Generate Token**
- Enter a user identity (e.g., "user-123")
- Click "Generate Token"
- Copy the URL and Token for later use

#### 2. **Start Agent**
- Click "▶️ Start Agent" button
- Status indicator will turn green when running
- Agent will join the "demo-room"

#### 3. **Monitor Status**
- Status card shows real-time agent state
- Auto-updates every 5 seconds
- Green indicator = Agent running
- Red indicator = Agent stopped

---

## 🔌 API Endpoints

### 1. Generate Access Token

**Endpoint:** `GET /token`

**Parameters:**
```
identity (query): str = "browser-user"
```

**Response:**
```json
{
  "url": "ws://localhost:7880",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Example:**
```bash
curl "http://127.0.0.1:8000/token?identity=user-123"
```

---

### 2. Start Agent

**Endpoint:** `GET /start_agent`

**Response:**
```json
{
  "message": "Agent started"
}
```

**Example:**
```bash
curl "http://127.0.0.1:8000/start_agent"
```

**Notes:**
- Returns error if agent already running
- Creates async task for agent process
- Automatically joins configured room

---

### 3. Check Status

**Endpoint:** `GET /status`

**Response:**
```json
{
  "agent_running": true
}
```

**Example:**
```bash
curl "http://127.0.0.1:8000/status"
```

---

## 📁 Project Structure

```
LivekitVoiceAssistant/
├── main.py                 # FastAPI application & API endpoints
├── agent_runner.py         # AI agent implementation & room logic
├── tools.py                # Custom tools/functions for agent
├── index.html              # Web interface (HTML)
├── styles.css              # Styling & layout
├── script.js               # Frontend logic & API calls
├── .env                    # Environment variables (create this)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### File Descriptions

**`main.py`** (FastAPI Application)
- CORS middleware configuration
- Token generation endpoint
- Agent control endpoints
- Static file serving

**`agent_runner.py`** (Agent Implementation)
- `run_agent()` async function
- Room connection logic
- Agent initialization
- Event handlers

**`tools.py`** (Agent Tools)
- Custom functions available to agent
- Tool definitions and implementations

**`index.html`** (Web Interface)
- Responsive dashboard layout
- Status display
- Token management UI
- Agent control buttons

**`styles.css`** (Styling)
- Dark theme design
- Animations & transitions
- Responsive grid layout
- Component styling

**`script.js`** (Frontend Logic)
- API communication
- DOM manipulation
- Real-time status updates
- User interactions

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **Uvicorn** - ASGI server for async Python
- **LiveKit Python SDK** - Client library for LiveKit
- **LiveKit Agents** - Agent framework for building AI assistants
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients & animations
- **Vanilla JavaScript** - No frameworks, lightweight
- **Fetch API** - Async HTTP requests

### Infrastructure
- **LiveKit** - Real-time communication platform
- **WebSockets** - Bidirectional communication
- **WebRTC** - Media streaming

---

## 🐛 Troubleshooting

### Issue: "AttributeError: 'AccessToken' object has no attribute 'add_grant'"

**Solution:** Update your code to use the correct API:
```python
# ❌ Wrong
at.add_grant(api.VideoGrants(room="demo-room", room_join=True))

# ✅ Correct
at.grants = api.VideoGrants(room="demo-room", room_join=True)
```

---

### Issue: "RuntimeError: There is no current event loop in thread"

**Solution:** Make async endpoints actually async:
```python
# ❌ Wrong
@app.get("/start_agent")
def start_agent():
    agent_task = asyncio.create_task(run_agent(url, token))

# ✅ Correct
@app.get("/start_agent")
async def start_agent():
    agent_task = asyncio.create_task(run_agent(url, token))
```

---

### Issue: "Connection refused" to LiveKit server

**Troubleshooting:**
1. Check LiveKit server is running
   ```bash
   curl http://localhost:7880/health
   ```

2. Verify `LIVEKIT_URL` in `.env` is correct

3. For cloud instances, ensure firewall allows WebSocket (port 7880/7881)

4. Check API Key and Secret are correct

---

### Issue: Agent not showing in room

**Troubleshooting:**
1. Verify agent started successfully via status endpoint
2. Check agent logs in `agent_runner.py`
3. Ensure room name matches in token and agent
4. Verify `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` are correct

---

### Issue: CORS errors in browser console

**Troubleshooting:**
```python
# Already configured in main.py, but ensure it's set to:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Issue: Static files not serving

**Troubleshooting:**
1. Ensure `index.html`, `styles.css`, `script.js` are in project root
2. Restart FastAPI server
3. Check file paths in index.html:
   ```html
   <link rel="stylesheet" href="styles.css">
   <script src="script.js"></script>
   ```

---

## 📚 Additional Resources

- **LiveKit Documentation** - https://docs.livekit.io/
- **FastAPI Documentation** - https://fastapi.tiangolo.com/
- **LiveKit Agents SDK** - https://github.com/livekit/agents
- **WebRTC Documentation** - https://webrtc.org/
- **Python AsyncIO** - https://docs.python.org/3/library/asyncio.html

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎯 Roadmap

- [ ] Advanced agent customization UI
- [ ] Recording room sessions
- [ ] Multiple agent types
- [ ] Real-time transcription display
- [ ] Agent analytics dashboard
- [ ] Docker containerization
- [ ] Kubernetes deployment templates
- [ ] Unit tests & integration tests

---

## ❓ FAQ

**Q: Can I use this with cloud-hosted LiveKit?**
- A: Yes! Just update `LIVEKIT_URL` to your cloud instance endpoint.

**Q: How many users can join simultaneously?**
- A: Limited by LiveKit server capacity (typically thousands with proper setup).

**Q: Can I customize the AI agent's behavior?**
- A: Yes, modify `agent_runner.py` and `tools.py` to customize the agent.

**Q: Is this production-ready?**
- A: This is a starter template. Add authentication, error handling, and monitoring for production.

**Q: How do I add voice features?**
- A: LiveKit handles audio/video. Implement speech recognition/synthesis in `agent_runner.py`.

---

## 📞 Support

For issues and questions:
- **GitHub Issues** - [Create an issue](https://github.com/yourusername/LivekitVoiceAssistant/issues)
- **LiveKit Community** - https://livekit.io/community
- **Email** - ahmedlaminouamadou@gmail.com

---

## 🌟 Acknowledgments

- LiveKit team for the amazing real-time communication platform
- FastAPI for the modern Python web framework
- The open-source community

---

**Happy coding! 🚀**

Last Updated: December 6, 2025

