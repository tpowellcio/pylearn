# implementation of card game - Memory

import simplegui
import random

click_pos = (50, 100)
W = 800
H = 100
shown_cards = [False] * 16
cardlist =  range(8) * 2
clicked_cards = []
turn = 0

# helper function to initialize globals
def new_game():
    global state, clicked_cards, shown_cards, turn
    state = 0
    random.shuffle(cardlist)
    shown_cards = [False] * 16
    clicked_cards = []
    turn = 0
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, clicked_cards, turn
    x = pos[0] / 50
    # ignore flipped card
    if shown_cards[x] == True:
        return
    else:
        clicked_cards.append(x)
    # check card state
    if state == 0:
        state = 1
    elif state == 1:
        state = 2
    else:
        state = 1
        card0 = clicked_cards[0]
        card1 = clicked_cards[1]
        if cardlist[card0] != cardlist[card1]:
            shown_cards[card0] = False
            shown_cards[card1] = False 
        clicked_cards = [clicked_cards[-1]]
    if shown_cards[x] == False:
        shown_cards[x] = True
    if state == 2:
        turn += 1
        label.set_text("Turns = " + str(turn))
                       
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cardlist
    for x in range(0, 16):
        #if shown_cards[x]:
         #   canvas.draw_text(str(cardlist[x]), [x * 50 + 25, H / 1.4], 60, "white")
        if shown_cards[x] == True:
            canvas.draw_text(str(cardlist[x]), [x * 50 + 10, H / 1.4], 60, "white")
        else:
            canvas.draw_line([x * 50 + 25,0],[x * 50 + 25,100], 48, "blue")
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric