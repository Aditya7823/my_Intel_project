from flask import Flask, render_template, request
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load your pre-trained models
model = joblib.load('models/disease_classifier.pkl')
model1 = joblib.load('models/disease_classifier_random.pkl')
model2 = joblib.load('models/disease_classifier_bayes.pkl')

@app.route('/')
def home():
    return render_template('unati2.html')

@app.route('/health')
def index():
    return render_template('health.html')
@app.route('/symptoms')
def show_symptoms():
    symptoms_list = [
        'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
        'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
        'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
        'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
        'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
        'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
        'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
        'swollen_extremities', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
        'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
        'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
        'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of_urine',
        'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
        'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
        'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
        'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
        'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
        'distention_of_abdomen', 'history_of_alcohol_consumption', 'blood_in_sputum', 'prominent_veins_on_calf',
        'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
        'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
        'yellow_crust_ooze'
    ]

    # HTML template as a string
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Symptoms List</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>Symptoms</h1>
            <ul class="list-group">
                {% for symptom in symptoms %}
                    <li class="list-group-item">{{ symptom }}</li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(template, symptoms=symptoms_list)

@app.route('/healthpredict', methods=['GET', 'POST'])
def symptoms():
    if request.method == 'POST':
        # Retrieve selected symptoms from the form
        select1 = request.form.get('select1')
        select2 = request.form.get('select2')
        select3 = request.form.get('select3')
        select4 = request.form.get('select4')
        
        # List of all possible symptoms
        symptoms_list = [
            'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
            'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
            'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
            'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
            'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
            'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
            'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
            'swollen_extremities', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
            'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
            'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
            'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of_urine',
            'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
            'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
            'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
            'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
            'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
            'distention_of_abdomen', 'history_of_alcohol_consumption', 'blood_in_sputum', 'prominent_veins_on_calf',
            'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
            'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
            'yellow_crust_ooze'
        ]
        
        # List of diseases
        diseases = [
            'Fungal_infection', 'Allergy', 'GERD', 'Chronic_cholestasis', 'Drug_Reaction', 'Peptic_ulcer_diseae',
            'AIDS', 'Diabetes', 'Gastroenteritis', 'Bronchial_Asthma', 'Hypertension', 'Migraine',
            'Cervical_spondylosis', 'Paralysis_brain_hemorrhage', 'Jaundice', 'Malaria', 'Chicken_pox', 'Dengue',
            'Typhoid', 'hepatitis_A', 'Hepatitis_B', 'Hepatitis_C', 'Hepatitis_D', 'Hepatitis_E',
            'Alcoholic_hepatitis', 'Tuberculosis', 'Common_Cold', 'Pneumonia', 'Dimorphic_hemmorhoids',
            'Heart_attack', 'Varicose_veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
            'Osteoarthristis', 'Arthritis', 'Varicose_veins', 'Acne', 'Urinary_tract_infection', 'Psoriasis',
            'Impetigo', 'Paroymsal_Positional_Vertigo'
        ]
        
        # Create input for the model
        symptom_vector = [0] * len(symptoms_list)
        selected_symptoms = [select1, select2, select3, select4]
        
        for symptom in selected_symptoms:
            if symptom in symptoms_list:
                index = symptoms_list.index(symptom)
                symptom_vector[index] = 1
        
        input_data = [symptom_vector]
        
        # Predict using each model
        predicted_diseases = set()
        
        predictions = [
            model.predict(input_data),
            model1.predict(input_data),
            model2.predict(input_data)
        ]
        
        for prediction in predictions:
            disease_index = prediction[0]
            predicted_diseases.add(diseases[disease_index])
        
        result = ', '.join(predicted_diseases)
        
        return render_template('healthpredict.html', result=result)
    
    return render_template('healthpredict.html')

if __name__ == '__main__':
    app.run(debug=True)
