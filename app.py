from flask import Flask, request, render_template
import numpy as np
import pickle

app = Flask(__name__)

# Load the pre-trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define symptoms and corresponding indices in your feature space
symptom_index = {
    'back_pain': 0, 'constipation': 1, 'abdominal_pain': 2, 'diarrhoea': 3, 'mild_fever': 4,
    'yellow_urine': 5, 'yellowing_of_eyes': 6, 'acute_liver_failure': 7, 'fluid_overload': 8,
    'swelling_of_stomach': 9, 'swelled_lymph_nodes': 10, 'malaise': 11, 'blurred_and_distorted_vision': 12,
    'phlegm': 13, 'throat_irritation': 14, 'redness_of_eyes': 15, 'sinus_pressure': 16, 'runny_nose': 17,
    'congestion': 18, 'chest_pain': 19, 'weakness_in_limbs': 20, 'fast_heart_rate': 21, 'pain_during_bowel_movements': 22,
    'pain_in_anal_region': 23, 'bloody_stool': 24, 'irritation_in_anus': 25, 'neck_pain': 26, 'dizziness': 27,
    'cramps': 28, 'bruising': 29, 'obesity': 30, 'swollen_legs': 31, 'swollen_blood_vessels': 32,
    'puffy_face_and_eyes': 33, 'enlarged_thyroid': 34, 'brittle_nails': 35, 'swollen_extremities': 36,
    'excessive_hunger': 37, 'extra_marital_contacts': 38, 'drying_and_tingling_lips': 39, 'slurred_speech': 40,
    'knee_pain': 41, 'hip_joint_pain': 42, 'muscle_weakness': 43, 'stiff_neck': 44, 'swelling_joints': 45,
    'movement_stiffness': 46, 'spinning_movements': 47, 'loss_of_balance': 48, 'unsteadiness': 49,
    'weakness_of_one_body_side': 50, 'loss_of_smell': 51, 'bladder_discomfort': 52, 'foul_smell_of_urine': 53,
    'continuous_feel_of_urine': 54, 'passage_of_gases': 55, 'internal_itching': 56, 'toxic_look_(typhos)': 57,
    'depression': 58, 'irritability': 59, 'muscle_pain': 60, 'altered_sensorium': 61, 'red_spots_over_body': 62,
    'belly_pain': 63, 'abnormal_menstruation': 64, 'dischromic_patches': 65, 'watering_from_eyes': 66,
    'increased_appetite': 67, 'polyuria': 68, 'family_history': 69, 'mucoid_sputum': 70, 'rusty_sputum': 71,
    'lack_of_concentration': 72, 'visual_disturbances': 73, 'receiving_blood_transfusion': 74,
    'receiving_unsterile_injections': 75, 'coma': 76, 'stomach_bleeding': 77, 'distention_of_abdomen': 78,
    'history_of_alcohol_consumption': 79, 'fluid_overload': 80, 'blood_in_sputum': 81, 'prominent_veins_on_calf': 82,
    'palpitations': 83, 'painful_walking': 84, 'pus_filled_pimples': 85, 'blackheads': 86, 'scurring': 87,
    'skin_peeling': 88, 'silver_like_dusting': 89, 'small_dents_in_nails': 90, 'inflammatory_nails': 91,
    'blister': 92, 'red_sore_around_nose': 93, 'yellow_crust_ooze': 94
}

# Route for rendering the symptoms selection form
@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

# Route for handling the form submission and predicting the disease
@app.route('/healthpredict', methods=['POST'])
def predict():
    # Retrieve the symptoms selected by the user
    symptom1 = request.form.get('select1')
    symptom2 = request.form.get('select2')
    symptom3 = request.form.get('select3')
    symptom4 = request.form.get('select4')

    # Create a feature vector initialized to zero (assuming 95 features)
    input_data = np.zeros(len(symptom_index))

    # Set the corresponding indices to 1 if the symptom is selected
    if symptom1 in symptom_index:
        input_data[symptom_index[symptom1]] = 1
    if symptom2 in symptom_index:
        input_data[symptom_index[symptom2]] = 1
    if symptom3 in symptom_index:
        input_data[symptom_index[symptom3]] = 1
    if symptom4 in symptom_index:
        input_data[symptom_index[symptom4]] = 1

    # Debug: Print the input data shape
    print(f"Input data shape: {input_data.shape}")

    # Debug: Print the input data for verification
    print(f"Input data: {input_data}")

    # Ensure the input data has the correct shape (1, 95) before predicting
    input_data = input_data.reshape(1, -1)
    print(f"Reshaped input data: {input_data.shape}")

    # Predict the disease using the trained model
    try:
        prediction = model.predict(input_data)[0]
    except ValueError as e:
        print(f"Error during prediction: {e}")
        prediction = "Error in prediction, please check input."

    # Render the result in the healthpredict.html template
    return render_template('symptoms.html', result=prediction)

if __name__ == '__main__':
    app.run(debug=True)
