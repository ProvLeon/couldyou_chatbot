# backend/run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Development server
    app.run(debug=True, port=5000)
else:
    # Production server (Gunicorn)
    # Add basic health check route
    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'message': 'CouldYou? Chat API is running'}, 200
