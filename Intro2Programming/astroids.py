'''
Hi, my name is Andrew.  Thank you for grading my project.  

I added a lot of features and tweaks that I thought it needed.   I'm and old guy and
I remember this game when it was new in the arcade.  I wanted the project to be as faithful 
to that version as possible.   Sorry, no aliens, but you do get an extra life at 10,000 points
as well as become the hi score holder..  Sometimes it takes a while to respawn if there are a 
lot of rocks in the center.  It will eventually spawn when it's safe.  There is a bug in my 
implementation, can you find it?   I made the little asteroids blend in with the background 
on purpose to make it harder.

'''



# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
high_score = 10000
lives = 3
time = 0
explosion_time = 0
started = False
bonus_flag = False
beep_count = 0

SAFETY_FACTOR = 6
DIFF_ADJ = 0
FRICTION_COEF = .99

class ImageInfo:
    def __init__(self, center, size, radius = 0, draw_size = None, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
        self.draw_size = draw_size

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
    def get_draw_size(self):
        return self.draw_size

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480], 0, [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
#nebula_info = ImageInfo([400, 300], [800, 600], 0, [800, 600])
#nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

nebula_info = ImageInfo([512, 384], [1024, 768], 0, [800, 600])
nebula_image = simplegui.load_image("http://dl.dropbox.com/s/6pg28rt2lrxhzge/Cosmos03.jpg")


    
    
    
# splash image
splash_info = ImageInfo([200, 150], [400, 300], 0, [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], (35 * .5), [90 * .5, 90 * .5])
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, [10, 10], 150)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40, [90, 90])
med_asteroid_info = ImageInfo([45, 45], [90, 90], 27, [60, 60])
small_asteroid_info = ImageInfo([45, 45], [90, 90], 13, [30, 30])
asteroid_image_blue = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image_brown = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid_image_blend = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, [90, 90], 24, True)
explosion_med_info = ImageInfo([64, 64], [128, 128], 17, [60, 60], 24, True)
explosion_small_info = ImageInfo([64, 64], [128, 128], 17, [30, 30], 24, True)

explosion_image_alpha = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image_orange = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
explosion_image_blue = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")
explosion_image_blue2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")


EXPLOSION_CENTER = [50, 50]
EXPLOSION_SIZE = [100, 100]
EXPLOSION_DIM = [9, 9]
ship_explosion_info = ImageInfo([50, 50], [100,100], 17, [128,128], 82, True)
ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")




# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(.6)
#missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound = simplegui.load_sound("https://dl.dropbox.com/s/2fnggi606b8pjvx/fire.mp3")
missile_sound.set_volume(.4)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
#ship_thrust_sound = simplegui.load_sound("https://dl.dropbox.com/s/9j3f5hw0o17hwge/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound_small = simplegui.load_sound("http://dl.dropbox.com/s/kkjbmvlueqyzc2z/bangSmall.mp3")
explosion_sound_med = simplegui.load_sound("http://dl.dropbox.com/s/znmalqwlvnhs0bu/bangMedium.mp3")
explosion_sound_large = simplegui.load_sound("http://dl.dropbox.com/s/m3dk3ey2gdyzqsy/bangLarge.mp3")

