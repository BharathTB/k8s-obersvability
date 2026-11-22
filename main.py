from flask import Flask
from routes import register_routes

# Initialize Flask app
app = Flask(__name__)

#importing the metrics for prometheus
from metrics import init_metrics
init_metrics(app)

# Register all routes (API + GUI)
register_routes(app)

if __name__ == "__main__":
    # Run app in debug mode
    app.run(debug=True)
