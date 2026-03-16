from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np

class PerformanceClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        predictions = []
        for marks in X:
            if marks < 50:
                predictions.append('Weak student')
            elif 50 <= marks <= 75:
                predictions.append('Average student')
            else:
                predictions.append('Top student')
        return np.array(predictions)

def classify_student_performance(marks):
    classifier = PerformanceClassifier()
    return classifier.predict(marks)