# miniproject: Guess the number
# Description: Users has 7 tries to input a number within the range
# or either 0-100 or 0-1000
# by: TP

import simplegui
import random
import math

# initialize global variables used in your code here
num_range = 100

# helper function to start and restart the game
def new_game():
    
    global secret_number, num_range
    secret_number = 0
    frame.start()
    # games start logic
    if (num_range == 100):
        range100()
    elif (num_range == 1000):
        range1000()
    
    # Error catcher
    else:
        print "num_range Error %i" % num_range

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secret_number, trys, num_range
    trys = 6
    num_range = 100
    secret_number = random.randrange(0,100)
    print ""
    print "Guess a number from 0 to 100"

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number, trys, num_range
    trys = 9
    num_range = 1000
    secret_number = random.randrange(0,1000)
    print ""
    print "Guess a number from 0 to 1000"
        
def input_guess(guess):
    global secret_number, trys, num_range
    # main game logic goes here	
    if guess.isdigit():
        guess = int(guess)

        # limit number of trys
        if (trys > 0):
            
            # print users guess
            print ""
            print "Your guess was: %i" % guess
            print "Number of remaining guesses: %i " % trys
            
            # incriment trys
            trys -= 1
            
            # guess logic
            if (guess < secret_number):
                print "Higher!"
            elif (guess > secret_number):
                print "Lower!"
            elif (guess == secret_number):
                print "You guessed the secret number!"
                new_game()
            else:
                print "Game logic error: guess %i, secret %i" % (guess, secret_number)
        
        # Game over message
        elif (trys <= 0):
            print ""
            print "Your guess was: %i" % guess
            print "Number of remaining guesses: %i " % trys
            print "You ran out of Guesses. The number was: %i" % secret_number
            new_game()   
        
        # Error catcher
        else:
            print "input_guess Error %i" % input_guess
    else:
        print "Please enter a non floating point number"
    
# create frame
frame = simplegui.create_frame('Guess a Number', 500,300)

# register event handlers for control elements and start frame
frame.add_button("Range is [0-100)",range100, 200)
frame.add_button("Range is [0-1000)",range1000, 200)
frame.add_input('Enter a guess', input_guess, 200)

# call new_game 
new_game()

