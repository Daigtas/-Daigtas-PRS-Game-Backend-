from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import os
from flask_cors import CORS
import functools

app = Flask(__name__)
CORS(app,
     origins=["https://game.sandboxas.lt"],
     supports_credentials=True,
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Credentials"])

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local_game.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    highscore = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(50), default=lambda: datetime.now(timezone.utc).isoformat())
    
    game_history = db.relationship('GameHistory', backref='user', lazy=True)

class GameHistory(db.Model):
    __tablename__ = 'game_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    zaidimas = db.Column(db.String(50), nullable=False)
    pc = db.Column(db.String(50), nullable=False)
    laimetojas = db.Column(db.String(50), nullable=False)

def try_db_operation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'error': 'Database error'}), 500
    return wrapper

@app.route('/')
def home():
    return "Flask API is running!"

@app.route('/register', methods=['POST'])
@try_db_operation
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST', 'OPTIONS'])
@try_db_operation
def login():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight accepted'})
        response.headers.add('Access-Control-Allow-Origin', 'https://game.sandboxas.lt')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Credentials')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    response = jsonify({'message': 'Login successful', 'user_id': user.id})
    response.headers.add('Access-Control-Allow-Origin', 'https://game.sandboxas.lt')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/game_history', methods=['POST'])
@try_db_operation
def add_game_history():
    data = request.get_json()
    user_id = data.get('user_id')
    zaidimas = data.get('zaidimas')
    pc = data.get('pc')
    laimetojas = data.get('laimetojas')
    
    game = GameHistory(
        user_id=user_id,
        zaidimas=zaidimas,
        pc=pc,
        laimetojas=laimetojas
    )
    db.session.add(game)
    db.session.commit()
    return jsonify({'message': 'Game history added'}), 201

@app.route('/game_history/<int:user_id>', methods=['GET'])
@try_db_operation
def get_game_history(user_id):
    history = GameHistory.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': g.id,
        'zaidimas': g.zaidimas,
        'pc': g.pc,
        'laimetojas': g.laimetojas
    } for g in history])

@app.route('/scoreboard', methods=['GET'])
@try_db_operation
def get_scoreboard():
    users = User.query.order_by(User.highscore.desc()).all()
    return jsonify([{
        'username': u.username,
        'highscore': u.highscore
    } for u in users])

@app.route('/update_highscore', methods=['POST'])
@try_db_operation
def update_highscore():
    data = request.get_json()
    user_id = data.get('user_id')
    new_score = data.get('highscore')
    
    user = db.session.get(User, user_id)
    if user and new_score > user.highscore:
        user.highscore = new_score
        db.session.commit()
    return jsonify({'message': 'Highscore updated'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)