from PIL import Image
import cv2
import pandas as pd
import numpy as np
from datetime import datetime
import keras

filepath = './model_mask.h5'
loaded_model = keras.models.load_model(filepath)

liste_label = ['sans masque', 'avec masque']
# Modele de détection des visage
cascade_path = "./cascades/haarcascade_frontalface_default.xml"

def detecter_masks(imgr):
    img_exp = np.expand_dims(np.array(imgr)/255.0, axis=0)
    prediction = loaded_model.predict(img_exp)
    resultat = liste_label[np.argmax(prediction)]
    image_pred = cv2.putText(imgr, resultat, (20, 30), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (255,0,0))
    return image_pred, resultat

def afficher_visage(img_path):
    to_image = Image.open(img_path)
    src = cv2.cvtColor(np.array(to_image), cv2.COLOR_RGB2BGR)
    cascade = cv2.CascadeClassifier(cascade_path)
    rect = cascade.detectMultiScale(src)

    visages = []
    list_nom_img = []
    tableau = []
    if len(rect) > 0:
        for i,[x, y, w, h] in enumerate(rect):
            img_couper = src[y:y + h, x:x + w]
            imgr = cv2.resize(img_couper,(224,224), interpolation = cv2.INTER_AREA)
            nom_img = "visage{}".format(i+1)

            imgr, mask_port = detecter_masks(imgr)
            visages.append(cv2.cvtColor(imgr, cv2.COLOR_BGR2RGB))
            list_nom_img.append(nom_img)

            date_now = datetime.today()
            tableau.append([f"Visage {i+1}", f"{date_now.day}/{date_now.month}/{date_now.year}", f"{date_now.hour}:{date_now.minute}:{date_now.second}", mask_port])

    
    tableau = pd.DataFrame(tableau, columns=["Personne", "Date", "Heure", "Masque"])

    return visages, list_nom_img, tableau
