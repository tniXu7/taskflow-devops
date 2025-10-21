from flask import Flask, request, jsonify
import jwt
import datetime
import requests
import socket

@app.route('/info')
def service_info():
    return jsonify({
        'service': 'auth-service',
        'hostname': socket.gethostname(),
        'status': 'healthy'
    }) 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'taskflow-secret-key-2024'

@app.route('/auth/login', methods=['POST'])
def login():
    """Аутентификация пользователя"""
    data = request.get_json()
    
    if data.get('username') and data.get('password'):
        token = jwt.encode({
            'user': data['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user': {
                'username': data['username'],
                'role': 'user'
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/auth/verify', methods=['POST'])
def verify_token():
    """Проверка JWT токена"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'valid': True, 'user': decoded['user']})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({'status': 'healthy', 'service': 'auth-service'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)