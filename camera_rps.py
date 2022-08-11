# Alan (Wentao Li), Imperial College London
# AICore 2022, all rights reserved

'''
This script contains all the classes & functions required for the Python 
implementation of the "Rock, Paper & Scissors" game (with camera)
'''

import random
import time
import cv2
from keras.models import load_model
import numpy as np


######### Global variables ############
action = ['rock', 'paper', 'scissors'] # Should this be a class attribute instead?

######### Convenience functions ############

def countdown(wait_time: int):
    '''
    A simple countdown timer.
    Note this freezes the code as a whole with time.sleep() function
    '''
    if wait_time <= 0:
        raise ValueError('Invalid wait time')
    
    wait_time = int(wait_time)
    print('Get ready...')
    while wait_time > 0:
        print('Starting to take image in %d sec'%(wait_time))
        time.sleep(1)
        wait_time -= 1
    print('Start!')


######### Classes ############
class RPS_game:
    '''
    Play the "Rock, Paper & Scissors" game with the computer, with or without camera.
    The game repeats until the player or the computer get a certain number of victories.

    Parameters:
    ----------
    
    Attributes:
    ----------
    user_victory: int
        Number of victories user has got
    computer_victory: int
        Number of victories computer has got
    user_choice: str
        User's choice from all possible actions ('rock', 'paper' or 'scissors')
    computer_choice: str
        Computer's choice from all possible actions
    round_count: int
        Number of rounds the game has done

    Methods:
    -------
    get_computer_choice()
        Let the computer randomly pick an option from all possible actions and update computer_choice.
    get_user_choice(camera = True, duration = 3)
        Get the user's choice and update user_choice.
        If the user has no camera, get user's choice via keyboard input instead.
    get_prediction(duration = 3)
        Get the user's choice by taking an image with the computer's camera.
        After the camera is ready the user will be asked to press enter to continue.
        The image will be taken in 3 seconds.
        Adapted from the template provided in "RPS-Template.py"
    get_winner()
        Judge who is the winner through the logic paper -> rock -> scissor -> paper, then print the result.
    new_round(camera = True, duration = 3)
        Start a new round: Get the choices of the computer and the user, judge who wins, and then save the
        result in user_victory and computer_victory attributes.
    reset_game()
        Resets the game - Reset all attributes to their initial value.
    '''

    def __init__(self):
        self.user_victory = 0
        self.computer_victory = 0
        self.user_choice = ''
        self.computer_choice = ''
        self.round_count = 1
    
    def get_computer_choice(self):
        self.computer_choice = random.choice(action)
        return self.computer_choice
    
    def get_prediction(self, duration = 3):
        # Get the camera ready
        model = load_model('keras_model.h5')
        cap = cv2.VideoCapture(0)
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        #image_count = 0
        # Countdown after user is ready
        print('')
        input('The camera is ready. Press enter to continue...')
        countdown(2)
        start_time = time.time()
        while time.time() < (start_time + duration):
            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            data[0] = normalized_image
            prediction = model.predict(data)
            cv2.imshow('frame', frame)

            print(prediction) # This is a numpy array with (1,4) shape (why is it nested in an empty array...)
            #user_weight += prediction[0] # Don't do take multiple images + taking average stuff. Useless in this case
            #image_count += 1

            # Press q to quit early
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        # After the loop, release the cap object
        cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
        # Read user's choice
        # Judge: If 'nothing' is detected or cannot say with 70%+ confidence, then return 'unsure'
        user_weight = prediction[0]
        print(user_weight)
        if np.argmax(user_weight) == 3 or max(user_weight) < 0.7:
            self.user_choice = 'nothing' # Nothing or Undetected
            print('Failed to detect anything. Please try again')
        else:
            self.user_choice = action[np.argmax(user_weight)] # return rock/paper/scissors
            print('You chose ' + self.user_choice)
        return self.user_choice
    
    def get_user_choice(self, camera = True, duration = 3):
        if camera:
            self.user_choice = self.get_prediction(duration)
            return self.user_choice
        else:
            # If no camera: Ask for an input via keyboard
            while True:
                user_choose = input('Enter your choice: 1. rock, 2. paper 3. scissors')
                if user_choose not in ['1','2','3']:
                    print('Please, enter 1, 2 or 3')
                else: break
            self.user_choice = action[int(user_choose) - 1]
            return self.user_choice
    
    def get_winner(self):
        #action = ['rock', 'paper', 'scissors']
        if not (self.user_choice in action and self.computer_choice in action):
            raise TypeError('Expected "rock", "paper" or "scissors" as input')
        #outcome = ['win', 'lose', 'draw']
        if self.user_choice == self.computer_choice:
            print('Draw: Both you and computer chose ' + self.user_choice)
            return 'draw'
        elif self.user_choice == 'rock':
            if self.computer_choice == 'paper':
                print('You lose this round: you choose rock and computer choose paper')
                return 'lose'
            else:
                print('You win this round: you choose rock and computer choose scissors')
                return 'win'
        elif self.user_choice == 'paper':
            if self.computer_choice == 'scissors':
                print('You lose this round: you choose rock and computer choose scissors')
                return 'lose'
            else:
                print('You win this round: you choose rock and computer choose paper')
                return 'win'
        else:
            if self.computer_choice == 'rock':
                print('You lose this round: you choose scissors and computer choose rock')
                return 'lose'
            else:
                print('You win this round: you choose scissors and computer choose paper')
                return 'win'
    
    def new_round(self, camera = True, duration = 3):
        print('ROUND %.d' %(self.round_count))
        # Reset choices
        self.user_choice = ''
        self.computer_choice = ''
        
        while self.user_choice not in action:
            self.get_user_choice(camera, duration)
        self.get_computer_choice()

        self.round_count += 1
        result = self.get_winner()
        if result == 'win':
            self.user_victory += 1
        elif result == 'lose':
            self.computer_victory += 1
        else:
            pass
    
    def reset_game(self):
        self.user_victory = 0
        self.computer_victory = 0
        self.user_choice = ''
        self.computer_choice = ''
        self.round_count = 1

def play_rps(victory_num = 3):
    '''
    Play the "Rock, Paper & Scissors" game.
    The game continues until one side get a set number of victories.
    '''
    print('Welcome to the Rock-Paper-Scissors Game!')
    print('This game can be played with or without a camera')
    while True:
        camera_ask = input('Would you like to play with the camera? (y/n)')
        if camera_ask == 'y':
            camera = True
            break
        elif camera_ask == 'n':
            camera = False
            break
        else:
            print('Please input y or n')
    
    while True:
        game = RPS_game()
        while True:
            game.new_round(camera)
            if game.computer_victory == victory_num:
                print('The computer has won %.d times! You lose!' %(victory_num))
                break
            elif game.user_victory == victory_num:
                print('Congratulations - you have won %.d times! You win!' %(victory_num))
                break
        replay = input('Enter r to play again or press enter to exit')
        if replay != 'r': break

if __name__ == '__main__':
    play_rps()

