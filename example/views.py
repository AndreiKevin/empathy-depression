from datetime import datetime
import json
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

from joblib import load
from collections import Counter

import pandas as pd
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb


# Load the model from the file
current_dir = os.path.dirname(os.path.abspath(__file__))
model_1 = load(os.path.join(current_dir, "models", "model_1.joblib"))  # BernoulliNB
model_2 = load(
    os.path.join(current_dir, "models", "model_2.joblib")
)  # RandomForestClassifier
model_3 = load(
    os.path.join(current_dir, "models", "model_3.joblib")
)  # xgb.XGBClassifier


def index(request):
    now = datetime.now()
    html = f"""
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    """
    return HttpResponse(html)


def get_user_input(request):
    if request.method == "POST":
        # Assuming there's a form with a 'bmi' field
        bmi = request.POST.get("bmi")
        # You can add more fields as necessary

        # Redirect to a new URL to process the input and display the result
        return HttpResponseRedirect("/result/?bmi=" + bmi)

    # If a GET (or any other method) we'll create a blank form
    else:
        return render(request, "components/user_input_form.html")


@csrf_exempt
def process_input(request):
    if request.method == "POST":
        data = json.loads(request.body)
        bmi = data.get("bmi")
        
        result = prediction_from_models()
        response = {"is_depressed": result}
        return JsonResponse(response)


def submit_to_api(request, bmi):
    BASE_URL = os.getenv("BASE_API_URL")

    url = f"{BASE_URL}/api/process_input"
    data = {"bmi": bmi}
    response = requests.post(url, json=data, timeout=15)

    if response.status_code != 200:
        # Log the error or handle it accordingly
        print(f"Error: {response.text}")
        return None

    return response.json()


def result(request):
    bmi = request.GET.get("bmi")
    result = submit_to_api(request, bmi)
    return render(request, "components/result.html", {"result": result})


def prediction_from_models():
    user_input = get_sample_user_input()

    model_1_prediction = prediction_from_model_1(user_input)
    model_2_prediction = prediction_from_model_2(user_input)
    model_3_prediction = prediction_from_model_3(user_input)

    print(model_1_prediction, model_2_prediction, model_3_prediction)

    all_predictions = model_1_prediction + model_2_prediction + model_3_prediction
    prediction_counts = Counter(all_predictions)
    majority_class = max(prediction_counts, key=prediction_counts.get)
    return "depressed" if majority_class == 1 else "not depressed"


