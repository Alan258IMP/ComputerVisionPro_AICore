# Alan (Wentao Li), Imperial College London
# AICore 2022, all rights reserved

'''
This file is a Python implementation of the 'Rock, Paper & Scissors' game (without camera)
'''

import random

action = ['rock', 'paper', 'scissors'] # This should be a global variable really...

def get_computer_choice():
    #action = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(action)
    return computer_choice

def get_user_choice():
    #action = ['rock', 'paper', 'scissors']
    while True:
        user_choice = input('Enter your choice: 1. rock, 2. paper 3. scissors')
        if user_choice not in ['1','2','3']:
            print('Please enter 1, 2 or 3')
        else: break
    return action[int(user_choice) - 1]

def get_winner(user_choice, computer_choice):
    #action = ['rock', 'paper', 'scissors']
    if not (user_choice in action and computer_choice in action):
        raise TypeError('Expected "rock", "paper" or "scissors" as input')
    
    outcome = ['win', 'lose', 'draw']
    if user_choice == computer_choice:
        print('Draw: Both you and computer chose ' + user_choice)
        return outcome[2]
    elif user_choice == 'rock':
        if computer_choice == 'paper':
            print('You lose: you choose rock and computer choose paper')
            return outcome[1]
        else:
            print('You win: you choose rock and computer choose scissors')
            return outcome[0]
    elif user_choice == 'paper':
        if computer_choice == 'scissors':
            print('You lose: you choose rock and computer choose scissors')
            return outcome[1]
        else:
            print('You win: you choose rock and computer choose paper')
            return outcome[0]
    else:
        if computer_choice == 'rock':
            print('You lose: you choose scissors and computer choose rock')
            return outcome[1]
        else:
            print('You win: you choose scissors and computer choose paper')
            return outcome[0]

def play():
    while True:
        computer_choice = get_computer_choice()
        user_choice = get_user_choice()
        outcome = get_winner(user_choice, computer_choice)
        replay = input('Enter r to play again or enter anything else to exit')
        if replay != 'r': break
    return 0

play()