# Installation Guide

Follow these steps to set up the Fake News Detection System on your local machine.

## Prerequisites

1. **Python 3.x**: Download from [python.org](https://www.python.org/downloads/)
2. **Pip**: Usually comes with Python installation.

## Step 1: Clone or Set Up Project
Ensure all project files are in a single directory:
`C:\FAKE DECTION SYSTEM PROJECT 1`

## Step 2: Install Dependencies
Open your terminal (Command Prompt or PowerShell) and run:
```bash
pip install -r requirements.txt
```

## Step 3: Train the Model
You must train the model once before running the application to generate the `model.pkl` and `vectorizer.pkl` files.
```bash
python train_model.py
```
*Note: This will use the provided `dataset/news.csv`. The first run will also download necessary NLTK stopwords.*

## Step 4: Run the Application
Start the Flask development server:
```bash
python app.py
```

## Step 5: Access the Web App
Open your browser and navigate to:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

### Default Credentials
- **Admin Username**: admin
- **Admin Password**: admin123
*Note: The first user registered in the system is automatically assigned the Admin role.*
