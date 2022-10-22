#!/usr/bin/python3
"""Flask app module"""
from flask import Flask
from models.__init__ import storage
from api.v1.views import app_views

app = Flask(__name__)
@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_down(exception):
    """Release Resources"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)