# Alan (Wentao Li), Imperial College London
# AICore 2022, all rights reserved

'''
This file is a Python implementation of the 'Rock, Paper & Scissors' game (without camera)
'''

import random
import time
import cv2
from keras.models import load_model
import numpy as np

action = ['rock', 'paper', 'scissors'] # This should be a global variable really...

def countdown(wait_time):
    '''
    A simple countdown timer.
    Note this freezes the code as a whole with time.sleep() function
    '''
    if wait_time <= 0:
        raise ValueError("invalid wait time")
    wait_time = int(wait_time)
    print("Get ready...")
    while wait_time >= 0:
        print(int(wait_time))
        time.sleep(1)
        wait_time -= 1
    print("Start!")


def get_prediction():
    '''
    This is adapted from the template provided in "RPS-Template.py"
    '''
    # obtain image
    model = load_model('keras_model.h5')
    cap = cv2.VideoCapture(0)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    user_weight = np.zeros(4)
    image_count = 0

    countdown(3)
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
        user_weight += prediction[0] # Add to user_choice
        image_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                
    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    # Read user's choice
    # Judge: If "nothing" is detected or cannot say with 70%+ confidence, then return "unsure"
    user_weight = user_weight / image_count # To get exact weight of each action
    print(user_weight)
    if np.argmax(user_weight) == 3 or max(user_weight) < 0.7:
        user_choice = "nothing" # Nothing or Undetected
    else:
        user_choice = action[np.argmax(user_weight)] # return rock/paper/scissors
    return user_choice

A = get_prediction()
print(A)