def prediction_from_model_1(user_input):
        # DataFrames with exact column names for each model
    df1_columns = [
        "school_year",
        "age",
        "bmi",
        "phq_score",
        "gad_score",
        "epworth_score",
        "gender_male",
        "who_bmi_Class II Obesity",
        "who_bmi_Class III Obesity",
        "who_bmi_Normal",
        "who_bmi_Not Availble",
        "who_bmi_Overweight",
        "who_bmi_Underweight",
        "depression_severity_Moderate",
        "depression_severity_Moderately severe",
        "depression_severity_None-minimal",
        "depression_severity_Severe",
        "depression_severity_none",
        "depressiveness_True",
        "suicidal_True",
        "depression_treatment_True",
        "anxiety_severity_Mild",
        "anxiety_severity_Moderate",
        "anxiety_severity_None-minimal",
        "anxiety_severity_Severe",
        "anxiousness_True",
        "anxiety_diagnosis_True",
        "anxiety_treatment_True",
        "sleepiness_True",
    ]

    df1 = pd.DataFrame(columns=df1_columns, data=[{col: 0 for col in df1_columns}])
    # Filling out the DataFrame for Model 1
    df1.loc[0, "school_year"] = user_input["school_year"]
    df1.loc[0, "age"] = user_input["age"]
    df1.loc[0, "bmi"] = user_input["bmi"]
    df1.loc[0, "phq_score"] = user_input["phq_score"]
    df1.loc[0, "gad_score"] = user_input["gad_score"]
    df1.loc[0, "epworth_score"] = user_input["epworth_score"]
    df1.loc[0, "gender_male"] = 1 if user_input["gender"] == "Male" else 0

    # Infer BMI category fields
    bmi_categories = {
        "Class II Obesity": "who_bmi_Class II Obesity",
        "Class III Obesity": "who_bmi_Class III Obesity",
        "Normal": "who_bmi_Normal",
        "Not Availble": "who_bmi_Not Availble",
        "Overweight": "who_bmi_Overweight",
        "Underweight": "who_bmi_Underweight",
    }
    df1.loc[0, bmi_categories[user_input["bmi_category"]]] = 1

    # Depression severity related columns
    depression_severities = {
        "Moderate": "depression_severity_Moderate",
        "Moderately severe": "depression_severity_Moderately severe",
        "None-minimal": "depression_severity_None-minimal",
        "Severe": "depression_severity_Severe",
        "none": "depression_severity_none",
    }
    for severity, column in depression_severities.items():
        df1.loc[0, column] = 1 if user_input["depression_severity"] == severity else 0

    # Binary columns based on user input
    df1.loc[0, "depressiveness_True"] = 1 if user_input["depressiveness"] == "Yes" else 0
    df1.loc[0, "suicidal_True"] = 1 if user_input["suicidal"] == "Yes" else 0
    df1.loc[0, "depression_treatment_True"] = (
        1 if user_input["depression_treatment"] == "Yes" else 0
    )

    # Anxiety severity related columns
    anxiety_severities = {
        "Mild": "anxiety_severity_Mild",
        "Moderate": "anxiety_severity_Moderate",
        "None-minimal": "anxiety_severity_None-minimal",
        "Severe": "anxiety_severity_Severe",
    }
    for severity, column in anxiety_severities.items():
        df1.loc[0, column] = 1 if user_input["anxiety_severity"] == severity else 0

    # Additional binary columns for anxiety
    df1.loc[0, "anxiousness_True"] = 1 if user_input["anxiousness"] == "Yes" else 0
    df1.loc[0, "anxiety_diagnosis_True"] = (
        1 if user_input["anxiety_diagnosis"] == "Yes" else 0
    )
    df1.loc[0, "anxiety_treatment_True"] = (
        1 if user_input["anxiety_treatment"] == "Yes" else 0
    )

    # Sleepiness
    df1.loc[0, "sleepiness_True"] = 1 if user_input["sleepiness"] == "Yes" else 0

    # Predict using the model
    return model_1.predict(df1)


def prediction_from_model_2(user_input):
    df2_columns = [
        "Age",
        "SleepPerDayHours",
        "NumberOfFriend",
        "Gender_Male",
        "AcademicPerformance_Below average",
        "AcademicPerformance_Excellent",
        "AcademicPerformance_Good",
        "TakingNoteInClass_Sometimes",
        "TakingNoteInClass_Yes",
        "FaceChallangesToCompleteAcademicTask_Sometimes",
        "FaceChallangesToCompleteAcademicTask_Yes",
        "LikePresentation_Yes",
        "LikeNewThings_Yes",
    ]

    df2 = pd.DataFrame(columns=df2_columns, data=[{col: 0 for col in df2_columns}])

    # Filling out the DataFrame for Model 2
    df2.loc[0, 'Age'] = user_input['age']
    df2.loc[0, 'SleepPerDayHours'] = user_input['sleep_hours']
    df2.loc[0, 'NumberOfFriend'] = user_input['number_of_friends']
    df2.loc[0, 'Gender_Male'] = 1 if user_input['gender'] == 'Male' else 0

    df2.loc[0, 'TakingNoteInClass_Sometimes'] = 1 if user_input['note_taking'] == 'Sometimes' else 0
    df2.loc[0, 'TakingNoteInClass_Yes'] = 1 if user_input['note_taking'] == 'Yes' else 0

    df2.loc[0, 'FaceChallangesToCompleteAcademicTask_Sometimes'] = 1 if user_input['academic_challenges'] == 'Sometimes' else 0
    df2.loc[0, 'FaceChallangesToCompleteAcademicTask_Yes'] = 1 if user_input['academic_challenges'] == 'Yes' else 0

    df2.loc[0, 'LikePresentation_Yes'] = 1 if user_input['likes_presentations'] == 'Yes' else 0

    df2.loc[0, 'LikeNewThings_Yes'] = 1 if user_input['likes_new_things'] == 'Yes' else 0

    # Inferring AcademicPerformance fields based on user input, assuming one is selected
    academic_performance_options = [
        "AcademicPerformance_Below average",
        "AcademicPerformance_Excellent",
        "AcademicPerformance_Good"
    ]
    # Assuming the user input is "Good" for the demo; update this based on actual user input
    selected_academic_performance = "AcademicPerformance_Good"
    for option in academic_performance_options:
        df2.loc[0, option] = 1 if option == selected_academic_performance else 0

    # Predict using the model
    return model_2.predict(df2)


