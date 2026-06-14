from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load ML components
nltk.download('stopwords', quiet=True)
ps = PorterStemmer()

try:
    model = joblib.load(os.path.join(basedir, 'model.pkl'))
    vectorizer = joblib.load(os.path.join(basedir, 'vectorizer.pkl'))
except:
    model = None
    vectorizer = None

# Models now imported from models.py

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('register'))
        
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_pw, role='user' if User.query.count() > 0 else 'admin')
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('predict'))
        else:
            flash('Login failed. Check email and password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    prediction_result = None
    confidence = 0
    news_input = ""
    
    if request.method == 'POST':
        news_input = request.form.get('news_content')
        if not news_input:
            flash('Please enter some news content.', 'warning')
        elif model is None or vectorizer is None:
            flash('ML model not loaded. Please train the model first.', 'danger')
        else:
            # Preprocess and Predict
            cleaned_text = preprocessing(news_input)
            vectorized_text = vectorizer.transform([cleaned_text])
            prediction = model.predict(vectorized_text)[0]
            
            # Confidence score (using decision_function or predict_proba)
            try:
                proba = model.predict_proba(vectorized_text)[0]
                confidence = max(proba) * 100
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
            
    return render_template('predict.html', prediction=prediction_result, confidence=confidence, news_input=news_input)

@app.route('/history')
@login_required
def history():
    user_history = PredictionHistory.query.filter_by(user_id=current_user.id).order_by(PredictionHistory.timestamp.desc()).all()
    return render_template('history.html', history=user_history)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('predict'))
    
    total_analyses = PredictionHistory.query.count()
    real_count = PredictionHistory.query.filter_by(prediction='REAL').count()
    fake_count = PredictionHistory.query.filter_by(prediction='FAKE').count()
    total_users = User.query.count()
    
    recent_activity = PredictionHistory.query.order_by(PredictionHistory.timestamp.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                          total_analyses=total_analyses, 
                          real_count=real_count, 
                          fake_count=fake_count, 
                          total_users=total_users,
                          recent_activity=recent_activity)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(username='admin').first():
            admin_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
            admin = User(username='admin', email='admin@example.com', password=admin_pw, role='admin')
            db.session.add(admin)
            db.session.commit()
            
    app.run(debug=True)
