from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
import os
import datetime
from models import db, User, PredictionHistory

# Initializations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fake_news_detector_secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for frontend origin with credentials support
CORS(app, supports_credentials=True, origins=["http://localhost:8000", "http://127.0.0.1:8000"])

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Load ML components
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
ps = PorterStemmer()

try:
    model = joblib.load(os.path.join(basedir, 'model.pkl'))
    vectorizer = joblib.load(os.path.join(basedir, 'vectorizer.pkl'))
except:
    model = None
    vectorizer = None

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Preprocessing function
STOPWORDS = set(stopwords.words('english'))

def preprocessing(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [ps.stem(word) for word in stemmed_content if not word in STOPWORDS]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

# Routes
@app.route('/')
def api_root():
    return jsonify({
        "status": "healthy",
        "service": "TruthVerify Backend API",
        "version": "1.0.0"
    })

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            "authenticated": True,
            "user": {
                "username": current_user.username,
                "email": current_user.email,
                "role": current_user.role
            }
        })
    return jsonify({"authenticated": False})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No input data provided"}), 400
        
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400
        
    user_exists = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
    if user_exists:
        return jsonify({"success": False, "message": "Username or Email already exists."}), 409
        
    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=hashed_pw, role='user' if User.query.count() > 0 else 'admin')
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Registration successful. Please login."})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No credentials provided"}), 400
        
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400
        
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        })
    else:
        return jsonify({"success": False, "message": "Login failed. Check email and password."}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"success": True, "message": "Logged out successfully"})

@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No text provided"}), 400
        
    news_input = data.get('news_content')
    if not news_input:
        return jsonify({"success": False, "message": "Please enter some news content."}), 400
        
    if model is None or vectorizer is None:
        return jsonify({"success": False, "message": "ML model not loaded. Please train the model first."}), 503
        
    # Preprocess and Predict
    cleaned_text = preprocessing(news_input)
    vectorized_text = vectorizer.transform([cleaned_text])
    prediction = model.predict(vectorized_text)[0]
    
    # Confidence score (using decision_function or predict_proba)
    try:
        proba = model.predict_proba(vectorized_text)[0]
        confidence = float(max(proba) * 100)
    except:
        confidence = 100.0 # Default if proba not available
    
    prediction_result = 'REAL' if prediction == 'REAL' or prediction == 1 else 'FAKE'
    
    # Save to history
    history = PredictionHistory(
        user_id=current_user.id,
        news_text=news_input[:500], # Store first 500 chars
        prediction=prediction_result,
        confidence=confidence
    )
    db.session.add(history)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "prediction": prediction_result,
        "confidence": confidence
    })

@app.route('/api/history', methods=['GET'])
@login_required
def history():
    user_history = PredictionHistory.query.filter_by(user_id=current_user.id).order_by(PredictionHistory.timestamp.desc()).all()
    history_list = []
    for item in user_history:
        history_list.append({
            "id": item.id,
            "news_text": item.news_text,
            "prediction": item.prediction,
            "confidence": item.confidence,
            "timestamp": item.timestamp.strftime('%Y-%m-%d %H:%M')
        })
    return jsonify(history_list)

@app.route('/api/dashboard', methods=['GET'])
@login_required
def dashboard():
    if current_user.role != 'admin':
        return jsonify({"success": False, "message": "Admin access required."}), 403
        
    total_analyses = PredictionHistory.query.count()
    real_count = PredictionHistory.query.filter_by(prediction='REAL').count()
    fake_count = PredictionHistory.query.filter_by(prediction='FAKE').count()
    total_users = User.query.count()
    
    recent_activity = PredictionHistory.query.order_by(PredictionHistory.timestamp.desc()).limit(10).all()
    recent_list = []
    for activity in recent_activity:
        recent_list.append({
            "id": activity.id,
            "user_id": activity.user_id,
            "prediction": activity.prediction,
            "confidence": activity.confidence,
            "timestamp": activity.timestamp.strftime('%H:%M:%S')
        })
        
    return jsonify({
        "success": True,
        "total_analyses": total_analyses,
        "real_count": real_count,
        "fake_count": fake_count,
        "total_users": total_users,
        "recent_activity": recent_list
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(username='admin').first():
            admin_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
            admin = User(username='admin', email='admin@example.com', password=admin_pw, role='admin')
            db.session.add(admin)
            db.session.commit()
            
    app.run(debug=True, port=5000)
