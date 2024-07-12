from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'Key_secret1839@#*'
CORS(app)

# Set up MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['flask_login_system']
users_collection = db['users']

# Load your pre-trained models
model = joblib.load('disease_classifier.pkl')
model1 = joblib.load('disease_classifier_random.pkl')
model2 = joblib.load('disease_classifier_bayes.pkl')

@app.route('/')
def home():
    return render_template('unati2.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/hospital_info1', methods=['GET'])
def hospital_info1():
    hospital_name = request.args.get('hospital_name')
    # Your logic to handle hospital_name goes here
    return render_template('appoint.html', hospital_name=hospital_name)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/healthinfo/')
def healthinfo():
    if 'username' in session:
        return render_template('mainhealthModule.html')
    else:
        flash('You are not logged in. Please log in to access the services.')
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))
        
        if users_collection.find_one({'username': username}):
            flash('Username already exists!')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        users_collection.insert_one({'username': username, 'password': hashed_password, 'email': email})
        
        session['username'] = username
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/health')
def index():
    return render_template('health.html')


@app.route('/healthpredict')
def healthprediction():
    return render_template('healthpredict.html')

# @app.route('/healthpredict')
# def show_symptoms():
#     symptoms_list = [
#         'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
#         'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
#         'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
#         'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
#         'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
#         'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
#         'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
#         'swollen_extremities', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
#         'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
#         'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
#         'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of_urine',
#         'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
#         'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
#         'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
#         'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
#         'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
#         'distention_of_abdomen', 'history_of_alcohol_consumption', 'blood_in_sputum', 'prominent_veins_on_calf',
#         'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
#         'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
#         'yellow_crust_ooze'
#     ]

#     template = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Symptoms List</title>
#         <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
#     </head>
#     <body>
#         <div class="container mt-5">
#             <h1>Symptoms</h1>
#             <ul class="list-group">
#                 {% for symptom in symptoms %}
#                     <li class="list-group-item">{{ symptom }}</li>
#                 {% endfor %}
#             </ul>
#         </div>
#     </body>
#     </html>
#     """
    
#     return render_template_string(template, symptoms=symptoms_list)

