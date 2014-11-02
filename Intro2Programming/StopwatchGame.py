# "Stopwatch: The Game"

import simplegui

# define global variables

running = False
count = 0
wins = 0
attempts = 0
message = ""
color = "White"

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global color
    tenths = t % 10
    seconds = t / 10
    minutes = t / 600
    if minutes > 0:
         minutes = minutes % 60
    if seconds > 0:
        seconds = seconds % 60     
    
    if minutes > 0:
        color = "Red"    
    elif (seconds <= 9) and (seconds > 0):
        color = "Blue"
    elif (seconds >= 10) and (seconds < 30):
        color = "Green"
    elif (seconds >= 30) and (seconds < 50):
        color = "Yellow"
    elif (seconds >= 50) and (minutes <= 0):
        color = "Orange"
    else:
        color = "White"

    return str(minutes) + ":" + ("00" + str(seconds))[-2:] + "." + str(tenths)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
# Handler for start button
def on_start():
    global running
    if not(running):
        if not(running):
            running = True
            timer.start()

# handler for stop button
def on_stop():
    global running
    if running:
        running = False
        timer.stop()
        score()    
    
# handler for reset button
def on_reset():
    global count, message, wins, attempts
    timer.stop()
    wins = 0
    attempts = 0
    count = 0
    message = format(count)
    
# Update Score
def score():
    global wins, attempts
    attempts += 1
    if not(running):
        on_try = format(count)
        if (on_try[-1:] == "0"): 
            wins += 1

# Scoreboard format
def score_board():
    global wins, attempts
    return str(wins) + " / " + str(attempts)
            
# define event handler for timer with 0.1 sec interval
# handler for timer
def tick():
    global count, message
    count += 1
    message = format(count)
    
timer = simplegui.create_timer(100, tick)

# define draw handler
def draw_handler(canvas):
    global message, count, wins, attempts
    message = format(count)
    canvas.draw_text(message, [90,130], 50, color)
    canvas.draw_text(score_board(), [130,20], 20, "White")
    canvas.draw_line((0, 30), (300, 30), 5, 'Grey')
    
# create frame
frame = simplegui.create_frame('Stopwatch - the Game', 300, 200)
frame.set_draw_handler(draw_handler)

# register event handlers
btn_start = frame.add_button('Start', on_start, 200)
btn_stop = frame.add_button('Stop', on_stop, 200)
btn_reset = frame.add_button('Reset', on_reset, 200)

# start frame
frame.start()

# Please remember to review the grading rubric
