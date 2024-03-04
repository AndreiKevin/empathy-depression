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
model_1 = load(os.path.join(current_dir, 'models', 'model_1.joblib')) # BernoulliNB
model_2 = load(os.path.join(current_dir, 'models', 'model_2.joblib')) # RandomForestClassifier
model_3 = load(os.path.join(current_dir, 'models', 'model_3.joblib')) # xgb.XGBClassifier


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)


def get_user_input(request):
    if request.method == 'POST':
        # Assuming there's a form with a 'bmi' field
        bmi = request.POST.get('bmi')
        # You can add more fields as necessary

        # Redirect to a new URL to process the input and display the result
        return HttpResponseRedirect('/result/?bmi=' + bmi)

    # If a GET (or any other method) we'll create a blank form
    else:
        return render(request, 'components/user_input_form.html')


@csrf_exempt
def process_input(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bmi = data.get('bmi')
        
        # Process the BMI through your machine learning model
        # For now, let's assume your model's prediction is stored in a variable 'prediction'
        # prediction_1 = model_1.predict(df1)
        # prediction_2 = model_2.predict(df2)
        # prediction_3 = model_3.predict(df3)

        # print(prediction_1, prediction_2, prediction_3)
        
        # all_predictions = prediction_1 + prediction_2 + prediction_3
        # prediction_counts = Counter(all_predictions)
        # majority_class = max(prediction_counts, key=prediction_counts.get)
        # result = "depressed" if majority_class == 1 else "not depressed"

        result = "yesssss"
        response = {
            "is_depressed": result
        }
        return JsonResponse(response)
    

def submit_to_api(request, bmi):
    BASE_URL = os.getenv('BASE_API_URL')

    url = f'{BASE_URL}/api/process_input'
    data = {'bmi': bmi}
    response = requests.post(url, json=data, timeout=15)

    if response.status_code != 200:
        # Log the error or handle it accordingly
        print(f"Error: {response.text}")
        return None

    return response.json()


def result(request):
    bmi = request.GET.get('bmi')
    result = submit_to_api(request, bmi)
    return render(request, 'components/result.html', {'result': result})
