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
    return render(request, "components/user_input_form.html")


def evaluate_recommendations(user_input):
    recommendations = [
        {
            "id": "1",
            "title": "Master Stress Management",
            "description": "Learn and practice stress management techniques such as mindfulness, meditation, or yoga to improve your mental health and enhance your overall well-being.",
            "icon": "IconActivityHeartbeat",
            "url": "https://www.google.com/",
            "trigger": [
                {"label": "feeling_anxious", "value": "1"},
                {"label": "phq_score", "value": ">10"},
            ],
        },
        {
            "id": "2",
            "title": "Engage in Regular Exercise",
            "description": "Regular physical activity can significantly improve your mental health, reduce anxiety and depression levels, and elevate your mood. Aim for at least 30 minutes of moderate exercise most days of the week.",
            "icon": "IconStretching",
            "url": "https://www.google.com/",
            "trigger": [
                {"label": "bmi", "value": ">25"},
                {"label": "depressiveness", "value": "Yes"},
            ],
        },
        {
            "id": "3",
            "title": "Seek Professional Mental Health Support",
            "description": "If you're experiencing signs of depressiveness, anxiety, or suicidal thoughts, it's important to seek help from a mental health professional. They can offer guidance, therapy, and sometimes medication to help you manage your mental health effectively.",
            "icon": "IconUserSearch",
            "url": "https://www.mentalhealth.gov/get-help/immediate-help",
            "trigger": [
                {"label": "depressiveness", "value": "Yes"},
                {"label": "suicidal", "value": "Yes"},
                {"label": "anxiety_diagnosis", "value": "Yes"},
            ],
        },
        {
            "id": "4",
            "title": "Improve Your Sleep Hygiene",
            "description": "Good sleep is crucial for mental health. Develop a bedtime routine, limit screen time before bed, and create a comfortable sleep environment. Consider seeking professional advice if you frequently have trouble sleeping.",
            "icon": "IconMoon",
            "url": "https://www.sleepfoundation.org/sleep-hygiene",
            "trigger": [
                {"label": "sleep_hours", "value": "<7"},
                {"label": "epworth_score", "value": ">10"},
                {"label": "trouble_sleeping", "value": "2"},
            ],
        },
        {
            "id": "5",
            "title": "Adopt a Healthy Diet",
            "description": "Eating a balanced diet can help regulate your mood, improve your energy levels, and enhance your overall health. Consider consulting a nutritionist to create a diet plan that suits your lifestyle and preferences.",
            "icon": "IconCarrot",
            "url": "https://www.nutrition.gov/topics/basic-nutrition/healthy-eating",
            "trigger": [
                {"label": "overeating", "value": "2"},
                {"label": "bmi", "value": ">25"},
            ],
        },
        {
            "id": "6",
            "title": "Cultivate Social Connections",
            "description": "Building strong, healthy relationships can help reduce feelings of loneliness and isolation. Engage in community activities, join clubs, or reach out to friends and family to strengthen your social network.",
            "icon": "IconUsers",
            "url": "https://www.mentalhealth.org.uk/publications/relationships-and-mental-health",
            "trigger": [
                {"label": "number_of_friends", "value": "<3"},
                {"label": "feeling_sad", "value": "1"},
                {"label": "feeling_sad", "value": "2"},
            ],
        },
        {
            "id": "7",
            "title": "Practice Mindfulness and Relaxation Techniques",
            "description": "Mindfulness, meditation, and relaxation exercises can help you manage stress, reduce anxiety, and improve your mental clarity. These practices can be integrated into your daily routine to enhance your overall well-being.",
            "icon": "IconLeaf",
            "url": "https://www.mindful.org/meditation/mindfulness-getting-started/",
            "trigger": [
                {"label": "feeling_anxious", "value": "1"},
                {"label": "anxiousness", "value": "Yes"},
            ],
        },
        {
            "id": "8",
            "title": "Engage in Cognitive Behavioral Therapy (CBT)",
            "description": "CBT is a highly effective treatment for depression, helping you to identify and challenge negative thought patterns and engage in more positive behaviors. Consider finding a licensed therapist who specializes in CBT.",
            "icon": "IconBrain",
            "url": "https://www.apa.org/ptsd-guideline/patients-and-families/cognitive-behavioral",
            "trigger": [
                {"label": "depression_severity", "value": "Moderate"},
                {"label": "depression_severity", "value": "Moderately severe"},
                {"label": "depression_severity", "value": "Severe"},
            ],
        },
        {
            "id": "9",
            "title": "Regularly Update Your Personal Goals",
            "description": "Setting and working towards personal goals can provide a sense of purpose and direction, which is important for mental health. Ensure your goals are realistic, measurable, and time-bound.",
            "icon": "IconTarget",
            "url": "https://www.mindtools.com/pages/article/newHTE_90.htm",
            "trigger": [
                {"label": "feeling_guilt", "value": "2"},
                {"label": "feeling_guilt", "value": "3"},
            ],
        },
        {
            "id": "10",
            "title": "Maintain a Regular Routine",
            "description": "Keeping a consistent daily routine can improve your sense of stability and predictability, which can be comforting when feeling depressed. Try to maintain regular times for eating, sleeping, working, and socializing.",
            "icon": "IconCalendar",
            "url": "https://www.verywellmind.com/the-importance-of-routine-in-times-of-uncertainty-4802594",
            "trigger": [
                {"label": "trouble_sleeping", "value": "2"},
                {"label": "overeating", "value": "1"},
            ],
        },
        {
            "id": "11",
            "title": "Incorporate Physical Activity into Your Routine",
            "description": "Exercise can be as effective as medications in treating mild to moderate depression. It also helps with anxiety, stress, and improving mood through the release of endorphins. Find activities you enjoy and aim to be active for at least 30 minutes a day.",
            "icon": "IconRun",
            "url": "https://www.helpguide.org/articles/healthy-living/the-mental-health-benefits-of-exercise.htm",
            "trigger": [
                {"label": "phq_score", "value": ">10"},
                {"label": "feeling_sad", "value": "1"},
                {"label": "feeling_sad", "value": "2"},
            ],
        },
        {
            "id": "12",
            "title": "Prioritize Social Interaction",
            "description": "Social support is crucial in managing symptoms of depression. Make an effort to connect with loved ones, join support groups, or participate in community activities to enhance your social network.",
            "icon": "IconMessageCircle",
            "url": "https://www.mentalhealth.org.uk/a-to-z/s/social-support-and-mental-health",
            "trigger": [
                {"label": "number_of_friends", "value": "<3"},
                {"label": "feeling_anxious", "value": "1"},
            ],
        },
        {
            "id": "13",
            "title": "Develop Stress Management Strategies",
            "description": "Effective stress management can reduce the symptoms of depression. Techniques such as deep breathing exercises, progressive muscle relaxation, or practicing mindfulness can be beneficial.",
            "icon": "IconDeviceFloppy",
            "url": "https://www.mayoclinic.org/healthy-lifestyle/stress-management/in-depth/stress-relievers/art-20047257",
            "trigger": [
                {"label": "feeling_anxious", "value": "1"},
                {"label": "problems_concentrating", "value": "2"},
            ],
        },
        {
            "id": "14",
            "title": "Explore Art Therapy",
            "description": "Art therapy can be a powerful way to express your feelings and improve mental health. It helps to explore emotions, develop self-awareness, cope with stress, and boost self-esteem.",
            "icon": "IconPalette",
            "url": "https://www.psychologytoday.com/us/therapy-types/art-therapy",
            "trigger": [
                {"label": "depression_treatment", "value": "No"},
                {"label": "academic_challenges", "value": "Yes"},
            ],
        },
        {
            "id": "15",
            "title": "Establish a Mindful Eating Practice",
            "description": "Mindful eating can help you rebuild a healthy relationship with food, focusing on the experience and enjoyment of eating, which can be beneficial if you're dealing with overeating or anxiety related to food.",
            "icon": "IconGrillFork",
            "url": "https://www.healthline.com/nutrition/mindful-eating-guide",
            "trigger": [
                {"label": "overeating", "value": "1"},
                {"label": "overeating", "value": "2"},
            ],
        },
        {
            "id": "16",
            "title": "Consider Journaling for Emotional Expression",
            "description": "Journaling can be a therapeutic practice, allowing you to express thoughts and emotions, reflect on your feelings, and identify patterns in your behavior that may be contributing to your depression or anxiety.",
            "icon": "IconNotebook",
            "url": "https://www.psychologytoday.com/us/blog/words-matter/201812/how-journaling-can-help-you-in-hard-times",
            "trigger": [
                {"label": "feeling_sad", "value": "1"},
                {"label": "feeling_guilt", "value": "2"},
            ],
        },
        {
            "id": "17",
            "title": "Engage in Volunteering",
            "description": "Volunteering can increase your sense of community, boost your self-esteem, and provide a sense of purpose. It can also be a way to build new relationships and combat feelings of isolation.",
            "icon": "IconHandStop",
            "url": "https://www.helpguide.org/articles/healthy-living/volunteering-and-its-surprising-benefits.htm",
            "trigger": [
                {"label": "likes_new_things", "value": "Yes"},
                {"label": "feeling_anxious", "value": "1"},
            ],
        },
        {
            "id": "18",
            "title": "Practice Positive Self-Affirmations",
            "description": "Positive affirmations can help challenge and overcome self-sabotaging and negative thoughts. Repeating affirmations can encourage positive changes in your life and boost your self-esteem.",
            "icon": "IconBulb",
            "url": "https://www.healthline.com/health/mental-health/positive-affirmations",
            "trigger": [
                {"label": "problems_concentrating", "value": "1"},
                {"label": "feeling_guilt", "value": "3"},
            ],
        },
        {
            "id": "19",
            "title": "Create a Relaxation Routine Before Bed",
            "description": "Developing a pre-sleep routine to relax and unwind can improve your sleep quality. Consider practices like reading, taking a warm bath, or gentle stretching to signal your body it's time to sleep.",
            "icon": "IconBedOff",
            "url": "https://www.sleepfoundation.org/sleep-hygiene/relaxation-exercises-to-help-fall-asleep",
            "trigger": [
                {"label": "trouble_sleeping", "value": "1"},
                {"label": "sleepiness", "value": "Yes"},
            ],
        },
        {
            "id": "20",
            "title": "Learn and Practice Stress Reduction Techniques",
            "description": "Stress can exacerbate or trigger depression and anxiety. Techniques like guided imagery, progressive muscle relaxation, or yoga can reduce stress levels and promote a sense of peace.",
            "icon": "IconSun",
            "url": "https://www.verywellmind.com/tips-to-reduce-stress-3145195",
            "trigger": [
                {"label": "feeling_anxious", "value": "1"},
                {"label": "anxiety_severity", "value": "Moderate"},
                {"label": "anxiety_severity", "value": "Mild"},
                {"label": "anxiety_severity", "value": "Severe"},
            ],
        },
        {
            "id": "21",
            "title": "Enhance Academic Skills",
            "description": "Improving your academic skills, such as time management, note-taking, and effective studying, can reduce academic stress and enhance your learning experience. Consider workshops or online resources to develop these skills.",
            "icon": "IconSchool",
            "url": "https://www.educationcorner.com/study-skills-guide.html",
            "trigger": [
                {"label": "academic_challenges", "value": "Yes"},
                {"label": "note_taking", "value": "Sometimes"},
            ],
        },
        {
            "id": "22",
            "title": "Explore New Interests",
            "description": "Engaging in new hobbies or interests can boost your mental health, provide a sense of achievement, and reduce feelings of anxiety or depression. Consider trying something new that excites or challenges you.",
            "icon": "IconBallBasketball",
            "url": "https://www.psychologytoday.com/us/blog/what-mentally-strong-people-dont-do/201504/7-reasons-why-everyone-should-take-up-hobby",
            "trigger": [
                {"label": "likes_new_things", "value": "No"},
                {"label": "likes_presentations", "value": "No"},
            ],
        },
        {
            "id": "23",
            "title": "Adjust Your Study Environment",
            "description": "Creating a study environment that promotes concentration and minimizes distractions can enhance your learning efficiency and academic performance. Consider organizing your study space, using noise-canceling headphones, or studying during quieter times.",
            "icon": "IconLayout",
            "url": "https://www.oxfordlearning.com/tips-for-creating-study-space/",
            "trigger": [
                {"label": "problems_concentrating", "value": "2"},
                {"label": "problems_concentrating", "value": "3"},
            ],
        },
        {
            "id": "24",
            "title": "Regular Medical Check-ups",
            "description": "Regular check-ups can help find potential health issues before they become a problem. Early detection gives you the best chance for getting the right treatment quickly, avoiding any complications.",
            "icon": "IconReportMedical",
            "url": "https://www.healthline.com/health/annual-physical-examinations",
            "trigger": [
                {"label": "anxiety_treatment", "value": "Yes"},
                {"label": "depression_treatment", "value": "Yes"},
            ],
        },
        {
            "id": "25",
            "title": "Mindful Breathing Exercises",
            "description": "Mindful breathing exercises can help reduce stress, improve your focus, and calm your mind. Practice breathing techniques daily, focusing on slow, deep breaths to help manage anxiety and improve mental clarity.",
            "icon": "IconWind",
            "url": "https://www.mindful.org/a-five-minute-breathing-meditation/",
            "trigger": [
                {"label": "feeling_anxious", "value": "Often/Always"},
                {"label": "anxiety_severity", "value": "Mild"},
            ],
        },
        {
            "id": "26",
            "title": "Participate in Support Groups",
            "description": "Joining a support group can provide a sense of belonging, reduce feelings of isolation, and offer a space to share experiences and coping strategies with others facing similar challenges.",
            "icon": "IconHomeHeart",
            "url": "https://www.verywellmind.com/benefits-of-joining-a-support-group-4842335",
            "trigger": [
                {"label": "suicidal", "value": "Yes"},
                {"label": "anxiety_diagnosis", "value": "Yes"},
            ],
        },
        {
            "id": "27",
            "title": "Regular Mental Health Screenings",
            "description": "Regular mental health check-ups can help detect issues early and provide a clear picture of your mental health over time. It's advisable to undergo screenings, especially if you have a history or risk factors of mental health conditions.",
            "icon": "IconHealthRecoginition",
            "url": "https://www.nimh.nih.gov/health/topics/mental-health-screening",
            "trigger": [
                {"label": "gad_score", "value": ">5"},
                {"label": "age", "value": ">18"},
            ],
        },
        {
            "id": "28",
            "title": "Active Learning Strategies",
            "description": "Engaging actively with your learning material can improve comprehension and retention. Try methods like summarizing information, teaching others, or applying concepts to practical situations to deepen your understanding.",
            "icon": "IconBellSchool",
            "url": "https://www.cmu.edu/teaching/designteach/teach/instructionalstrategies/activelearning.html",
            "trigger": [
                {"label": "likes_presentations", "value": "No"},
                {"label": "school_year", "value": "2"},
            ],
        },
        {
            "id": "29",
            "title": "Encourage Curiosity and Exploration",
            "description": "Fostering a sense of curiosity can enhance your mental flexibility and creativity. Encourage yourself to explore new hobbies, learn new skills, or simply try new experiences to stimulate your mind and broaden your horizons.",
            "icon": "IconZoomQuestion",
            "url": "https://www.psychologytoday.com/us/blog/curious/201412/the-benefits-cultivating-curiosity",
            "trigger": [{"label": "likes_new_things", "value": "No"}],
        },
        {
            "id": "30",
            "title": "Structured Problem-Solving Techniques",
            "description": "Learning structured problem-solving techniques can help you manage life's challenges more effectively. This skill can reduce the stress associated with academic or personal problems by providing a clear framework for finding solutions.",
            "icon": "IconPuzzle",
            "url": "https://www.mindtools.com/pages/article/newTMC_00.htm",
            "trigger": [{"label": "problems_concentrating", "value": "3"}],
        },
        {
            "id": "31",
            "title": "Participate in Public Speaking Workshops",
            "description": "Public speaking is a valuable skill that can enhance your self-confidence and communication abilities. Workshops or local groups can provide a supportive environment to practice and improve your public speaking skills.",
            "icon": "IconMicrophone",
            "url": "https://www.toastmasters.org/",
            "trigger": [{"label": "likes_presentations", "value": "No"}],
        },
        {
            "id": "32",
            "title": "Develop Emotional Resilience",
            "description": "Building emotional resilience can help you navigate stressful situations and bounce back from setbacks. Techniques like cognitive reframing, building optimism, and maintaining social connections can strengthen your resilience.",
            "icon": "IconShieldCheck",
            "url": "https://www.apa.org/topics/resilience",
            "trigger": [{"label": "feeling_sad", "value": "2"}],
        },
        {
            "id": "33",
            "title": "Engage in Mind-Body Practices",
            "description": "Mind-body practices like yoga, tai chi, or qigong can improve your physical health, reduce stress, and enhance your mental clarity. These practices combine physical movement, mental focus, and deep breathing to promote overall well-being.",
            "icon": "IconAccessible",
            "url": "https://www.nccih.nih.gov/health/mindbody-practices",
            "trigger": [{"label": "bmi", "value": ">24"}],
        },
        {
            "id": "34",
            "title": "Cultivate a Growth Mindset",
            "description": "Adopting a growth mindset can significantly enhance your personal and academic growth. Embrace challenges, persist in the face of setbacks, and see effort as a path to mastery. This mindset can lead to a love for learning and resilience.",
            "icon": "IconGrowth",
            "url": "https://www.mindsetworks.com/science/",
            "trigger": [
                {"label": "likes_new_things", "value": "No"},
                {"label": "academic_challenges", "value": "Yes"},
            ],
        },
        {
            "id": "35",
            "title": "Integrate Brain-Boosting Foods into Your Diet",
            "description": "Incorporating foods rich in omega-3 fatty acids, antioxidants, and vitamins can support brain health, improve memory, and reduce the risk of cognitive decline. Consider adding foods like fish, berries, nuts, and leafy greens to your diet.",
            "icon": "IconFish",
            "url": "https://www.health.harvard.edu/mind-and-mood/foods-linked-to-better-brainpower",
            "trigger": [
                {"label": "bmi", "value": "<18"},
                {"label": "bmi", "value": "18-25"},
            ],
        },
    ]

    matched_recommendations = []

    for recommendation in recommendations:
        match = True
        for trigger in recommendation["trigger"]:
            label = trigger["label"]
            value = trigger["value"]

            # Handling different types of triggers
            if ">" in value:
                num_value = float(value.strip(">"))
                if not (label in user_input and float(user_input[label]) > num_value):
                    match = False
                break
            elif "<" in value:
                num_value = float(value.strip("<"))
                if not (label in user_input and float(user_input[label]) < num_value):
                    match = False
                break
            else:
                if not (label in user_input and user_input[label] == value):
                    match = False

        if match:
            matched_recommendations.append(recommendation)

    return matched_recommendations