@app.route('/symptomes', methods=['POST'])
def symptomes():
 if request.method == 'POST':
    select1 = request.form['select1']
    select2 = request.form['select2']
    select3 = request.form['select3']
    select4 = request.form['select4']
    print(select1,select2,select3,select4)
    l1=['back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
    'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
    'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
    'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
    'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
    'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
    'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
    'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
    'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
    'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
    'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
    'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
    'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
    'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
    'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
    'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
    'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
    'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
    'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
    'yellow_crust_ooze']

    disease=['Fungal_infection', 'Allergy', 'GERD', 'Chronic_cholestasis',
       'Drug_Reaction', 'Peptic_ulcer_diseae', 'AIDS', 'Diabetes ',
       'Gastroenteritis', 'Bronchial_Asthma', 'Hypertension ', 'Migraine',
       'Cervical_spondylosis', 'Paralysis_brain_hemorrhage', 'Jaundice',
       'Malaria', 'Chicken_pox', 'Dengue', 'Typhoid', 'hepatitis_A',
       'Hepatitis_B', 'Hepatitis_C', 'Hepatitis_D', 'Hepatitis_E',
       'Alcoholic_hepatitis', 'Tuberculosis', 'Common_Cold', 'Pneumonia',
       'Dimorphic_hemmorhoids', 'Heart_attack', 'Varicose_veins',
       'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
       'Osteoarthristis', 'Arthritis',
       'Varicose_veins', 'Acne',
       'Urinary_tract_infection', 'Psoriasis', 'Impetigo','Paroymsal_Positional_Vertigo']
    
    l2=[]
    for i in range(0,len(l1)):
        l2.append(0)
    print(l2)
    
    psymptoms=[select1,select2,select3,select4]
    for k in range(0,len(l1)):
     for z in psymptoms:
        if(z==l1[k]):
            l2[k]=1

    inputtest = [l2]
    print(inputtest)
    predicted_disease=[]
    predict1=model.predict(inputtest)
    predicted1=predict1[0]
    h='no'
    for a in range(0,len(disease)):
        if(predicted1 == a):
            h='yes'
            break

    predicted_disease.append(disease[a])
    if (h=='yes'):
        print("Predicted disease:", disease[a])
    else:
        print("not found")

    predict2=model1.predict(inputtest)
    predicted2=predict2[0]
    h='no'
    for a in range(0,len(disease)):
        if(predicted2 == a):
            h='yes'
            break
    predicted_disease.append(disease[a])
    if (h=='yes'):
        print("Predicted disease:", disease[a])
    else:
        print("not found")  


    predict3=model2.predict(inputtest)
    predicted3=predict3[0]
    h='no'
    for a in range(0,len(disease)):
        if(predicted3 == a):
            h='yes'
            break
    predicted_disease.append(disease[a])
    if (h=='yes'):
        print("Predicted disease:", disease[a])
    else:
        print("not found")
    predicted_disease=list(set(predicted_disease)) 
    print(predicted_disease) 
    predicted_disease[0]

 disease_info = {
    "Drug_Reaction": {
        "Precautions": ["Stop irritation", "Consult nearest hospital", "Stop taking drug", "Follow up"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Drug reactions can vary widely from mild irritations to severe adverse effects. "
                       "Common reactions include irritation at the site of application or ingestion. "
                       "If you experience any adverse effects, such as swelling or difficulty breathing, "
                       "seek immediate medical attention. Discontinue the drug and consult the nearest "
                       "hospital for further evaluation and management. Follow up with your healthcare "
                       "provider to monitor your recovery and adjust your treatment plan as needed."
    },
    "Malaria": {
        "Precautions": ["Consult nearest hospital", "Avoid oily food", "Avoid non-vegetarian food", "Keep mosquitoes out"],
        "Prevalence": "Rare - Fewer than 1 million cases per year (India)",
        "Description": "Malaria is a tropical disease spread by mosquitoes infected with Plasmodium parasites. "
                       "Symptoms include fever, chills, and flu-like illness. If diagnosed with malaria, seek "
                       "medical attention promptly. Treatment typically involves antimalarial medications. "
                       "Avoid oily and non-vegetarian foods during recovery as they may aggravate symptoms. "
                       "Prevent mosquito bites by using nets and repellents, especially in endemic areas."
    },
    "Allergy": {
        "Precautions": ["Apply calamine lotion", "Cover affected area with a bandage", "Use ice to compress itching"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Allergies are hypersensitive reactions to substances like pollen, pet dander, or certain foods. "
                       "Symptoms can range from mild itching and sneezing to severe anaphylaxis. Treat mild "
                       "symptoms with calamine lotion or ice packs. Cover affected areas to prevent further irritation. "
                       "For severe reactions, seek immediate medical help. Allergies are very common and affect "
                       "millions annually in India. Identifying and avoiding triggers is crucial for management."
    },
    "Hypothyroidism": {
        "Precautions": ["Reduce stress", "Exercise regularly", "Eat a healthy diet", "Get proper sleep"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Hypothyroidism occurs when the thyroid gland doesn't produce enough hormones. Symptoms include "
                       "fatigue, weight gain, and sensitivity to cold. Manage hypothyroidism with stress reduction "
                       "techniques, regular exercise, and a balanced diet. Ensure adequate sleep for hormone regulation. "
                       "Consult a doctor for medication, which may include thyroid hormone replacement therapy. This "
                       "condition is prevalent, affecting over 10 million people annually in India."
    },
    "Psoriasis": {
        "Precautions": ["Wash hands with warm soapy water", "Stop bleeding using pressure", "Consult doctor", "Take salt baths"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Psoriasis is a chronic skin condition characterized by red, itchy, and scaly patches. "
                       "Treatment involves washing affected areas with warm, soapy water and using salt baths for relief. "
                       "Consult a dermatologist for prescribed treatments and ongoing management. Psoriasis is common "
                       "in India, impacting more than 10 million individuals annually."
    },
    "GERD": {
        "Precautions": ["Avoid fatty and spicy food", "Avoid lying down after eating", "Maintain a healthy weight", "Exercise regularly"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "GERD (Gastroesophageal Reflux Disease) causes frequent acid reflux, leading to heartburn, chest pain, "
                       "and regurgitation. Manage symptoms by avoiding fatty and spicy foods, especially before lying down. "
                       "Maintain a healthy weight through diet and exercise. If symptoms persist, consult a healthcare provider "
                       "for medications and lifestyle modifications. GERD is highly prevalent, affecting millions annually in India."
    },
    "Chronic_cholestasis": {
        "Precautions": ["Take cold baths", "Use anti-itch medicine", "Consult doctor", "Eat a healthy diet"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Chronic cholestasis is a condition where bile flow from the liver slows or stops. Symptoms include itching "
                       "and jaundice. Treat symptoms with cold baths and anti-itch medications. Follow a healthy diet to manage "
                       "liver function and consult a doctor for ongoing care. This condition affects over a million people annually "
                       "in India."
    },
    "Hepatitis_A": {
        "Precautions": ["Consult nearest hospital", "Wash hands thoroughly", "Avoid fatty and spicy food", "Take prescribed medication"],
        "Prevalence": "Rare - Fewer than 1 million cases per year (India)",
        "Description": "Hepatitis A is a liver infection caused by the hepatitis A virus (HAV). Symptoms include jaundice, fatigue, "
                       "and abdominal pain. Seek medical attention for diagnosis and management. Prevent transmission by washing hands "
                       "thoroughly and avoiding fatty or spicy foods. Vaccination is available for prevention. Hepatitis A is relatively "
                       "rare in India, with fewer than a million cases annually."
    },
    "Osteoarthristis": {
        "Precautions": ["Take acetaminophen for pain relief", "Consult nearest hospital for severe cases", "Follow up with doctor", "Take salt baths"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Osteoarthritis is a degenerative joint disease characterized by pain, swelling, and stiffness. Treat symptoms "
                       "with acetaminophen for pain relief and salt baths for relief. Consult a healthcare provider for proper diagnosis "
                       "and management. Follow up appointments are essential for monitoring progression. This condition affects a significant "
                       "number of people annually in India."
    },
    "Paroxysmal_Positional_Vertigo": {
        "Precautions": ["Lie down", "Avoid sudden changes in body position", "Avoid abrupt head movements", "Practice relaxation techniques"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Paroxysmal positional vertigo (PPV) is a type of vertigo caused by certain head movements. Symptoms include "
                       "dizziness and nausea. Treat PPV by lying down and avoiding sudden head movements. Relaxation techniques may "
                       "also help alleviate symptoms. This condition is common, affecting over a million people annually in India."
    },
    "Hypoglycemia": {
        "Precautions": ["Lie down on side", "Check pulse rate", "Drink sugary drinks", "Consult doctor"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Hypoglycemia occurs when blood sugar levels drop too low. Symptoms include dizziness, confusion, and "
                       "sweating. Treat hypoglycemia by lying down on your side and consuming sugary drinks or snacks. Check "
                       "blood sugar levels regularly and consult a doctor for proper management. This condition is common, "
                       "affecting millions annually in India."
    },
    "Acne": {
        "Precautions": ["Bathe twice daily", "Avoid fatty and spicy food", "Drink plenty of water", "Avoid excessive use of skincare products"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Acne is a common skin condition characterized by pimples and blemishes. Treat acne by washing affected "
                       "areas twice daily with a mild cleanser. Avoid fatty or spicy foods that may exacerbate acne. Stay hydrated "
                       "and avoid using too many skincare products. Acne is prevalent in India, affecting millions annually."
    },
    "Urinary_tract_infection": {
        "Precautions": ["Drink plenty of water", "Increase vitamin C intake", "Take probiotics", "Consult doctor for antibiotics"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Urinary tract infections (UTIs) are bacterial infections affecting the urinary system. Symptoms include "
                       "painful urination, frequent urges to urinate, and abdominal pain. Prevent UTIs by staying hydrated, "
                       "increasing vitamin C intake, and taking probiotics. Consult a doctor for antibiotics if needed. UTIs are "
                       "common, affecting over a million people annually in India."
    },
    "Impetigo": {
        "Precautions": ["Soak affected area in warm water", "Use antibiotics as prescribed", "Gently remove scabs with wet cloth", "Consult doctor for severe cases"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Impetigo is a highly contagious skin infection characterized by blisters or sores. Treat impetigo by soaking "
                       "the affected area in warm water and gently removing scabs with a wet cloth. Use antibiotics as prescribed by "
                       "a doctor for bacterial infections. Consult a healthcare provider for severe cases. Impetigo is widespread in "
                       "India, affecting millions annually."
    },
    "Psoriasis": {
        "Precautions": ["Wash hands with warm soapy water", "Stop bleeding using pressure", "Consult doctor", "Take salt baths"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Psoriasis is a chronic skin condition characterized by red, itchy, and scaly patches. "
                       "Treatment involves washing affected areas with warm, soapy water and using salt baths for relief. "
                       "Consult a dermatologist for prescribed treatments and ongoing management. Psoriasis is common "
                       "in India, impacting more than 10 million individuals annually."
    },
    "GERD": {
        "Precautions": ["Avoid fatty and spicy food", "Avoid lying down after eating", "Maintain a healthy weight", "Exercise regularly"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "GERD (Gastroesophageal Reflux Disease) causes frequent acid reflux, leading to heartburn, chest pain, "
                       "and regurgitation. Manage symptoms by avoiding fatty and spicy foods, especially before lying down. "
                       "Maintain a healthy weight through diet and exercise. If symptoms persist, consult a healthcare provider "
                       "for medications and lifestyle modifications. GERD is highly prevalent, affecting millions annually in India."
    },
    "Chronic_cholestasis": {
        "Precautions": ["Take cold baths", "Use anti-itch medicine", "Consult doctor", "Eat a healthy diet"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Chronic cholestasis is a condition where bile flow from the liver slows or stops. Symptoms include itching "
                       "and jaundice. Treat symptoms with cold baths and anti-itch medications. Follow a healthy diet to manage "
                       "liver function and consult a doctor for ongoing care. This condition affects over a million people annually "
                       "in India."
    },
    "Hepatitis_A": {
        "Precautions": ["Consult nearest hospital", "Wash hands thoroughly", "Avoid fatty and spicy food", "Take prescribed medication"],
        "Prevalence": "Rare - Fewer than 1 million cases per year (India)",
        "Description": "Hepatitis A is a liver infection caused by the hepatitis A virus (HAV). Symptoms include jaundice, fatigue, "
                       "and abdominal pain. Seek medical attention for diagnosis and management. Prevent transmission by washing hands "
                       "thoroughly and avoiding fatty or spicy foods. Vaccination is available for prevention. Hepatitis A is relatively "
                       "rare in India, with fewer than a million cases annually."
    },
    "Osteoarthristis": {
        "Precautions": ["Take acetaminophen for pain relief", "Consult nearest hospital for severe cases", "Follow up with doctor", "Take salt baths"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Osteoarthritis is a degenerative joint disease characterized by pain, swelling, and stiffness. Treat symptoms "
                       "with acetaminophen for pain relief and salt baths for relief. Consult a healthcare provider for proper diagnosis "
                       "and management. Follow up appointments are essential for monitoring progression. This condition affects a significant "
                       "number of people annually in India."
    },
    "Paroxysmal_Positional_Vertigo": {
        "Precautions": ["Lie down", "Avoid sudden changes in body position", "Avoid abrupt head movements", "Practice relaxation techniques"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Paroxysmal positional vertigo (PPV) is a type of vertigo caused by certain head movements. Symptoms include "
                       "dizziness and nausea. Treat PPV by lying down and avoiding sudden head movements. Relaxation techniques may "
                       "also help alleviate symptoms. This condition is common, affecting over a million people annually in India."
    },
    "Hypoglycemia": {
        "Precautions": ["Lie down on side", "Check pulse rate", "Drink sugary drinks", "Consult doctor"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Hypoglycemia occurs when blood sugar levels drop too low. Symptoms include dizziness, confusion, and "
                       "sweating. Treat hypoglycemia by lying down on your side and consuming sugary drinks or snacks. Check "
                       "blood sugar levels regularly and consult a doctor for proper management. This condition is common, "
                       "affecting millions annually in India."
    },
    "Acne": {
        "Precautions": ["Bathe twice daily", "Avoid fatty and spicy food", "Drink plenty of water", "Avoid excessive use of skincare products"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Acne is a common skin condition characterized by pimples and blemishes. Treat acne by washing affected "
                       "areas twice daily with a mild cleanser. Avoid fatty or spicy foods that may exacerbate acne. Stay hydrated "
                       "and avoid using too many skincare products. Acne is prevalent in India, affecting millions annually."
    },
    "Urinary_tract_infection": {
        "Precautions": ["Drink plenty of water", "Increase vitamin C intake", "Take probiotics", "Consult doctor for antibiotics"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Urinary tract infections (UTIs) are bacterial infections affecting the urinary system. Symptoms include "
                       "painful urination, frequent urges to urinate, and abdominal pain. Prevent UTIs by staying hydrated, "
                       "increasing vitamin C intake, and taking probiotics. Consult a doctor for antibiotics if needed. UTIs are "
                       "common, affecting over a million people annually in India."
    },
    "Psoriasis": {
        "Precautions": ["Wash hands with warm soapy water", "Stop bleeding using pressure", "Consult doctor", "Take salt baths"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Psoriasis is a chronic skin condition characterized by red, itchy, and scaly patches. "
                       "Treatment involves washing affected areas with warm, soapy water and using salt baths for relief. "
                       "Consult a dermatologist for prescribed treatments and ongoing management. Psoriasis is common "
                       "in India, impacting more than 10 million individuals annually."
    },
    "GERD": {
        "Precautions": ["Avoid fatty and spicy food", "Avoid lying down after eating", "Maintain a healthy weight", "Exercise regularly"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "GERD (Gastroesophageal Reflux Disease) causes frequent acid reflux, leading to heartburn, chest pain, "
                       "and regurgitation. Manage symptoms by avoiding fatty and spicy foods, especially before lying down. "
                       "Maintain a healthy weight through diet and exercise. If symptoms persist, consult a healthcare provider "
                       "for medications and lifestyle modifications. GERD is highly prevalent, affecting millions annually in India."
    },
    "Chronic_cholestasis": {
        "Precautions": ["Take cold baths", "Use anti-itch medicine", "Consult doctor", "Eat a healthy diet"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Chronic cholestasis is a condition where bile flow from the liver slows or stops. Symptoms include itching "
                       "and jaundice. Treat symptoms with cold baths and anti-itch medications. Follow a healthy diet to manage "
                       "liver function and consult a doctor for ongoing care. This condition affects over a million people annually "
                       "in India."
    },
    "Hepatitis_A": {
        "Precautions": ["Consult nearest hospital", "Wash hands thoroughly", "Avoid fatty and spicy food", "Take prescribed medication"],
        "Prevalence": "Rare - Fewer than 1 million cases per year (India)",
        "Description": "Hepatitis A is a liver infection caused by the hepatitis A virus (HAV). Symptoms include jaundice, fatigue, "
                       "and abdominal pain. Seek medical attention for diagnosis and management. Prevent transmission by washing hands "
                       "thoroughly and avoiding fatty or spicy foods. Vaccination is available for prevention. Hepatitis A is relatively "
                       "rare in India, with fewer than a million cases annually."
    },
    "Osteoarthristis": {
        "Precautions": ["Take acetaminophen for pain relief", "Consult nearest hospital for severe cases", "Follow up with doctor", "Take salt baths"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Osteoarthritis is a degenerative joint disease characterized by pain, swelling, and stiffness. Treat symptoms "
                       "with acetaminophen for pain relief and salt baths for relief. Consult a healthcare provider for proper diagnosis "
                       "and management. Follow up appointments are essential for monitoring progression. This condition affects a significant "
                       "number of people annually in India."
    },
    "Paroxysmal_Positional_Vertigo": {
        "Precautions": ["Lie down", "Avoid sudden changes in body position", "Avoid abrupt head movements", "Practice relaxation techniques"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Paroxysmal positional vertigo (PPV) is a type of vertigo caused by certain head movements. Symptoms include "
                       "dizziness and nausea. Treat PPV by lying down and avoiding sudden head movements. Relaxation techniques may "
                       "also help alleviate symptoms. This condition is common, affecting over a million people annually in India."
    },
    "Hypoglycemia": {
        "Precautions": ["Lie down on side", "Check pulse rate", "Drink sugary drinks", "Consult doctor"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Hypoglycemia occurs when blood sugar levels drop too low. Symptoms include dizziness, confusion, and "
                       "sweating. Treat hypoglycemia by lying down on your side and consuming sugary drinks or snacks. Check "
                       "blood sugar levels regularly and consult a doctor for proper management. This condition is common, "
                       "affecting millions annually in India."
    },
    "Acne": {
        "Precautions": ["Bathe twice daily", "Avoid fatty and spicy food", "Drink plenty of water", "Avoid excessive use of skincare products"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Acne is a common skin condition characterized by pimples and blemishes. Treat acne by washing affected "
                       "areas twice daily with a mild cleanser. Avoid fatty or spicy foods that may exacerbate acne. Stay hydrated "
                       "and avoid using too many skincare products. Acne is prevalent in India, affecting millions annually."
    },
    "Urinary_tract_infection": {
        "Precautions": ["Drink plenty of water", "Increase vitamin C intake", "Take probiotics", "Consult doctor for antibiotics"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Urinary tract infections (UTIs) are bacterial infections affecting the urinary system. Symptoms include "
                       "painful urination, frequent urges to urinate, and abdominal pain. Prevent UTIs by staying hydrated, "
                       "increasing vitamin C intake, and taking probiotics. Consult a doctor for antibiotics if needed. UTIs are "
                       "common, affecting over a million people annually in India."
    },
    "Psoriasis": {
        "Precautions": ["Wash hands with warm soapy water", "Stop bleeding using pressure", "Consult doctor", "Take salt baths"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Psoriasis is a chronic skin condition characterized by red, itchy, and scaly patches. "
                       "Treatment involves washing affected areas with warm, soapy water and using salt baths for relief. "
                       "Consult a dermatologist for prescribed treatments and ongoing management. Psoriasis is common "
                       "in India, impacting more than 10 million individuals annually."
    },
    "GERD": {
        "Precautions": ["Avoid fatty and spicy food", "Avoid lying down after eating", "Maintain a healthy weight", "Exercise regularly"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "GERD (Gastroesophageal Reflux Disease) causes frequent acid reflux, leading to heartburn, chest pain, "
                       "and regurgitation. Manage symptoms by avoiding fatty and spicy foods, especially before lying down. "
                       "Maintain a healthy weight through diet and exercise. If symptoms persist, consult a healthcare provider "
                       "for medications and lifestyle modifications. GERD is highly prevalent, affecting millions annually in India."
    },
    "Chronic_cholestasis": {
        "Precautions": ["Take cold baths", "Use anti-itch medicine", "Consult doctor", "Eat a healthy diet"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Chronic cholestasis is a condition where bile flow from the liver slows or stops. Symptoms include itching "
                       "and jaundice. Treat symptoms with cold baths and anti-itch medications. Follow a healthy diet to manage "
                       "liver function and consult a doctor for ongoing care. This condition affects over a million people annually "
                       "in India."
    },
    "Hepatitis_A": {
        "Precautions": ["Consult nearest hospital", "Wash hands thoroughly", "Avoid fatty and spicy food", "Take prescribed medication"],
        "Prevalence": "Rare - Fewer than 1 million cases per year (India)",
        "Description": "Hepatitis A is a liver infection caused by the hepatitis A virus (HAV). Symptoms include jaundice, fatigue, "
                       "and abdominal pain. Seek medical attention for diagnosis and management. Prevent transmission by washing hands "
                       "thoroughly and avoiding fatty or spicy foods. Vaccination is available for prevention. Hepatitis A is relatively "
                       "rare in India, with fewer than a million cases annually."
    },
    "Osteoarthristis": {
        "Precautions": ["Take acetaminophen for pain relief", "Consult nearest hospital for severe cases", "Follow up with doctor", "Take salt baths"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Osteoarthritis is a degenerative joint disease characterized by pain, swelling, and stiffness. Treat symptoms "
                       "with acetaminophen for pain relief and salt baths for relief. Consult a healthcare provider for proper diagnosis "
                       "and management. Follow up appointments are essential for monitoring progression. This condition affects a significant "
                       "number of people annually in India."
    },
    "Paroxysmal_Positional_Vertigo": {
        "Precautions": ["Lie down", "Avoid sudden changes in body position", "Avoid abrupt head movements", "Practice relaxation techniques"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Paroxysmal positional vertigo (PPV) is a type of vertigo caused by certain head movements. Symptoms include "
                       "dizziness and nausea. Treat PPV by lying down and avoiding sudden head movements. Relaxation techniques may "
                       "also help alleviate symptoms. This condition is common, affecting over a million people annually in India."
    },
    "Hypoglycemia": {
        "Precautions": ["Lie down on side", "Check pulse rate", "Drink sugary drinks", "Consult doctor"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Hypoglycemia occurs when blood sugar levels drop too low. Symptoms include dizziness, confusion, and "
                       "sweating. Treat hypoglycemia by lying down on your side and consuming sugary drinks or snacks. Check "
                       "blood sugar levels regularly and consult a doctor for proper management. This condition is common, "
                       "affecting millions annually in India."
    },
    "Acne": {
        "Precautions": ["Bathe twice daily", "Avoid fatty and spicy food", "Drink plenty of water", "Avoid excessive use of skincare products"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Acne is a common skin condition characterized by pimples and blemishes. Treat acne by washing affected "
                       "areas twice daily with a mild cleanser. Avoid fatty or spicy foods that may exacerbate acne. Stay hydrated "
                       "and avoid using too many skincare products. Acne is prevalent in India, affecting millions annually."
    },
    "Urinary_tract_infection": {
        "Precautions": ["Drink plenty of water", "Increase vitamin C intake", "Take probiotics", "Consult doctor for antibiotics"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Urinary tract infections (UTIs) are bacterial infections affecting the urinary system. Symptoms include "
                       "painful urination, frequent urges to urinate, and abdominal pain. Prevent UTIs by staying hydrated, "
                       "increasing vitamin C intake, and taking probiotics. Consult a doctor for antibiotics if needed. UTIs are "
                       "common, affecting over a million people annually in India."
    },
    "AIDS": {
        "Precautions": ["Avoid open cuts", "Do not share needles", "consult doctor", "wear gloves"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "AIDS (Acquired Immunodeficiency Syndrome) is a chronic condition caused by HIV (Human Immunodeficiency Virus). "
                       "Prevent transmission by avoiding open cuts, not sharing needles, and wearing gloves when handling bodily fluids. "
                       "Consult a doctor for antiretroviral therapy and regular check-ups. AIDS affects over a million people annually in India."
    },
    "Diabetes": {
        "Precautions": ["Exercise regularly", "Follow diet plan", "consult doctor", "regular follow up"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Diabetes is a chronic condition characterized by high blood sugar levels. Manage diabetes through regular exercise, "
                       "a balanced diet, and medication as prescribed by a healthcare provider. Follow up with regular check-ups to monitor "
                       "blood sugar levels and overall health. Diabetes is highly prevalent, affecting more than 10 million individuals annually "
                       "in India."
    },
    "Gastroenteritis": {
        "Precautions": ["Consult nearest hospital", "Drink safe water", "consult doctor", "eat light food"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Gastroenteritis is an inflammation of the stomach and intestines, causing diarrhea, vomiting, and abdominal pain. "
                       "Seek medical attention for severe cases at the nearest hospital. Prevent dehydration by drinking safe water and "
                       "eating light, easy-to-digest foods. Consult a doctor for proper diagnosis and management. Gastroenteritis is very "
                       "common, affecting more than 10 million people annually in India."
    },
    "Bronchial_Asthma": {
        "Precautions": ["Avoid smoke", "use mask", "Consult doctor", "exercise"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Bronchial asthma is a chronic condition characterized by inflammation and narrowing of the airways, causing "
                       "wheezing, shortness of breath, and coughing. Avoid smoke and wear masks to prevent triggers. Consult a doctor "
                       "for prescribed medications and follow an exercise regimen to manage symptoms. Bronchial asthma is highly prevalent, "
                       "affecting more than 10 million individuals annually in India."
    },
    "Hypertension ": {
        "Precautions": ["consult doctor", "exercise", "regular follow up", "diet"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Hypertension, or high blood pressure, is a chronic condition that can lead to cardiovascular complications. "
                       "Manage hypertension through regular consultation with a doctor, exercise, and following a balanced diet. "
                       "Monitor blood pressure levels with regular follow-ups to prevent complications. Hypertension is highly prevalent, "
                       "affecting more than 10 million individuals annually in India."
    },
    "Migraine": {
        "Precautions": ["Lie down in a quiet, dark room", "apply ice to head", "consult doctor", "take medication"],
        "Prevalence": "Very common - More than 10 million cases per year (India)",
        "Description": "Migraine is a neurological condition characterized by severe headaches, often accompanied by nausea, "
                       "vomiting, and sensitivity to light and sound. Manage migraines by lying down in a quiet, dark room and applying "
                       "ice packs to the head. Consult a doctor for prescribed medications and follow-up care. Migraines are highly prevalent, "
                       "affecting more than 10 million individuals annually in India."
    },
    "Cervical_spondylosis": {
        "Precautions": ["Consult nearest hospital", "apply heat pack", "consult doctor", "regular follow up"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Cervical spondylosis is a degenerative condition of the cervical spine, causing neck pain and stiffness. "
                       "Apply heat packs to the affected area and consult the nearest hospital for severe cases. Regularly consult "
                       "a doctor for prescribed treatments and follow-up care. Cervical spondylosis is common, affecting over a million "
                       "people annually in India."
    },
    "Hyperthyroidism": {
        "Precautions": ["Consult nearest hospital", "drink water", "consult doctor", "regular follow up"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Hyperthyroidism is a condition where the thyroid gland produces too much thyroid hormone. Symptoms include "
                       "weight loss, rapid heartbeat, and irritability. Seek medical attention at the nearest hospital and stay hydrated "
                       "to manage symptoms. Consult a doctor for prescribed medications and regular follow-up care. Hyperthyroidism is "
                       "common, affecting over a million people annually in India."
    },
    "Hypothyroidism": {
        "Precautions": ["Consult nearest hospital", "drink water", "consult doctor", "regular follow up"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Hypothyroidism is a condition where the thyroid gland does not produce enough thyroid hormone. Symptoms include "
                       "fatigue, weight gain, and sensitivity to cold. Seek medical attention at the nearest hospital and stay hydrated "
                       "to manage symptoms. Consult a doctor for prescribed medications and regular follow-up care. Hypothyroidism is "
                       "common, affecting over a million people annually in India."
    },
    "Hepatitis_B": {
        "Precautions": ["Consult nearest hospital", "consult doctor", "vaccinate", "regular follow up"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Hepatitis B is a liver infection caused by the hepatitis B virus (HBV). Symptoms include jaundice, fatigue, "
                       "and abdominal pain. Seek medical attention at the nearest hospital for diagnosis and management. Vaccination "
                       "is available for prevention. Consult a doctor for regular follow-up care. Hepatitis B is common, affecting "
                       "over a million people annually in India."
    },
    "Fungal_infection": {
        "Precautions": ["Consult nearest hospital", "keep infected area dry", "consult doctor", "regular follow up"],
        "Prevalence": "Common - More than 1 million cases per year (India)",
        "Description": "Fungal infections are caused by fungi and can affect the skin, nails, and other areas. Keep infected areas "
                       "dry and consult the nearest hospital for severe cases. Consult a doctor for prescribed antifungal medications "
                       "and follow-up care. Fungal infections are common, affecting over a million people annually in India."
    }
 }




 for disease_name in predicted_disease:
    precautions = disease_info[disease_name]["Precautions"]
    occurrences = disease_info[disease_name]["Prevalence"]
    information = disease_info[disease_name]["Description"]    
    
    return render_template('healthpredict.html', predicted_disease=predicted_disease, precautions=precautions, occurrences=occurrences,information= information )


if __name__ == '__main__':
    app.run(debug=True)
