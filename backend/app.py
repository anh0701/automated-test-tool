from flask import Flask
from flask_cors import CORS
from routes.checker import checker_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(checker_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
