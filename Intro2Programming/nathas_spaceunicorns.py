
"""
SPACE UNICORN LYRICS
CREDIT TO PARRY GRIPP FOR BG MUSIC

Space unicorn
Soaring through the stars
Delivering the rainbows all around the world

Space unicorn
Shining in the night
Smiles and hugs forever
All around the world

So pure of heart
And strong of mind
So true of aim with his marshmallow laser
Marshmallow laser

Space unicorn
Soaring through the stars
Delivering the rainbows all around the world

Delivering the rainbows
Delivering the rainbows
Delivering the rainbows all around the world
Delivering the rainbows all around the world
All around the world
All around the world
All around the world
All around the world
Muffins are amazing!!!!!
Happiness is awesome!!!!
"""
import simplegui
import math
import random


WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
collision = False

CONTROLS = {
    "left": simplegui.KEY_MAP["left"],
    "right": simplegui.KEY_MAP["right"],
    "up": simplegui.KEY_MAP["up"],
    "down": simplegui.KEY_MAP["down"],
    "space": simplegui.KEY_MAP["space"]
}

###IMAGES DRAWN BY NATHAN AND DAVID ALGER###
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

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

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://nathanalger.com/images/color_dots.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://nathanalger.com/images/bg.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://nathanalger.com/images/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_info_thrust = ImageInfo([135, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://nathanalger.com/images/ship.png")

unicorn_info =  ImageInfo([53, 40], [106, 79], 35)
unicorn_image = simplegui.load_image("http://nathanalger.com/images/unicorn.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([10,10], [20, 20], 3, 50)
missile_image = simplegui.load_image("http://nathanalger.com/images/bullet.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://nathanalger.com/images/rock.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://www.parrygripp.com/wimpy/Space%20Unicorn.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")



def new_game():
    global my_ship, missile_group, rock_group, explosion_group
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    missile_group = set([])
    rock_group = set([])
    explosion_group = set([])

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def process_sprite_group(canvas, group):
    for item in set(group):
        item.draw(canvas)
        if item.update():
            group.remove(item)
        if item.age > item.lifespan:
            explosion_group.remove(item)

#rock - ship helper function
def group_collide(group, other_object):
    global explosion_group
    coll = False
    copygroup = set(group)
    for item in copygroup:
        if item.collide(other_object) == True:
            group.remove(item)
            coll = True
            explosion_group.add(Sprite(item.get_position(), [0, 0], 0, 0, explosion_image1, explosion_info, explosion_sound))
    return coll

#missile - rock helper function
def group_group_collide(group1, group2):
    colls = 0
    for i in set(group1):
        if group_collide(group2, i) == True:
            group2.discard(i)
            group1.discard(i)
            colls += 1
    return colls


class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0

    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        if self.animated == True:
            current_ship_index = (self.age % 24) // 1
            current_ship_center = [self.image_center[0] +  current_ship_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_ship_center, self.image_size, self.pos, self.image_size)
            self.age += 1

    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .12
            self.vel[1] += acc[1] * .12

        self.vel[0] *= .99
        self.vel[1] *= .99

        if self.age > self.lifespan:
            self.animated = False

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def increment_angle_vel(self):
        self.angle_vel += .07

    def decrement_angle_vel(self):
        self.angle_vel -= .07

    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

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
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if self.animated == True:
            current_rock_index = (self.age % 24) // 1
            current_rock_center = [self.image_center[0] +  current_rock_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_rock_center, self.image_size, self.pos, self.image_size)
            self.age += 1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def update(self):
        # update angle
        self.age += 1
        self.angle += self.angle_vel
        life = False
        if self.age >= self.lifespan:
            life = True
            return life

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

    def collide(self, other_object):
        global collision
        collision = False
        if dist(self.pos, other_object.get_position()) <= (self.radius + other_object.get_radius()):
            collision = True
        return collision


# key handlers to control the ship
def keydown(key):
    if key == CONTROLS["left"]:
        my_ship.decrement_angle_vel()
    elif key == CONTROLS["right"]:
        my_ship.increment_angle_vel()
    elif key == CONTROLS["up"]:
        my_ship.set_thrust(True)
    elif key == CONTROLS["space"]:
        my_ship.shoot()
def keyup(key):
    if key == CONTROLS["left"]:
        my_ship.increment_angle_vel()
    elif key == CONTROLS["right"]:
        my_ship.decrement_angle_vel()
    elif key == CONTROLS["up"]:
        my_ship.set_thrust(False)

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0

# draw handler
def draw(canvas):
    global time, started, score, lives

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_image(unicorn_image, [53,40], [106,79], [30,45], [50,50])
    canvas.draw_text('x '+str(lives), (65, 60), 30, 'rgba(0,0,0,0.5)', 'sans-serif')
    canvas.draw_text('Score: '+str(score), (660, 40), 20, 'rgba(0,0,0,0.5)', 'sans-serif')


    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas, missile_group)
    if started:
        process_sprite_group(canvas, rock_group)

    # update ship and sprites
    my_ship.update()

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

    if group_collide(rock_group, my_ship) == True:
        explosion_group.add(Ship(my_ship.get_position(), [0, 0], 0, explosion_image2, explosion_info))
        lives -= 1

    score += group_group_collide(missile_group, rock_group)

    if lives == 0:
        for rock in rock_group:
            rock_group.discard(rock)
        started = False
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

    if started == True:
        soundtrack.play()
    else:
        soundtrack.pause()
        soundtrack.rewind()

    # draw explosions
    process_sprite_group(canvas, explosion_group)

# timer handler that spawns a rock
def rock_spawner():
    global rock_group, my_ship, score

    if started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
        if len(rock_group) < 12:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            acc = .6 + score*.1
            rock_vel = [random.random() * acc - .3, random.random() * acc - .3]
            rock_avel = random.random() * .2 - .1
            a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
            if dist(rock_pos, my_ship.get_position()) > (a_rock.get_radius() + my_ship.get_radius()) + 20:
                rock_group.add(a_rock)


frame = simplegui.create_frame("Space Unicorn", WIDTH, HEIGHT,180)

frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.set_canvas_background('white')
frame.add_label('Use the arrow keys to move and the space bar to shoot marshmallows!')
frame.add_label('')
stlbl = frame.add_label('Click over there to start...')
timer = simplegui.create_timer(1000, rock_spawner)

timer.start()
frame.start()
new_game()
