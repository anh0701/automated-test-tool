from flask import Flask
from flask_cors import CORS
from routes.checker import checker_bp
from routes.analyze import analyst_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(checker_bp)
    app.register_blueprint(analyst_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
