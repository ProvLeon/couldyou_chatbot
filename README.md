<div align="center">
  <h1 style="border-bottom: none">
    CouldYou? Cup AI Assistant
  </h1>
  <p style="font-size: 1.4em; font-weight: 300; margin-top: -0.5em; margin-bottom: 1em;">
    Empowering Menstrual Health Knowledge
  </p>

  <img src="frontend/public/logo.png" alt="CouldYou? Cup" width="200" style="margin: 2em 0" />

  <p style="max-width: 800px; margin: 1em auto;">
    An intelligent chatbot system designed to provide information and support about menstrual health and the CouldYou? Cup. This project combines a modern React frontend with a Flask-powered AI backend to deliver accurate, compassionate responses to menstrual health questions.
  </p>

  <p>
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" />
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome" />
    <img src="https://img.shields.io/badge/powered%20by-Flask-blue.svg" alt="Powered by Flask" />
    <img src="https://img.shields.io/badge/Made%20with-Next.js-000000.svg" alt="Made with Next.js" />
  </p>
</div>

## 🌟 Features

### User Interface
- 💬 Real-time chat interface with smooth animations
- 📱 Responsive design for all devices
- 🌐 Multi-language support
- 🎨 Markdown formatting for structured responses
- 📋 Message copy functionality
- ⌨️ Keyboard shortcuts
- 🕒 Message timestamps and read receipts

### Backend Intelligence
- 🤖 Google Gemini AI integration
- 💭 Context-aware conversations
- 🔄 Session management
- 🌍 Translation services
- 📚 Comprehensive knowledge base
- 🛡️ Error handling and recovery

## 🏗️ Architecture

```
couldyou_chatbot/
├── frontend/                # Next.js frontend application
│   ├── app/                # App router and pages
│   ├── components/         # React components
│   ├── context/           # React context providers
│   └── public/            # Static assets
│
├── backend/               # Flask backend service
│   ├── app/              # Application code
│   │   ├── services/     # Business logic
│   │   └── routes.py     # API endpoints
│   └── config.py         # Configuration
│
└── docs/                 # Documentation
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- Google API key for Gemini
- MongoDB (optional)

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000

# Start development server
npm run dev
```

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env
FLASK_ENV=development
GOOGLE_API_KEY=your-key-here
SECRET_KEY=your-secret-key

# Start server
python run.py
```

## 🔧 Technologies

### Frontend
- [Next.js 13+](https://nextjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Framer Motion](https://www.framer.com/motion/)
- [React Markdown](https://remarkjs.github.io/react-markdown/)

### Backend
- [Flask](https://flask.palletsprojects.com/)
- [Google Generative AI](https://ai.google.dev/)
- [MongoDB](https://www.mongodb.com/)
- [Python-Jose](https://python-jose.readthedocs.io/)

## 📝 API Documentation

### Chat Endpoint
```http
POST /api/chat
Content-Type: application/json

{
    "message": "How do I use the CouldYou? Cup?",
    "session_id": "optional-session-id",
    "language": "en"
}
```

Response:
```json
{
    "session_id": "uuid",
    "response": {
        "type": "chat",
        "text": "Here's how to use the CouldYou? Cup..."
    }
}
```

## 🔒 Security

- CORS protection
- Rate limiting
- Input validation
- Secure session management
- Environment variable protection
- Data encryption

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm run test
```

### Backend Tests
```bash
cd backend
pytest
```

## 📦 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Docker)
```bash
cd backend
docker build -t couldyou-chatbot .
docker run -p 5000:5000 couldyou-chatbot
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- Frontend Development: [Name]
- Backend Development: [Name]
- AI Integration: [Name]
- UI/UX Design: [Name]

## 🙏 Acknowledgments

- [CouldYou?](https://couldyou.org) for their mission in menstrual health
- Google for providing the Generative AI API
- The open source community for various tools and libraries

## 📞 Support

For support:
- 📧 Email: support@couldyou.org
- 🌐 Website: https://couldyou.org
- 📱 Social Media: @couldyoucup

## 🔄 Version History

- 1.0.0
  - Initial Release
  - Basic chat functionality
  - Multi-language support
- 1.1.0
  - Enhanced AI responses
  - Improved UI/UX
  - Mobile optimization

## 🗺️ Roadmap

- [ ] Voice interface
- [ ] Image recognition for product queries
- [ ] Community forum integration
- [ ] Offline support
- [ ] Enhanced analytics

## 💡 Development Notes

- Follow [Conventional Commits](https://www.conventionalcommits.org/)
- Use TypeScript for all new features
- Maintain test coverage above 80%
- Document all API changes

## 🌐 Environmental Impact

This project is designed with sustainability in mind:
- Efficient caching strategies
- Optimized asset delivery
- Minimal database operations
- Green hosting providers
