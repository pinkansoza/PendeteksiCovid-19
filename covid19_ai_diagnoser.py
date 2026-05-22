#Code Written By Jordan Bennett
#Modified for MobileNetV2 Integration

import os
import cv2
import numpy as np
import datetime
import tensorflow as tf
from tensorflow.keras.models import load_model
# pyrefly: ignore [missing-import]
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

MODEL_PATH = 'covid_mobilenet_model.h5'
model_covid19 = None
if os.path.exists(MODEL_PATH):
    print("Loading MobileNetV2 Covid-19 Model...")
    model_covid19 = load_model(MODEL_PATH)
else:
    print(f"WARNING: {MODEL_PATH} not found. Please train the model using train_covid_model.ipynb.")

DIAGNOSIS_MESSAGES = [ "Pneumonia detected", "Covid19 detected", "Normal lungs detected" ]

def recordInferenceEvent(imagePath, outputContent):
    currentDate = datetime.datetime.now()
    with open("inference_record.txt", "a") as text_file:
        text_file.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        text_file.write(f"DATE/TIME : {currentDate.month} {currentDate.day}, {currentDate.year}...{currentDate.hour}:{currentDate.minute}:{currentDate.second}\n\n") 
        text_file.write(f"IMAGE : {imagePath}\n\n")
        text_file.write(f"RESULT : \n{outputContent}\n\n\n\n")

def doOnlineInference_covid19Pneumonia(imagePath):
    if model_covid19 is None:
        return "Error: covid_mobilenet_model.h5 not found. Please train the model using train_covid_model.ipynb first.\nRaw Neural Network Output : 0.0"

    img = cv2.imread(imagePath) # Read in color
    if img is None:
        return "Error: Could not read image.\nRaw Neural Network Output : 0.0"
        
    img = cv2.resize(img, (224, 224)) # MobileNetV2 default size
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert BGR to RGB
    
    # Preprocess specifically for MobileNetV2 (scale to [-1, 1])
    img = preprocess_input(img)
    
    test_data = np.array([img])
    prediction = model_covid19.predict(test_data)
    
    raw_score = prediction[0][0]
    score_percentage = round(raw_score * 100, 3)
    
    prediction_msg = "Unknown"
    if score_percentage > 50:
        prediction_msg = DIAGNOSIS_MESSAGES[1]
    elif score_percentage <= 50:
        prediction_msg = DIAGNOSIS_MESSAGES[2]  
        
    outputContent = f"{prediction_msg}\n"
    outputContent += f"Raw Neural Network Output : {raw_score}. A value closer to 1 signifies illness, while a value closer to 0 signifies normalness.\n\n"
    
    recordInferenceEvent(imagePath, outputContent)
    
    return {
        "status": prediction_msg,
        "raw_score": float(raw_score),
        "percentage": float(score_percentage)
    }