def prediction_from_model_3(user_input):
    df3_columns = [
        "Age",
        "Feeling sad or Tearful",
        "Trouble sleeping at night",
        "Problems concentrating or making decision",
        "Overeating or loss of appetite",
        "Feeling anxious",
        "Feeling of guilt",
    ]
    
    df3 = pd.DataFrame(columns=df3_columns, data=[{col: 0 for col in df3_columns}])

    # Filling out the DataFrame for Model 3
    df3.loc[0, 'Age'] = user_input['age']
    df3.loc[0, 'Feeling sad or Tearful'] = user_input['feeling_sad']
    df3.loc[0, 'Trouble sleeping at night'] = user_input['trouble_sleeping']
    df3.loc[0, 'Problems concentrating or making decision'] = user_input['problems_concentrating']
    df3.loc[0, 'Overeating or loss of appetite'] = user_input['overeating']
    df3.loc[0, 'Feeling anxious'] = user_input['feeling_anxious']
    df3.loc[0, 'Feeling of guilt'] = user_input['feeling_guilt']

    # Predict using the model
    return model_3.predict(df3)


def get_sample_user_input():
    # Simulated user input
    return {
        "gender": "Male",  # "Male", "Female"
        "age": 22,  # [20, 25]
        "school_year": 3,  # [1, 4]
        "sleep_hours": 8,  # number [4, 12]
        "number_of_friends": 15,  # number [0.0, 100.0]
        "phq_score": 5,  # [0, 24]
        "gad_score": 4,  # [0, 21]
        "epworth_score": 10,  # [0.0, 32.0]
        "bmi": 23.5,  # [0.0, 54.55266812]
        "bmi_category": "Normal",  # use categorize_bmi() function
        "depressiveness": "No",
        "suicidal": "No",
        "depression_treatment": "No",
        "anxiousness": "No",
        "anxiety_diagnosis": "No",
        "anxiety_treatment": "No",
        "sleepiness": "No",
        "likes_presentations": "Yes",
        "likes_new_things": "Yes",
        "feeling_anxious": 0,
        "depression_severity": "None-minimal",  # "Moderate", "Moderately severe", "None-minimal", "Severe", "none"
        "anxiety_severity": "Mild",  # "Mild", "Moderate", "None-minimal", "Severe"
        "note_taking": "Sometimes",  # Sometimes, Always (Yes)
        "academic_challenges": "Yes",  # Sometimes, Always (Yes)
        "feeling_sad": 1,  # Rarely, Sometimes, Often [0, 2]
        "trouble_sleeping": 1,  # Rarely, Sometimes, Often [0, 2]
        "overeating": 1,  # Rarely, Sometimes, Often [0, 2]
        "feeling_guilt": 1,  # Rarely, Sometimes, Often, Always [0, 3]
        "problems_concentrating": 2,  # Rarely, Sometimes, Often, Always [0, 3]
    }
