from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

def calculate_activity(acc_x, acc_y, acc_z):
    """Calcule le score d'activité à partir des accélérations."""
    try:
        return math.sqrt(float(acc_x)**2 + float(acc_y)**2 + float(acc_z)**2) - 9.81
    except (TypeError, ValueError):
        return 0.5

def diagnostiquer(temperature, activity, gyro_x, gyro_y, spo2):
    """Retourne un diagnostic basé sur les paramètres."""
    # Nettoyage et valeurs par défaut
    temp = float(temperature) if temperature is not None else 38.5
    act = float(activity) if activity is not None else 0.5
    gyro_x = float(gyro_x) if gyro_x is not None else 0.0
    gyro_y = float(gyro_y) if gyro_y is not None else 0.0
    spo2 = float(spo2) if spo2 is not None else 98.0

    boiterie = abs(gyro_x) + abs(gyro_y)

    # Ordre des priorités (du plus grave au moins grave)
    if temp > 40.5:
        return {"statut": "critique", "maladie": "Fièvre très élevée", "confidence": 95}
    if spo2 < 88:
        return {"statut": "critique", "maladie": "Détresse respiratoire sévère", "confidence": 92}
    if boiterie > 0.012 and act < 0.5:
        return {"statut": "critique", "maladie": "Boiterie sévère", "confidence": 88}
    if temp > 39.5 and act < 0.6:
        return {"statut": "alerte", "maladie": "Fièvre modérée", "confidence": 78}
    if boiterie > 0.008 and act < 0.7:
        return {"statut": "alerte", "maladie": "Boiterie légère", "confidence": 75}
    if spo2 < 93:
        return {"statut": "alerte", "maladie": "Légère hypoxie", "confidence": 80}
    if act < 0.25 and act > 0:
        return {"statut": "alerte", "maladie": "Léthargie", "confidence": 70}

    return {"statut": "normal", "maladie": "Aucune anomalie détectée", "confidence": 90}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"app": "AgriBovin IA API", "status": "ok", "version": "1.0"})

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint de prédiction.
    Attend un JSON avec (au moins) : temperature, acc_x, acc_y, acc_z, gyro_x, gyro_y, spo2
    Exemple :
    {
        "temperature": 39.8,
        "acc_x": 0.12,
        "acc_y": -0.05,
        "acc_z": 9.81,
        "gyro_x": 0.001,
        "gyro_y": 0.002,
        "spo2": 97
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée reçue"}), 400

        # Calcul de l'activité
        activity = calculate_activity(
            data.get('acc_x', 0),
            data.get('acc_y', 0),
            data.get('acc_z', 9.81)
        )

        # Diagnostic
        result = diagnostiquer(
            data.get('temperature'),
            activity,
            data.get('gyro_x'),
            data.get('gyro_y'),
            data.get('spo2')
        )

        # Ajout des métriques brutes pour information
        result['metrics'] = {
            'temperature': float(data.get('temperature', 38.5)),
            'activity_score': round(activity, 3),
            'spo2': float(data.get('spo2', 98))
        }

        return jsonify({"success": True, "diagnostic": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)