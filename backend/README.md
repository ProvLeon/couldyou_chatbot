# CouldYou? Cup Chatbot Backend

A Flask-based backend service that powers the CouldYou? Cup chatbot, providing intelligent responses about menstrual health and the CouldYou? Cup using Google's Generative AI.

## Features

- 🤖 AI-powered responses using Google's Gemini model
- 🌐 Multi-language support with translation service
- 💬 Contextual chat management
- 🔒 Secure message handling
- 📝 Comprehensive knowledge base about menstrual health
- ⚡ Asynchronous request processing
- 🛡️ Error handling and middleware
- 🔍 Health monitoring endpoints

## Tech Stack

- **Framework**: Flask with async support
- **AI/ML**: Google Generative AI (Gemini model)
- **Database**: MongoDB (optional)
- **Security**: Python-Jose, Cryptography
- **Testing**: Pytest, Pytest-asyncio
- **Documentation**: Sphinx
- **Code Quality**: Black, Flake8, MyPy
- **Deployment**: Gunicorn

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── middleware.py        # Error handling middleware
│   ├── routes.py           # API endpoints
│   └── services/
│       ├── chat_manager.py    # Session management
│       ├── chat_service.py    # Main chat logic
│       ├── nlp_service.py     # AI integration
│       └── translation_service.py  # Language support
├── config.py               # Configuration settings
├── requirements.txt        # Dependencies
└── run.py                 # Application entry point
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/couldyou-chatbot.git
cd couldyou-chatbot/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
GOOGLE_API_KEY=your-google-api-key
MONGODB_URI=your-mongodb-uri
```

5. Run the development server:
```bash
python run.py
```

## API Endpoints

### Health Check
```
GET /
Response: { "status": "healthy", "message": "CouldYou? Chat API is running" }
```

### Chat
```
POST /api/chat
Body: {
    "message": "string",
    "session_id": "string" (optional),
    "language": "string" (default: "en")
}
Response: {
    "session_id": "string",
    "response": {
        "type": "string",
        "text": "string"
    }
}
```

### Clear Session
```
DELETE /api/sessions/<session_id>
Response: { "status": "success" }
```

## Development

### Code Style
```bash
# Format code
black .

# Sort imports
isort .

# Type checking
mypy .

# Linting
flake8
```

### Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

### Documentation
```bash
# Generate documentation
cd docs
make html
```

## Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker
```bash
# Build image
docker build -t couldyou-chatbot-backend .

# Run container
docker run -p 5000:5000 couldyou-chatbot-backend
```

## Environment Variables

- `FLASK_ENV`: Application environment (development/production)
- `SECRET_KEY`: Secret key for Flask application
- `GOOGLE_API_KEY`: Google API key for Generative AI
- `MONGODB_URI`: MongoDB connection string
- `ENCRYPTION_KEY`: Key for sensitive data encryption

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google Generative AI](https://ai.google.dev/)
- [Flask](https://flask.palletsprojects.com/)
- CouldYou? organization for their mission in menstrual health

## Support

For support, please email support@couldyou.org or raise an issue in the GitHub repository.
