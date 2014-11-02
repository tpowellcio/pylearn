# READ ME FIRST:
#   Basic "Guess the Number" Game PLUS a Bonus Mode
#   To unlock Bonus Mode, user has to win 3 games (NOT necessarily
# consecutively).
#   In the Bonus Mode, user will have only one chance to guess a
# number betwenn [0, 10) and press the corresponding key. If wins,
# user will be provided with a bonus message.

import simplegui
import random
import math

#first opening program is set to guess between 0-100
guess_range = 100
bonus_counter = 0
bonus_number = 0
# helper function to start and restart the game
def new_game():
    """
    initialize the secret number between [0,guess_range)
    """
    global secret_number, remaining, guess_range, bonus_counter
    low = 0
    high = guess_range
    secret_number = random.randrange(0,guess_range)
    remaining = int(math.ceil(math.log(high - low + 1, 2)))
    print "****************"
    print "New game begins: Guess a number between " + "[0, " + str(guess_range) + "):"
    print "You have " + str(remaining) + " remaining guesses now!"   
    print "To unlock Bonus Mode, you have to win aonther " + str(2 - bonus_counter) + " games."
    print ""

def bonus_mode():
    """
    only one chance to guess a number between [0,10)
    """
    print "$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "You unlock the Bonus Mode"
    print "- You'll have ONLY ONE chance to guess a number between [0,10)"
    print "- Press any number button on your keyboard (0-9)."  
    print "" 
    global bonus_number, bonus_chr
    bonus_number = random.randrange(0,9)
    bonus_chr = str(bonus_number)
   
    
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global guess_range 
    guess_range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global guess_range 
    guess_range = 1000 
    new_game()

def bonus_guess(key):
    """
    if keypress number is the same with random number, then user wins
    """
    global bonus_chr, bonus_counter
    if key == simplegui.KEY_MAP[bonus_chr]:
        print "Wowwww! You win!"
        print "Thank you for playing with me."
        print "I'm Fan, living in Victoria, BC, Canada."
    else:
        print "Sorry. Your guess is wrong."
        print "Re-directing back to normal mode..."
    print "$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "$$$$$$$$$$$$$$$$$$$$$$$$$"
    print ""
    bonus_counter = 0
    new_game()
            
def input_guess(guess):
    """
    store the user's guess number
    """
    global guess_number, remaining, bonus_counter
    guess_number = int(guess)
    print "Guess was", guess
    # compare the guess & secret number
    if secret_number > guess_number:
        low = guess_number
        remaining = remaining - 1
        print "Higher!"
        print "You have " + str(remaining) + " remaining guesses now!" 
        print ""   
    elif secret_number < guess_number:
        high = guess_number
        remaining = remaining - 1
        print "Lower!"
        print "You have " + str(remaining) + " remaining guesses now!" 
        print ""
    else:
        print "Correct!"
        bonus_counter = bonus_counter + 1
        print ""
        if bonus_counter == 2:
            bonus_mode()
        else:
            new_game()
    # terminate the game when 0 remaining
    if remaining == 0:
        print "GAME OVER!! You have run out of chances. Try again!"
        print ""
        new_game()   
    
            
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)

# register event handlers for control elements and start frame
keydown_bonus = frame.set_keydown_handler(bonus_guess)
button_100 = frame.add_button("Range: 0 - 100", range100, 200)
button_1000 = frame.add_button("Range: 0 - 1000", range1000, 200)
inp = frame.add_input("Enter your guess number here:", input_guess, 100)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
