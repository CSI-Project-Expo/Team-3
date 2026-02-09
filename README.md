# 🛡️ Dual-Layer Defense System

An AI-powered content safety scanner using FastAPI and React with a two-tier detection approach.

## 🎯 Features

- **Layer 1:** Fast keyword & regex-based scanning
- **Layer 2:** AI-powered semantic analysis using LiteLLM
- **Real-time Dashboard:** React frontend with live scanning
- **Multiple AI Providers:** Support for OpenAI, Anthropic, and more via LiteLLM
- **Extensible Architecture:** Easy to add new detection layers

## 🏗️ Project Structure

```
├── /backend                 # FastAPI Code (The "Brain")
│   ├── main.py              # Entry point for the server
│   ├── /layers              # Your Dual-Layer Defense
│   │   ├── keyword_layer.py # Layer 1: Regex & Keyword scanning logic
│   │   └── ai_layer.py      # Layer 2: LiteLLM "Judge" model logic
│   ├── /models              # Database schemas (MongoDB)
│   ├── requirements.txt     # Python libraries (FastAPI, LiteLLM, etc.)
│   └── .env                 # API Keys (DON'T UPLOAD TO GITHUB)
│
├── /frontend                # React Code (The "Dashboard")
│   ├── /src
│   │   ├── /components      # UI pieces (ChatBox, StatusLight)
│   │   └── App.jsx          # Main page logic
│   ├── package.json         # JS dependencies
│   └── vite.config.js       
│
├── /docs                    # Research & Team Guides
│   ├── architecture.md      # Explaining the "Dual-Layer" flow
│   └── banned_keywords.txt  # Your Layer 1 dictionary
│
├── .gitignore               # Files to ignore (node_modules, .env)
└── README.md                # Project overview & Setup instructions
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- API key for OpenAI, Anthropic, or other LiteLLM-supported provider

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Edit backend/.env with your API keys
OPENAI_API_KEY=your_key_here
```

5. Run the server:
```bash
python main.py
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 📖 Usage

1. Open `http://localhost:3000` in your browser
2. Enter a message in the text area
3. Click "Scan Message"
4. View the results showing:
   - Safety status (Safe/Unsafe)
   - Which layer detected the issue
   - Reason for the determination

## 🔧 Configuration

### Adding Custom Keywords

Edit `docs/banned_keywords.txt` to add your own banned keywords (one per line).

### Changing AI Model

Edit `backend/.env`:
```bash
# Use different models
LITELLM_MODEL=gpt-4
LITELLM_MODEL=claude-3-opus-20240229
LITELLM_MODEL=gemini/gemini-pro
```

## 📚 Documentation

- [Architecture Guide](docs/architecture.md) - Detailed system design
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when server is running)

## 🧪 Testing

### Test the API directly:
```bash
curl -X POST http://localhost:8000/check-message \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello world"}'
```

## 🔐 Security Notes

- **Never commit `.env` files** - They contain sensitive API keys
- The `.gitignore` is configured to exclude these automatically
- In production, use environment variables from your hosting provider
- Enable rate limiting for production deployments

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- LiteLLM - Multi-provider LLM gateway
- Python 3.8+

**Frontend:**
- React 18
- Vite - Fast build tool
- Modern ES6+ JavaScript

## 📝 License

This project is for educational purposes. Modify as needed for your use case.

## 👥 Team

Team-3 - Content Safety Challenge

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues or questions, please open an issue on GitHub.