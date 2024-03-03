from datetime import datetime
import json
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os


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
        #prediction = your_model.predict([[bmi]])  # Replace with actual model logic
        prediction = [1]

        response = {
            "is_depressed": "Yes" if prediction[0] == 1 else "No"
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
