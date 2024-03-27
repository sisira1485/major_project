# utility.py

import pickle

def load_trained_model(model_path):
    with open(model_path, 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model

def make_prediction(text_data, loaded_model):
    prediction = loaded_model.predict(text_data)  # Adjust this according to your model's prediction method
    return prediction
