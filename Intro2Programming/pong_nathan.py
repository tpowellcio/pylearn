
####################################################################################################
# PASTE YOUR PYTHON CODE BELOW
####################################################################################################

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Mini-project 4:     PONG                                #
# Programmed by:      NATHAN ALGER                        #
#_________________________________________________________#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


import simplegui
import random

# 1. Initialize global variables
#---------------------------------------------------------#

WIDTH = 600
HEIGHT = 400
BALL_POS = [WIDTH / 2, HEIGHT / 2]
BALL_RADIUS = 20
PAD_WIDTH = 5
PAD_HEIGHT = 80
BALL_VEL = [-5, -2]
PAD1_TOP = HEIGHT / 2 - PAD_HEIGHT / 2
PAD2_TOP = HEIGHT / 2 - PAD_HEIGHT / 2
PAD1_VEL = 0
PAD2_VEL = 0
SCORE1 = 0
SCORE2 = 0
COLOR1 = '#2288ff'
COLOR2 = '#ff8822'
direc = 1
POINTS_TO_WIN = 9
GAME_OVER = False

# 2. Define helper functions
#---------------------------------------------------------#

def new_game():
    global PAD1_TOP, PAD2_TOP, SCORE1, SCORE2, GAME_OVER
    PAD1_TOP = HEIGHT / 2 - PAD_HEIGHT / 2
    PAD2_TOP = HEIGHT / 2 - PAD_HEIGHT / 2
    sound.pause()
    sound.rewind()
    sound.play()
    soundwin.pause()
    soundwin.rewind()
    SCORE1 = 0
    SCORE2 = 0
    spawn_ball()
    GAME_OVER = False
    timer.start()
    timer2.stop()
    timer2.start()

def midline(canvas):
    m = 0
    while m < HEIGHT:
        canvas.draw_line([WIDTH / 2, m],[WIDTH / 2, m+2], 3, "Gray")
        m += 4
        
def draw_paddles_and_gutters(canvas):
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 10, COLOR2)
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 10, COLOR1)
    canvas.draw_line([PAD_WIDTH, PAD1_TOP], [PAD_WIDTH, PAD1_TOP + PAD_HEIGHT], 10, COLOR1)
    canvas.draw_line([WIDTH - PAD_WIDTH, PAD2_TOP], [WIDTH - PAD_WIDTH, PAD2_TOP + PAD_HEIGHT], 10, COLOR2)
    
def draw_ball(canvas):
    canvas.draw_circle(BALL_POS, 20, 4, COLOR1, COLOR2)
    canvas.draw_circle(BALL_POS, 12, 4, COLOR1, COLOR2)
    canvas.draw_circle(BALL_POS, 4, 4, COLOR1, COLOR2)
    
def draw_score(canvas):
    canvas.draw_text(str(SCORE1), (WIDTH * 0.25, 50), 40, COLOR1, "sans-serif")
    canvas.draw_text(str(SCORE2), (WIDTH * 0.75, 50), 40, COLOR2, "sans-serif")
    
def update_ball():
    BALL_POS[0] += BALL_VEL[0]
    BALL_POS[1] += BALL_VEL[1]
    
    
def update_paddles():
    global PAD1_TOP, PAD2_TOP
    PAD1_TOP += PAD1_VEL
    PAD2_TOP += PAD2_VEL
    
def check_paddles():
    global PAD1_TOP, PAD2_TOP, PAD_HEIGHT
    if PAD1_TOP <= 0:
        PAD1_TOP = 0
    if PAD2_TOP <= 0:
        PAD2_TOP = 0
    if PAD1_TOP >= HEIGHT - PAD_HEIGHT:
        PAD1_TOP = HEIGHT - PAD_HEIGHT
    if PAD2_TOP >= HEIGHT - PAD_HEIGHT:
        PAD2_TOP = HEIGHT - PAD_HEIGHT
    
