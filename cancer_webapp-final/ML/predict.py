import joblib
import numpy as np

# TODO use MODEL_PATH
model = joblib.load('ml/cancer_model.pkl')


def predict_cancer(input_data):
    # TODO move it to env
    label_map ={0: 'malignant', 1: 'benign'}
    input_data = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_data)
    return label_map[int(prediction[0])]

## Example input:
# worst area=2019.0, 
# worst concave points= 0.2654, 
# mean concave points=0.14710,	
# worst radius=25.380, 
# mean concavity=0.30010
#print(predict_cancer([2019.0,0.2654,0.14710,25.380,0.30010]))