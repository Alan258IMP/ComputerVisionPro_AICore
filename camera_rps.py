# Alan (Wentao Li), Imperial College London
# AICore 2022, all rights reserved

'''
This file is a Python implementation of the 'Rock, Paper & Scissors' game (without camera)
'''

import random
import cv2
from keras.models import load_model
import numpy as np

action = ['rock', 'paper', 'scissors'] # This should be a global variable really...

def get_prediction():
    '''
    This is adapted from the template provided in "RPS-Template.py"
    '''
    # obtain image
    model = load_model('keras_model.h5')
    cap = cv2.VideoCapture(0)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    user_choice = np.zeros(4)
    image_count = 0

    while True: 
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        cv2.imshow('frame', frame)

        # Press q to close the window
        print(prediction) # This is a numpy array with (1,4) shape (why is it nested in an empty array...)
        user_choice += prediction[0] # Add to user_choice
        image_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                
    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    # Read user's choice
    # user_choice = user_choice / image_count # To get exact weight of each action, but not necessary
    user_choice = action[np.argmax(user_choice)]

    return user_choice

A = get_prediction()
print(A)
