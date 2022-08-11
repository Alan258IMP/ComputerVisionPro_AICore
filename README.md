# ComputerVisionPro_AICore

This Python project is an implementation of the "Rock, Paper, Scissors" game with camera. The model will take an image with the camera and recognize if it's rock, paper or scissors through a machine-learning model created with [Teachable-Machine](https://teachablemachine.withgoogle.com/ ).

This project requires [opencv-python](https://github.com/opencv/opencv-python), [tensorflow](https://github.com/tensorflow) and [ipykernel](https://github.com/ipython/ipykernel) modules.

## Milestone 1 & 2: Creating the machine-learning model

Firstly I created the model with 4 classes: rock, paper, scissors and nothing. I fed ~250 sample images to each class with the camera on my laptop. The sample images were then used to train the model through 60 epochs. After training the model seems to distinguish each class reasonably well.

## Milestone 3: Install the libraries for the model

I installed the necessary dependencies for this project including opencv-python, tensorflow and ipykernel in a new virtual conda environment named "ComputerVision". Then I confirmed all modules are working as expected by running the example script provided ("RPS-Template.py"), which takes an image and use the model "keras_model.h5" to analyse it.

Note: If you are running the code on a device with Nvidia Graphic card, there is no need to install CUDA for this script to normally function, and all warning messages about "cudartxxx.dll file missing" can be safely ignored.

## Milestone 4: Code the game 

I coded the logic of the game in "manual_rps.py" file. This script lets the computer to randomly choose from rock, paper or scissors and then gets the choice of the user via keyboard input. Finally the script tells the user who wins the game.

## Milestone 5: Use the camera to play the game

We put everything together in "camera_rps.py" and rewrote the game in a class "RPS-game". This class contains "get_prediction()" method which is adapted from the example script "RPS-Template.py". The user will be asked to get the camera ready, and the image will be taken after a 2-second countdown. The camera will then be active for 3 seconds and only the final image counts. Note that this method will return "nothing" if it cannot fit the image to rock / paper / scissors with more than 70% confidence.

Finally, we code the procedure of the game in the "play_rps()" function. This function creates an instance of the "RPS-game" class and then run the game repeatedly until one side get more than a set amount of victories (3 by default).

