############################################################
# Project 3 - Stopwatch: The Game
############################################################
# Name:   Dave Alger
# Date:   8 OCT 2014
# Follow: https://twitter.com/DaveAlger
############################################################

import simplegui
import time

############################################################
# 1. Initialize global variables
############################################################
counter = 0
is_running = False
attempts = 0
wins = 0


############################################################
# 2. Define helper functions
############################################################
def format(t):
    """
    converts time in tenths of seconds into 
    formatted string A:BC.D
    """
    minutes = t / 600
    if minutes > 0:
        t -= minutes * 600
    seconds = t / 10
    if seconds > 0:
        t -= seconds * 10
    tenths = t
    return str(minutes) + ":" + ("00"+str(seconds))[-2:] + "." + str(tenths)
    
def get_score():
    """
    returns a formatted string representing the score
    """
    return str(wins) + "/" + str(attempts)
    
def update_score():
    global attempts
    global wins
    t = format(counter)
    attempts += 1
    if (t[-1:] == "0"):
        wins += 1
    
def update_controls():
    if not(is_running):
        update_score()

############################################################
# 3. Define classes
############################################################


############################################################
# 4. Define event handlers
############################################################
def on_draw(canvas):
    # update timer
    t = format(counter)
    canvas.draw_text(t, [44,126], 64, "#ffffff", "monospace")
    
    # update score
    canvas.draw_line([0, 0], [300, 0], 50, "#444444")
    canvas.draw_line([0, 26], [300, 26], 1, "#cccccc")
    canvas.draw_text(get_score(), [150, 18], 18, "#cccccc", "monospace")
    
    # set background to green when tenths digit = 0
    if (counter > 0) and (t[-1:] == "0"):
        frame.set_canvas_background("#009900")
    else:
        frame.set_canvas_background("#222222")

def on_kirby():
    global is_running
    is_running = not(is_running)
    update_controls()

def on_start():
    global is_running
    if not(is_running):
        is_running = True
        update_controls()
    
def on_stop():
    global is_running
    if is_running:
        is_running = False
        update_controls()
    
def on_reset():
    global counter
    global is_running
    global attempts
    global wins
    counter = 0
    is_running = False
    attempts = 0
    wins = 0
    btn_kirby.set_text("^(' - ')^")
    
def on_tick():
    global counter
    if (is_running):
        counter += 1
        t = int(format(counter)[-1:])
        if t == 0:
           btn_kirby.set_text("^(' - ')^")
        elif t <= 3:
           btn_kirby.set_text("(>'-')>")
        elif t <= 5:
           btn_kirby.set_text("<('-'<)")
        elif t <= 7:
           btn_kirby.set_text("(>'-')>")
        else:
           btn_kirby.set_text("<('-'<)")


############################################################
# 5. Create frame
############################################################
frame = simplegui.create_frame("Stopwatch", 300, 200, 150)


############################################################
# 6. Register event handlers
############################################################
frame.set_draw_handler(on_draw)
btn_start = frame.add_button("Start", on_start, 150)
btn_stop = frame.add_button("Stop", on_stop, 150)
btn_reset = frame.add_button("Reset", on_reset, 150)
frame.add_label("___________________")
frame.add_label("")
btn_kirby = frame.add_button("^(' - ')^", on_kirby, 150)
frame.add_label("___________________")

tick = simplegui.create_timer(100, on_tick)


############################################################
# 7. Start frame and timers
############################################################
frame.start()
tick.start()

