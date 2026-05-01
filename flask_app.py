from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

def calculate_activity(acc_x, acc_y, acc_z):
    try:
        return math.sqrt(float(acc_x)**2 + float(acc_y)**2 + float(acc_z)**2) - 9.81
    except:
        return 0.5

def diagnostiquer(temperature, activity, gyro_x, gyro_y, spo2):
    # ... (le reste de votre fonction de diagnostic)
    return {"statut": "normal", "maladie": "En bonne santé", "confidence": 90}

@app.route('/')
def home():
    return jsonify({"app": "AgriBovin API", "status": "ok"})

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

@app.route('/predict', methods=['POST'])
def predict():
    # ... (logique de prédiction)
    pass

# Pas besoin de if __name__ == '__main__' ici ; PythonAnywhere utilise le fichier WSGI.