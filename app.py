from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)

# JWT配置
app.config['JWT_SECRET_KEY'] = '123897'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

# 后续可以存储到db
users_db = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': '缺少用户名或密码'}), 400
    
    username = data['username']
    
    if username in users_db:
        return jsonify({'message': '用户已存在'}), 400
        
    hashed_password = generate_password_hash(data['password'])
    users_db[username] = hashed_password
    
    return jsonify({'message': '注册成功'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': '缺少用户名或密码'}), 400
    
    username = data['username']
    
    if username not in users_db:
        return jsonify({'message': '用户不存在'}), 404
        
    if check_password_hash(users_db[username], data['password']):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'message': '密码错误'}), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'logged_in_as': current_user}), 200


if __name__ == '__main__':
    app.run(debug=True)
