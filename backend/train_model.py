import pandas as pd
import numpy as np
import re
import joblib
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import nltk
import os

# Download necessary NLTK datasets for text preprocessing
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

class NewsPredictorTrainer:
    def __init__(self, dataset_path):
        """
        Initializes the trainer with the data path and ML components.
        """
        self.dataset_path = dataset_path
        self.ps = PorterStemmer() # Used for word reduction
        self.vectorizer = TfidfVectorizer() # For text-to-feature conversion
        self.model = LogisticRegression() # Classification algorithm
        self.stopwords_set = set(stopwords.words('english'))

    def stemming(self, content):
        """
        Clean the text: lowercase, remove non-alphabetic characters, 
        remove stopwords, and apply stemming.
        """
        stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
        stemmed_content = stemmed_content.lower()
        stemmed_content = stemmed_content.split()
        stemmed_content = [self.ps.stem(word) for word in stemmed_content if not word in self.stopwords_set]
        stemmed_content = ' '.join(stemmed_content)
        return stemmed_content

    def train(self):
        print("Loading dataset...")
        if not os.path.exists(self.dataset_path):
            print(f"Error: Dataset not found at {self.dataset_path}")
            return

        df = pd.read_csv(self.dataset_path)
        
        # Handle missing values
        df = df.fillna('')
        
        # Combine title and text for better prediction if both exist
        # Using 'title' as specified in common datasets, but flexible
        if 'title' in df.columns and 'text' in df.columns:
            df['content'] = df['title'] + ' ' + df['text']
        elif 'text' in df.columns:
            df['content'] = df['text']
        else:
            df['content'] = df['title']

        print("Preprocessing text (stemming)... This might take a while.")
        df['content'] = df['content'].apply(self.stemming)

        # Extract features and targets
        X = df['content'].values
        y = df['label'].values # Assumes labels are 'REAL'/'FAKE' or 0/1

        # Vectorize
        print("Vectorizing data...")
        X = self.vectorizer.fit_transform(X)

        # Split data
        X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)

        # Train model
        print("Training Logistic Regression model...")
        self.model.fit(X_train, Y_train)

        # Evaluation
        X_train_prediction = self.model.predict(X_train)
        training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
        print(f'Accuracy score on the training data: {training_data_accuracy:.4f}')

        X_test_prediction = self.model.predict(X_test)
        test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
        print(f'Accuracy score on the test data: {test_data_accuracy:.4f}')

        # Confusion Matrix
        print("\nConfusion Matrix:")
        cm = confusion_matrix(Y_test, X_test_prediction)
        print(cm)

        # Save model and vectorizer
        print("Saving model and vectorizer...")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        joblib.dump(self.model, os.path.join(current_dir, 'model.pkl'))
        joblib.dump(self.vectorizer, os.path.join(current_dir, 'vectorizer.pkl'))
        print("Training complete! Files saved: model.pkl, vectorizer.pkl")

# Handle paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    dataset_path = os.path.join(BASE_DIR, 'dataset', 'news.csv')
    trainer = NewsPredictorTrainer(dataset_path)
    trainer.train()
