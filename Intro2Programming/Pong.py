# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
pad1_pos = HEIGHT / 2 - PAD_HEIGHT / 2
pad2_pos = HEIGHT / 2 - PAD_HEIGHT / 2
pad1_vel = 0
pad2_vel = 0
score1 = 0
score2 = 0
ball_colour = "White"


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(player):
    global ball_pos, ball_vel, ball_colour # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    vector = random.randrange(1, 3)
    if player == 1:
        direction = random.randrange(-2, 0)
    else:
        direction = random.randrange(1, 3)
    if vector == 1:
        vector = random.randrange(1, 3)
    else:
        vector = random.randrange(-2, 0)      
    ball_vel = [direction, vector]
    ball_colour = "White"
    
def increase_speed():
    global ball_vel
    if ball_vel[0] < 0:
        ball_vel[0] -= 1
    elif ball_vel[0] > 0:
        ball_vel[0] += 1
        
# define event handlers
def new_game():
    global pad1_pos, pad2_pos, pad1_vel, pad2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    pad1_pos = HEIGHT / 2 - PAD_HEIGHT / 2
    pad2_pos = HEIGHT / 2 - PAD_HEIGHT / 2
    pad1_vel = 0
    pad1_vel = 0
    
    spawn_ball(random.randrange(1, 3))

def draw(canvas):
    global score1, score2, pad1_pos, pad2_pos, ball_pos, ball_vel, ball_colour
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # wall bounce
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1] 
        
    # pad bounce    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ((ball_pos[1] >= pad1_pos) and (ball_pos[1] <= pad1_pos + PAD_HEIGHT)):
            ball_vel[0] = - ball_vel[0]
            increase_speed()
            ball_colour = "Yellow"
        else:
            score2 += 1
            spawn_ball(2)
                      
    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        if ((ball_pos[1] >= pad2_pos) and (ball_pos[1] <= pad2_pos + PAD_HEIGHT)):
            ball_vel[0] = - ball_vel[0]
            increase_speed()
            ball_colour = "Blue"
        else:
            score1 += 1
            spawn_ball(1)
            
                    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", ball_colour)
    
    # update paddle's vertical position, keep paddle on the screen
    pad1_pos += pad1_vel
    pad2_pos += pad2_vel  
    
    if pad1_pos <= 0:
        pad1_pos = 0
    if pad2_pos <= 0:
        pad2_pos = 0
    if pad1_pos >= HEIGHT - PAD_HEIGHT:
        pad1_pos = HEIGHT - PAD_HEIGHT
    if pad2_pos >= HEIGHT - PAD_HEIGHT:
        pad2_pos = HEIGHT - PAD_HEIGHT
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, pad1_pos], [HALF_PAD_WIDTH, pad1_pos + PAD_HEIGHT], PAD_WIDTH, "Yellow")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, pad2_pos], [WIDTH - HALF_PAD_WIDTH, pad2_pos + PAD_HEIGHT], PAD_WIDTH, "Blue")
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH * 0.25, 50), 40, "yellow")
    canvas.draw_text(str(score2), (WIDTH * 0.75, 50), 40, "blue")
 
def keydown(key):
    global pad1_vel, pad2_vel
    pad_acc = 5
    if key == simplegui.KEY_MAP["w"]:
        pad1_vel -= pad_acc
    elif key == simplegui.KEY_MAP["s"]:
        pad1_vel += pad_acc
    elif key == simplegui.KEY_MAP["up"]:
        pad2_vel -= pad_acc
    elif key == simplegui.KEY_MAP["down"]:
        pad2_vel += pad_acc
        
def keyup(key):
    global pad1_vel, pad2_vel
    pad_acc = 5
    if key == simplegui.KEY_MAP["w"]:
        pad1_vel += pad_acc
    elif key == simplegui.KEY_MAP["s"]:
        pad1_vel -= pad_acc
    elif key == simplegui.KEY_MAP["up"]:
        pad2_vel += pad_acc
    elif key == simplegui.KEY_MAP["down"]:
        pad2_vel -= pad_acc

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart Game', new_game, 200)


# start frame
new_game()
frame.start()
