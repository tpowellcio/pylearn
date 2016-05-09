# implementation of card game - Memory

import simplegui
import random

canvas_width = 800
canvas_height = 100
card_width = canvas_width / 16
card_height = canvas_height
card_pos = 0
num_cards = canvas_width / card_width
card_dict = {}
card_num = range(num_cards / 2) + range(num_cards / 2)
card_state = {}

# helper function to initialize globals
def new_game():
    global state, card_pos, card_num
    state = 0
    card_pos = 0
    
    #shuffle cards
    random.shuffle(card_num)
    
   #layout cards face down
    for i in range(0,num_cards):
        card_dict[card_pos] = card_num[i]
        card_state[card_pos] = 0
        card_pos += card_width

# define event handlers
def mouseclick(pos):
    global card_state
    # add game state logic here
    for card in card_dict:
        if (pos[0] > card) and (pos[0] < (card + card_width)):
            if card_state[card] == 0:
                card_state[card] = 1
            elif card_state[card] == 1:
                card_state[card] = 2
            else:
                card_state[card] = 1
            print card_state[card]
                       
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global card_pos, card_state
    for card in list(card_dict.keys()):
        if (card_state[card] == 1) or (card_state[card] == 2):
            canvas.draw_text(str(card_dict[card]),[card + card_width / 5, canvas_height / 1.4], 60, "White")
        else:
            canvas.draw_line([card + card_width / 2,0],[card + card_width / 2,canvas_height],card_width - 1,"blue")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", canvas_width, canvas_height)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric