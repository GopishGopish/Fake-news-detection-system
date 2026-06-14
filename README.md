# Fake News Detection System

TruthVerify is a modern, full-stack web application designed to detect and combat misinformation using Machine Learning (Logistic Regression) and Natural Language Processing (TF-IDF).

## 🚀 Features

- **Real-time News Analysis**: Uses a trained Logistic Regression model to predict if news is REAL or FAKE.
- **Confidence Scores**: Displays the model's confidence level for every prediction.
- **User Authentication**: Secure registration, login, and session management with password hashing.
- **Admin Dashboard**: Comprehensive statistics, analysis counts, and recent activity monitoring.
- **Prediction History**: Users can review all their past analyses with timestamps.
- **Premium UI**: Responsive, dark-mode design built with Bootstrap 5.

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Python, Flask
- **Machine Learning**: Scikit-learn, Pandas, NLTK, TF-IDF Vectorizer
- **Database**: SQLite (SQLAlchemy ORM)

## 📁 Project Structure

```text
fake-news-detection/
│
├── app.py              # Main Flask application
├── train_model.py      # ML training script
├── model.pkl           # Saved ML model (Generated after training)
├── vectorizer.pkl      # Saved TF-IDF vectorizer (Generated after training)
├── database.db         # SQLite database file (Generated automatically)
├── requirements.txt    # Python dependencies
│
├── static/             # Static assets
│   ├── css/            # Custom styles
│   └── js/             # Frontend logic
│
├── templates/          # HTML templates (Flask/Jinja2)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── predict.html
│   └── dashboard.html
│
└── dataset/            # Data storage
    └── news.csv        # Training dataset
```

## 📝 License

This project is open-source and available under the MIT License.
