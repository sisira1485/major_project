# Import necessary modules
from django.shortcuts import render,HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from user.utility import load_trained_model, make_prediction
from user.models import UserRegistrationModel,UserTextDataModel
import pickle
from django.shortcuts import redirect

# Import necessary modules
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
        else:
            messages.error(request, 'Email or Mobile Already Exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'userregistration.html', {'form': form})

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        try:
            user = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            if user.status == "activated":
                request.session['id'] = user.id
                request.session['loginid'] = loginid
                request.session['email'] = user.email
                request.session['name'] = user.name
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, 'Your Account is not activated')
                return render(request, 'UserLogin.html')
        except UserRegistrationModel.DoesNotExist:
            messages.error(request, 'Invalid Login ID and Password')
    return render(request, 'UserLogin.html', {})

def UserHome(request):
    return render(request, 'users/UserHome.html', {})

# Load the pre-trained model
def load_trained_model(model_path):
    with open(model_path, 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model

# Make predictions using the loaded model
def make_prediction(text_data, loaded_model):
    prediction = loaded_model.predict(text_data)  
    return prediction

def UploadTextAction(request):
    if request.method == 'POST':
        try:
            # Retrieve input data from the form
            General_Health = request.POST.get('General_Health')
            Checkup = request.POST.get('Checkup')
            Exercise = request.POST.get('Exercise')
            Skin_Cancer = request.POST.get('Skin_Cancer')
            Other_Cancer = request.POST.get('Other_Cancer')
            Depression = request.POST.get('Depression')
            Diabetes = request.POST.get('Diabetes')
            Arthritis = request.POST.get('Arthritis')
            Sex = request.POST.get('Sex')
            Age_Category = request.POST.get('Age_Category')
            Height_cm = request.POST.get('Height_cm')
            Weight_kg = request.POST.get('Weight_kg')
            BMI = request.POST.get('BMI')
            Smoking_History = request.POST.get('Smoking_History')
            Alcohol_Consumption = request.POST.get('Alcohol_Consumption')
            Fruit_Consumption = request.POST.get('Fruit_Consumption')
            Green_Vegetables_Consumption = request.POST.get('Green_Vegetables_Consumption')
            FriedPotato_Consumption = request.POST.get('FriedPotato_Consumption')

            # Convert inputs to a list
            features = [
                float(General_Health) if General_Health else None,
                float(Checkup) if Checkup else None,
                float(Exercise) if Exercise else None,
                float(Skin_Cancer) if Skin_Cancer else None,
                float(Other_Cancer) if Other_Cancer else None,
                float(Depression) if Depression else None,
                float(Diabetes) if Diabetes else None,
                float(Arthritis) if Arthritis else None,
                float(Sex) if Sex else None,
                float(Age_Category) if Age_Category else None,
                float(Height_cm) if Height_cm else None,
                float(Weight_kg) if Weight_kg else None,
                float(BMI) if BMI else None,
                float(Smoking_History) if Smoking_History else None,
                float(Alcohol_Consumption) if Alcohol_Consumption else None,
                float(Fruit_Consumption) if Fruit_Consumption else None,
                float(Green_Vegetables_Consumption) if Green_Vegetables_Consumption else None,
                float(FriedPotato_Consumption) if FriedPotato_Consumption else None
            ]

            # Combine input data into a list
            input_data = [features]

            # Load the pre-trained model
            loaded_model = load_trained_model('trained_model1.sav')

            # Make predictions using the loaded model
            prediction = make_prediction(input_data, loaded_model)

            # Get the prediction result
            if prediction[0] == 0:
                prediction_result = 'You do not have cardiovascular disease, but please take care of your health.Have a nice day. '
            else:
                prediction_result = 'You have cardiovascular disease. Please check the About Us page for dietary information.'

            # Render the form with the prediction result
            return render(request, 'text_upload_form.html', {'prediction_result': prediction_result})

        except Exception as e:
            # If an exception occurs, render the upload form again with an error message
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'text_upload_form.html', {'prediction_result': None})

    else:
        return render(request, 'text_upload_form.html', {'prediction_result': None})

def UserViewHistory(request):
    about_content = """
    <h2>About Our Application</h2>
    <p>This application provides valuable insights into cardiovascular health based on user input data. 
    It utilizes machine learning algorithms to predict the risk of cardiovascular disease.</p>
    <p>Our goal is to empower users to make informed decisions about their health and well-being.</p>
    <p>For any inquiries or feedback, please contact us at info@example.com.</p>
    """


    return render(request, "users/UserViewHistory.html", {"about_content": about_content})