# Backend
@csrf_exempt
def result(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # infer bmi_category column
        print("received data:", data)
        data["bmi_category"] = categorize_bmi(data["bmi"])
        result = prediction_from_models(data)
        recommendations = evaluate_recommendations(user_input=data)
        return JsonResponse(
            {"is_depressed": result, "recommendations": recommendations}
        )  # jsonify the result
    return render(
        request, "components/user_input_form.html"
    )  # remove unnecessary "else" statement


def prediction_from_models(user_input):
    # user_input = get_sample_user_input()
    print("user_input given to models:", user_input)

    # cast the input to the correct data types
    user_input["age"] = int(user_input["age"])
    user_input["school_year"] = int(user_input["school_year"])
    user_input["sleep_hours"] = int(user_input["sleep_hours"])
    user_input["number_of_friends"] = int(user_input["number_of_friends"])
    user_input["phq_score"] = int(user_input["phq_score"])
    user_input["gad_score"] = int(user_input["gad_score"])
    user_input["epworth_score"] = int(user_input["epworth_score"])
    user_input["bmi"] = int(user_input["bmi"])
    user_input["feeling_anxious"] = int(user_input["feeling_anxious"])
    user_input["feeling_sad"] = int(user_input["feeling_sad"])
    user_input["trouble_sleeping"] = int(user_input["trouble_sleeping"])
    user_input["overeating"] = int(user_input["overeating"])
    user_input["feeling_guilt"] = int(user_input["feeling_guilt"])
    user_input["problems_concentrating"] = int(user_input["problems_concentrating"])

    model_1_prediction = prediction_from_model_1(user_input)
    model_2_prediction = prediction_from_model_2(user_input)
    # https://www.kaggle.com/datasets/parvezalmuqtadir2348/postpartum-depression
    model_3_prediction = prediction_from_model_3(user_input)

    print(model_1_prediction, model_2_prediction, model_3_prediction)

    all_predictions = model_1_prediction + model_2_prediction + model_3_prediction
    prediction_counts = sum(all_predictions)
    if prediction_counts == 1:
        return "1"
    elif prediction_counts == 2:
        return "2"
    elif prediction_counts == 3:
        return "3"
    else:
        return "0"


def categorize_bmi(bmi=None):
    if bmi is None:
        return "Not Available"

    bmi = int(bmi)

    if bmi < 0:
        return "Not Available"
    elif bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    elif 30 <= bmi <= 34.9:
        return "Class II Obesity"  # Assuming Class I Obesity is grouped here
    elif 35 <= bmi <= 39.9:
        return "Class II Obesity"
    elif bmi >= 40:
        return "Class III Obesity"
    else:
        return "Not Available"


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
    df1.loc[0, "depressiveness_True"] = (
        1 if user_input["depressiveness"] == "Yes" else 0
    )
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
    df2.loc[0, "Age"] = user_input["age"]
    df2.loc[0, "SleepPerDayHours"] = user_input["sleep_hours"]
    df2.loc[0, "NumberOfFriend"] = user_input["number_of_friends"]
    df2.loc[0, "Gender_Male"] = 1 if user_input["gender"] == "Male" else 0

    df2.loc[0, "TakingNoteInClass_Sometimes"] = (
        1 if user_input["note_taking"] == "Sometimes" else 0
    )
    df2.loc[0, "TakingNoteInClass_Yes"] = 1 if user_input["note_taking"] == "Yes" else 0

    df2.loc[0, "FaceChallangesToCompleteAcademicTask_Sometimes"] = (
        1 if user_input["academic_challenges"] == "Sometimes" else 0
    )
    df2.loc[0, "FaceChallangesToCompleteAcademicTask_Yes"] = (
        1 if user_input["academic_challenges"] == "Yes" else 0
    )

    df2.loc[0, "LikePresentation_Yes"] = (
        1 if user_input["likes_presentations"] == "Yes" else 0
    )

    df2.loc[0, "LikeNewThings_Yes"] = (
        1 if user_input["likes_new_things"] == "Yes" else 0
    )

    # Inferring AcademicPerformance fields based on user input, assuming one is selected
    academic_performance_options = [
        "AcademicPerformance_Below average",
        "AcademicPerformance_Excellent",
        "AcademicPerformance_Good",
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
    df3.loc[0, "Age"] = user_input["age"]
    df3.loc[0, "Feeling sad or Tearful"] = user_input["feeling_sad"]
    df3.loc[0, "Trouble sleeping at night"] = user_input["trouble_sleeping"]
    df3.loc[0, "Problems concentrating or making decision"] = user_input[
        "problems_concentrating"
    ]
    df3.loc[0, "Overeating or loss of appetite"] = user_input["overeating"]
    df3.loc[0, "Feeling anxious"] = user_input["feeling_anxious"]
    df3.loc[0, "Feeling of guilt"] = user_input["feeling_guilt"]

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
