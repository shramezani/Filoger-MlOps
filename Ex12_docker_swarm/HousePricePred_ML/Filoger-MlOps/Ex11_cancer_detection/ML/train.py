import joblib
import pandas as pd
import numpy as np

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, roc_auc_score

# TODO :  move it to the env file
MODEL_PATH = 'ml/cancer_model.pkl'

# Load dataset
data = load_breast_cancer()
#TODO : move selected_features to .env
selected_features = ['worst area', 'worst concave points', 'mean concave points', 'worst radius', 'mean concavity'] 
X = np.array(pd.DataFrame(data.data, columns=data.feature_names)[selected_features])
# Labels (0 = malignant, 1 = benign)
y = data.target

#Train and Save the Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
joblib.dump(model, MODEL_PATH)

# Evaluate
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1] 
auc_score = roc_auc_score(y_test, y_pred_proba)

print(f'AUC-ROC Score: {auc_score:.2f}')
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred))
