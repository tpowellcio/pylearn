# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in code
low = 0
high = 100
secret_number = 0
remaining_guesses = 0

# helper functions to initial game

def init():
    range100()

# helper function to create a new game
def new_game(low1, high1):
    global secret_number, remaining_guesses, low, high
    low = low1
    high = high1
    secret_number = random.randrange(low, high)
    remaining_guesses = math.ceil(math.log(high - low,2))
    
    print "\nNew game. Range is from", low, "to", high
    print "Number of remaining guesses is:", remaining_guesses
    
# define event handlers for control panel
    
def range100():
    # button that changes range to range [0, 100) and restarts
    new_game(0,100)

def range1000():
    # button that changes range to range [0, 1000) and restarts
    new_game(0,1000)

def get_input(guess):
    global secret_number, remaining_guesses
    remaining_guesses = remaining_guesses - 1
    guess = int(guess)
    
    print "\nGuess was", guess
    #print "Number of remaining guesses is", remaining_guesses
    
    if remaining_guesses > 0:
        if guess > secret_number:
            print "Number of remaining guesses is", remaining_guesses
            print "Lower!"
        elif guess < secret_number:
            print "Number of remaining guesses is", remaining_guesses
            print "Higher!"
        else:
            print "You are correct!"
            new_game(low,high)
    else:
        if guess == secret_number:
            print "You are correct!"
        else:
            print "You ran out of guesses. The number was", secret_number
        new_game(low,high)
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", get_input, 200)

# start frame
init()

# always remember to check your completed program against the grading rubric

