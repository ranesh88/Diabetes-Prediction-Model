from flask import Flask, request, render_template
import pickle
import numpy as np



app = Flask(__name__)

# Load model
model = pickle.load(open('rf_classifier.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))


def predict(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age):
    # Prepare features array
    features = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

    # scaling
    scaled_features = scaler.transform(features)

    # predict by model
    result = model.predict(scaled_features)

    return result[0]

# Routes
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_route():
    if request.method == 'POST':
        Pregnancies = request.form['Pregnancies']
        Glucose = (request.form['Glucose'])
        BloodPressure = request.form['BloodPressure']
        SkinThickness = (request.form['SkinThickness'])
        Insulin = request.form['Insulin']
        BMI = request.form['BMI']
        DiabetesPedigreeFunction = request.form['DiabetesPedigreeFunction']
        Age = request.form['Age']

        prediction = predict(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age)
        prediction_text = "The Patient has Diabetes" if prediction == 1 else "The Patient has no Diabetes"

        return render_template('index.html', prediction=prediction_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)