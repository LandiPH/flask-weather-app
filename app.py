from flask import Flask, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Flask Weather API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'weather': '/weather?city=<city_name>',
            'status': '/status'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city', 'London')
    try:
        # Using Open-Meteo API (no API key required)
        response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json')
        if response.status_code != 200 or not response.json().get('results'):
            return jsonify({'error': 'City not found'}), 404
        
        location = response.json()['results'][0]
        lat, lon = location['latitude'], location['longitude']
        
        weather_response = requests.get(
            f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code'
        )
        weather_data = weather_response.json()['current']
        
        return jsonify({
            'city': city,
            'latitude': lat,
            'longitude': lon,
            'temperature': weather_data['temperature_2m'],
            'weather_code': weather_data['weather_code'],
            'unit': '°C'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'app': 'flask-weather-app',
        'status': 'running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