beep_sound = simplegui.load_sound("http://dl.dropbox.com/s/hffbxou26ai20ri/extraShip.mp3")
beep_sound.set_volume(.3)


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.destruct = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.tracker = [pos[0], pos[1]]
        self.draw_size = info.get_draw_size()
        
    def draw(self,canvas):
        global my_ship
        if self.destruct:
            pass
        elif self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.draw_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.draw_size, self.angle)

        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT


        # update velocity
        if self.thrust and not self.destruct:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .12
            self.vel[1] += acc[1] * .12
            
            
            
        self.vel[0] *= FRICTION_COEF
        self.vel[1] *= FRICTION_COEF
        self.tracker[0] += self.vel[0]
        self.tracker[1] += self.vel[1]


    def set_thrust(self, on):
        self.thrust = on
        if on and not self.destruct:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global a_missile
        if len(missile_group) < 6 and not self.destruct:         
            forward = angle_to_vector(self.angle)
            missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
            missile_vel = [(self.vel[0]/2) + 2 * forward[0], (self.vel[1]/2) + 2 * forward[1]]
            missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    
    def reset_ship(self):
        global my_ship
        self.pos = [WIDTH / 2, HEIGHT / 2]
        self.vel = [0, 0]
        self.angle = math.pi * 1.5
        my_ship.angle_vel = 0       
        explosion_time = 0  
        too_close = False
        for rock in rock_group:
            if dist(rock.pos, self.pos) < self.radius * SAFETY_FACTOR:
                too_close = True

        if too_close == True:
            timer.start()
        elif too_close == False: 
            timer.stop()
            my_ship.destruct = False
            my_ship.angle_vel = 0
           
            
            
            
            
            
            
            
            
            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.draw_size = info.get_draw_size()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        global explosion_time
        if self.animated and my_ship.destruct == True:
            explosion_index = [explosion_time % EXPLOSION_DIM[0], (explosion_time // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
            canvas.draw_image(ship_explosion_image, 
            [EXPLOSION_CENTER[0] + explosion_index[0] * EXPLOSION_SIZE[0], 
            EXPLOSION_CENTER[1] + explosion_index[1] * EXPLOSION_SIZE[1]], 
            EXPLOSION_SIZE, my_ship.pos, my_ship.draw_size)
            explosion_time += 1
            if explosion_time >= 54:
                explosion_time = 0
                my_ship.reset_ship()
        elif self.animated: 
            center = self.image_center[0]
            explosion_index = self.image_size[0] * self.age
            center += explosion_index
            canvas.draw_image(self.image, [center, self.image_center[1]], self.image_size, self.pos, self.draw_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
            self.pos, self.draw_size, self.angle)

                    
            
            
            
            
        
    
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        
        if self.age > self.lifespan:
            return True
        return False

    
    
    
    
    
    def collide(self, other_object):        
        a = dist(self.pos, other_object.pos)
        b = self.radius + other_object.radius
        if a < b:
            return True
        return False


    
    
    
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        reset_game()

def reset_game():
    global started, lives, score, my_ship, DIFF_ADJ
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    started = True
    my_ship.destruct = False
    lives = 3
    score = 0
    DIFF_ADJ = 0
    bonus_flag = False
    soundtrack.rewind()
    soundtrack.play()
    reset_level()
    my_ship.reset_ship()
    
def reset_level():
    global DIFF_ADJ
    DIFF_ADJ += 1
    #timer.stop()
    for i in range(4):
        rock_spawner(None)      

        
        
        
def draw(canvas):
    global time, started, lives, score, rock_group, my_ship, high_score, bonus_flag
    center = debris_info.get_center()
    size = [debris_info.get_size()[0] * .75, debris_info.get_size()[1] * .75]

    nebula_map = [ ((WIDTH / 2 ) - (my_ship.tracker[0] / 100)) % WIDTH, ((HEIGHT / 2) - (my_ship.tracker[1] / 100)) % HEIGHT ]
    canvas.draw_image(nebula_image, nebula_info.get_center(), [800, 600], nebula_map, [1024, 768])
#   canvas.draw_image(image,          center_source,        width_height_source,center_destwidth_height_dest, rotation)
    #nebula_info = ImageInfo([512, 384], [800, 600], 0, [800, 600])

#   canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest, rotation)    
    tracker = [ (((WIDTH / 2 ) - (my_ship.tracker[0] / 5)) % WIDTH) + 200, ((HEIGHT / 2) - (my_ship.tracker[1] / 5)) % HEIGHT ]
    trackers = screen_wrap(tracker)
    for pos in trackers:
        canvas.draw_image(debris_image, center, size, [pos[0], pos[1]], [WIDTH, HEIGHT])



    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    canvas.draw_text("Hi Score", [340, 50], 22, "White")
    canvas.draw_text(str(high_score), [340, 80], 22, "White")
    
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    if group_group_collide(missile_group, rock_group):
        pass
    
    if group_collide(rock_group, my_ship):
        lives -= 1
        explosion_creator(my_ship)
        my_ship.destruct = True 
        ship_thrust_sound.rewind()

    if score > high_score:
        high_score = score        

    if not bonus_flag and score > 10000:
        bonus_flag = True
        lives += 1
        bonus_timer.start()
        
        
    if lives <= 0:
        started = False

        
        
           
    if len(rock_group) == 0 and started == True:
        reset_level()

        pass

        
    # draw splash screen if not started
    if not started:
        rock_group = set()
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        

def screen_wrap(position):
# Handles screen wrap math.  Is called by the draw functions of all moving objects
    
    screen_wrap_effect = [[position[0], position[1]],
    [position[0] + WIDTH, position[1]],
    [position[0] - WIDTH, position[1]],
    [position[0], position[1] + HEIGHT],
    [position[0], position[1] - HEIGHT],
    [position[0] + WIDTH, position[1] + HEIGHT],
    [position[0] - WIDTH, position[1] + HEIGHT],
    [position[0] + WIDTH, position[1] - HEIGHT],
    [position[0] - WIDTH, position[1] - HEIGHT] ]
        
    return screen_wrap_effect       
        
def process_sprite_group(a_set, canvas): 
    for item in set(a_set):
        item.draw(canvas)
        item.update()
        if item.update():
            a_set.discard(item)
      
def group_collide(group, other_object):
    if my_ship.destruct == True:
        return False
    else:
        for item in set(group):
            if item.collide(other_object):
                score_keeper(item)
                animation = random.choice([explosion_image_alpha, explosion_image_orange, explosion_image_blue, explosion_image_blue2])
                if item.draw_size == asteroid_info.draw_size:
                    explosion_group.add(Sprite(item.pos, item.vel, 0, 0, animation, explosion_info, explosion_sound_large))
                    rock_spawner(item)
                    rock_spawner(item)
                    group.remove(item)
                elif item.draw_size == med_asteroid_info.get_draw_size():
                    explosion_group.add(Sprite(item.pos, item.vel, 0, 0, animation, explosion_med_info, explosion_sound_med))
                    rock_spawner(item)
                    rock_spawner(item)
                    group.remove(item)
                elif item.draw_size == small_asteroid_info.get_draw_size():
                    explosion_group.add(Sprite(item.pos, item.vel, 0, 0, animation, explosion_small_info, explosion_sound_small))
                    group.remove(item)

                return True

        return False
    
def group_group_collide(a_group, another_group): 
    for item in set(a_group):
        if group_collide(another_group, item):
            a_group.discard(item)
            return True
    return False


            
def explosion_creator(item):
    if item == my_ship:
        animation = ship_explosion_image
        info = ship_explosion_info
        ship_explosion = Sprite(item.pos, item.vel, 0, 0, animation, info, explosion_sound_large)
        explosion_group.add(ship_explosion)
    else:
        animation = random.choice([explosion_image_alpha, explosion_image_orange, explosion_image_blue, explosion_image_blue2])
        explosion = Sprite(item.pos, item.vel, 0, 0, animation, explosion_info, explosion_sound_large)
        
        explosion_group.add(explosion)

def score_keeper(item): 
    global score
    if item.draw_size == asteroid_info.draw_size:
        score += 20
    elif item.draw_size == med_asteroid_info.draw_size:
        score += 50
    elif item.draw_size == small_asteroid_info.draw_size:
        score += 100

def bonus_sound():
    global beep_count
    if beep_count > 32:
        bonus_timer.stop()
        beep_count = 0
    else:
        beep_count += 1
        beep_sound.rewind()
        beep_sound.play()

        
        
        
        
def rock_spawner(parent):
    if started == True:
        random_pos = [random.random() * WIDTH, random.random() * HEIGHT]
        while dist(random_pos, my_ship.pos) < my_ship.radius * SAFETY_FACTOR:
            random_pos = [random.random() * WIDTH, random.random() * HEIGHT]
    
        random_velocity = [0, 0]
        random_velocity = [(random.random() * .6 - .3) * (1 + DIFF_ADJ), (random.random() * .6 - .3) * (1 + DIFF_ADJ)]
        random_angle = random.random() * 2 * math.pi
        random_angular_velocity = random.random() * (.01 +.002) * random.choice([-1, 1])
        asteroid_image = random.choice([asteroid_image_blue, asteroid_image_brown, asteroid_image_blend])
        if parent == None:
            a_rock = Sprite(random_pos, random_velocity, random_angle, random_angular_velocity, asteroid_image_blend, asteroid_info, sound = None)
        elif parent.draw_size == asteroid_info.draw_size: 
            a_rock = Sprite(parent.pos, random_velocity, random_angle, random_angular_velocity, asteroid_image_brown, med_asteroid_info, sound = None)
        elif parent.draw_size == med_asteroid_info.draw_size: 
            a_rock = Sprite(parent.pos, random_velocity, random_angle, random_angular_velocity, asteroid_image_blue, small_asteroid_info, sound = None)
        rock_group.add(a_rock)
                            
def rock_breaks_apart(a_rock):
    rock_avel = random.random() * .2 - .1
    
    new_rock = Sprite(a_rock.pos, a_rock.vel, 0, rock_avel, asteroid_image, asteroid_info)
    rock_group.add(a_rock)
    #a rock breaks into two rocks of the next smaller size
    pass






# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(300.0, my_ship.reset_ship)

bonus_timer = simplegui.create_timer(25.0, bonus_sound)


# get things rolling
#timer.start()
frame.start()
