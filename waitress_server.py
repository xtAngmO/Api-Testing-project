from waitress import serve
from server import app  # Replace 'your_flask_app' with the actual import name of your Flask app

serve(app, host='0.0.0.0', port=8080)