def check_collision():
    global SCORE1, SCORE2, direc
    # switch y velocity direction if hits top or bottom
    global BALL_POS, BALL_VEL, PAD1_TOP, PAD2_TOP
    if BALL_POS[1] <= 0 + BALL_RADIUS:
        BALL_VEL[1] = -BALL_VEL[1]
        sound_ping()
    if BALL_POS[1] >= HEIGHT - BALL_RADIUS:
        BALL_VEL[1] = -BALL_VEL[1]
        sound_ping()
    # switch x velocity direction if hits paddles
    if BALL_POS[0] <= 0 + BALL_RADIUS + PAD_WIDTH:
        if not((BALL_POS[1] >= PAD1_TOP - 10) and (BALL_POS[1] <= PAD1_TOP + PAD_HEIGHT + 10)):
            SCORE2 += 1
            sound_miss()
            spawn_ball()
        else:
            sound_pong()
        BALL_VEL[0] = -BALL_VEL[0]
        direc *= -1
        increase_vel()
    if BALL_POS[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        if not((BALL_POS[1] >= PAD2_TOP - 10) and (BALL_POS[1] <= PAD2_TOP + PAD_HEIGHT + 10)):
            SCORE1 += 1
            sound_miss()
            spawn_ball()
        else:
            sound_pong()
        BALL_VEL[0] = -BALL_VEL[0]
        direc *= -1
        increase_vel()
        
def spawn_ball():
    global BALL_POS, BALL_VEL
    BALL_POS = [WIDTH / 2, HEIGHT / 2]
    BALL_VEL = [direc, -dice()]

    
def dice():
    return random.randrange(1, 4)

def increase_vel():
    if BALL_VEL[0] < 0:
        BALL_VEL[0] -= 1
    elif BALL_VEL[0] > 0:
        BALL_VEL[0] += 1
        
def win_message1(canvas): 
    canvas.draw_text('PLAYER 1 WINS', (WIDTH * 0.25, 200), 40, COLOR1, 'sans-serif')
    
def win_message2(canvas):    
    canvas.draw_text('PLAYER 2 WINS', (WIDTH * 0.25, 200), 40, COLOR2, 'sans-serif')  

def sound_ping():
    sound2.rewind()
    sound2.play()

def sound_pong():
    sound3.rewind()
    sound3.play()

def sound_miss():
    sound4.rewind()
    sound4.play()
    
def sound_win():
    soundwin.rewind()
    soundwin.play()
    sound.pause()    
    
    
# 3. Define classes
#---------------------------------------------------------#


# 4. Define event handlers
#---------------------------------------------------------#

def oodles_of_doodles(canvas):
    global GAME_OVER
    if not(GAME_OVER): 
        draw_score(canvas)    
        midline(canvas)
        draw_paddles_and_gutters(canvas)
        update_paddles()
        check_paddles()
        draw_ball(canvas)
        update_ball()
        check_collision()
    else:
        draw_score(canvas)    
        midline(canvas)
    if POINTS_TO_WIN == SCORE1:
        GAME_OVER = True
        win_message1(canvas)
    elif POINTS_TO_WIN == SCORE2:
        GAME_OVER = True
        win_message2(canvas)


    
def keydown(key):
    global PAD1_VEL, PAD2_VEL
    
    if key == simplegui.KEY_MAP["up"]:
        PAD2_VEL = -5
    elif key == simplegui.KEY_MAP["down"]:
        PAD2_VEL = 5
    elif key == simplegui.KEY_MAP["w"]:
        PAD1_VEL = -5
    elif key == simplegui.KEY_MAP["s"]:
        PAD1_VEL = 5  
   
def keyup(key):
    global PAD1_VEL, PAD2_VEL
    
    if key == simplegui.KEY_MAP["up"]:
        PAD2_VEL = 0
    elif key == simplegui.KEY_MAP["down"]:
        PAD2_VEL = 0
    elif key == simplegui.KEY_MAP["w"]:
        PAD1_VEL = 0
    elif key == simplegui.KEY_MAP["s"]:
        PAD1_VEL = 0 
        
def button():
    new_game()
   
def loop():
    sound.rewind()
    sound.play()

# 5. Create frame
#---------------------------------------------------------#

frame = simplegui.create_frame('PING-PONG', WIDTH, HEIGHT, 120)

def timer_handler():
    if GAME_OVER:
        timer.stop()
        sound_win()

timer = simplegui.create_timer(100, timer_handler)

timer2 = simplegui.create_timer(140000, loop)
timer2.start()




# 6. Register event handlers
#---------------------------------------------------------#

frame.set_draw_handler(oodles_of_doodles)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
sound = simplegui.load_sound("http://mariomedia.net/music/Nintendo%20Gamecube/Luigi's%20Mansion/082%20-%20Kazumi%20Totaka%3B%20Shinobu%20Tanaka%20-%20Staff%20Credits.mp3")
sound.set_volume(0.7)
sound2 = simplegui.load_sound("http://themushroomkingdom.net/sounds/wav/smb/smb_fireball.wav")
sound2.set_volume(1.0)
sound3 = simplegui.load_sound("http://themushroomkingdom.net/sounds/wav/smb/smb_kick.wav")
sound3.set_volume(0.7)
sound4 = simplegui.load_sound("http://themushroomkingdom.net/sounds/wav/smb/smb_fireworks.wav")
sound4.set_volume(0.7)
soundwin = simplegui.load_sound("http://mariomedia.net/music/Super%20Nintendo%20Entertainment%20System/Chrono%20Trigger/20%20-%20Fanfare%201.mp3")

RESTART = frame.add_button('RESTART', button,120)


# 7. Start frame and timers
#---------------------------------------------------------#
frame.start()
new_game()
sound.play()

####################################################################################################
# PASTE YOUR PYTHON CODE ABOVE
####################################################################################################
