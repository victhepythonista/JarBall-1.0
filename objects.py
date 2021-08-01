import pygame
import pymunk
import random

gumball_colors =[
                    (100,50,50),
                    (0,200,50),
                    (150,150,10),
                ]
obstacle_images = {
        
        'beachball':'./data/images/obstacles/beachball.png',
        'platform':'./data/images/obstacles/platform.png',
        'spiked_platform':'./data/images/obstacles/spiked_platform.png'

        }
SAW_IMAGES = [
    './data/images/obstacles/saw.png',
    './data/images/obstacles/saw2.png',]

OBSTACLE_MAX_Y = 500
OBSTACLE_MIN_Y = 400
OBSTACLE_MAX_X = 700
OBSTACLE_MIN_X = -200

"""
 POINTS
 -rim +1
 -ricochet +2
 - jar +5
"""
class Pendulum:
    def __init__(self,space,joint_position,ball_position ,radius = 30, moment = 200, elasticity =1.2, friction = 1):
        self.b0 =space.static_body
        self.space = space
        self.body = pymunk.Body(100, moment,pymunk.Body.DYNAMIC)
        self.body.position = ball_position
        self.pendulum = pymunk.Circle(self.body, radius)
        self.pendulum.collision_type = 1
        self.pendulum.color = pygame.Color("green")
        self.pendulum.elasticity = elasticity
        self.pendulum.friction = friction
        self.joint_position = joint_position
        self.joint = pymunk.PinJoint(self.b0, self.body, joint_position)

        space.add(self.joint, self.body, self.pendulum)

    def cut(self):
        try:
            self.space.remove(self.joint)
        except:
            pass
    def destroy(self):
        to_be_removed =  self.body, self.pendulum  
        for item in to_be_removed:
            try:
                self.space.remove(item)
            except:
                pass

    @property
    def get_ball_pos(self):
        return self.pendulum.body.position

class GumBall:
    '''
    '''
    def __init__(self, body):
        self.body = body
        self.original_image = pygame.image.load('./data/images/first.png')
        self.angle = 30
        self.current_image =    None #pygame.transform.rotate(self.original_image,self.angle)
        self.color = 250,250,250,1 #random.choice(gumball_colors)
        self.radius = 31
        self.angle_cache  = 0
    @staticmethod
    def get_random_color():
        return random.choice(gumball_colors)

    def show(self, window, angle):
        pos = self.body.position
        image_pos = pos[0] - 31, pos[1] -31
        self.angle_cache -= angle
        if self.current_image == None:
            pygame.draw.circle(window, self.color,pos,self.radius, 0)
        else:
            self.current_image = pygame.transform.rotate(self.original_image,self.angle_cache)
            image = pygame.transform.rotate(self.original_image,angle)
            image_rect = self.current_image.get_rect(center = self.original_image.get_rect(center = pos).center)
            window.blit( self.current_image,image_rect)
class Jar:
    def __init__(self,  space  , x,y,w,h,d =5 , elasticity = .4, friction = 3, color = (240,240,240,1)):
        self.x = x
        self.y = y
        self.pos = x,y
        self.limit_x = self.x + w
        self.limit_y = self.y + h
        self.w = w
        self.h =h

        p1 = self.x,self.y
        p2 = self.x, self.y + h
        p3 = self.x + w, self.y +h
        p4 = self.x + w ,self.y
        points = p1,p2,p3,p4
        rim_points = [[(self.x,self.y),(self.x, self.y +10)],[(self.x + w, y), (self.x + w, self.y+10)]]
        self.space = space
        self.bodies = []
        self.segs = []
        body = space.static_body
        self.body = body
        # add the rims
        for point in rim_points:
            rim = pymunk.Segment(body,point[0],point[1],d)
            rim.collision_type = 3
            rim.elasticity = elasticity
            rim.color = color
            rim.friction = friction
            self.segs.append(rim)
            space.add(rim)

        # add the jar body
        for i in range(3):
            pa = points[i]
            pb = points[i + 1]
            self.bodies.append(body)
            seg = pymunk.Segment(body,pa,pb,d)
            seg.collision_type = 7
            self.segs.append(seg)
            seg.elasticity = elasticity
            seg.color = color
            seg.friction = friction
            space.add(seg)
    def destroy(self):
        for b in self.segs:
            try:
                self.space.remove(b)
            except:
                pass
class JarImage:
    def __init__(self):
        self.image = pygame.image.load('./data/images/jar.png')
    def show(self, window, pos):
        window.blit(self.image, pos)
class EnclosedBox:
    # AN ENCLOSED BOX
    def __init__(self,  space  , x,y,w,h,d =1, elasticity = .8, friction = .5, color = (20,20,20,1)):
        self.x = x
        self.y = y
        self.w = w
        self.h =h

        self.p1 = [self.x,self.y]
        self.p2 = [self.x + self.w,self.y]
        self.p3 = [self.x + self.w , self.y + self.h]
        self.p4 = [self.x , self.y + self.h]
        self.points = [self.p1,self.p2,self.p3,self.p4]
        self.d =d
        self.bodies = []
        self.space = space
        for i in range(4):
            pa = self.points[i]
            pb =  self.points[(i + 1)%4]
            body = space.static_body
            self.bodies.append(body)
            seg = pymunk.Segment(body,pa,pb,d)
            seg.collision_type = 2
            seg.elasticity = elasticity
            seg.color = color
            seg.friction = friction
            space.add(seg)
    def destroy(self):
        for b in self.bodies:
            try:
                self.space.remove(b)
            except:pass


class Obstacle:
    def __init__(self,pos, image,space):
        self.x = pos[0]
        self.y = pos[1]
        self.limit_y1 = OBSTACLE_MIN_Y
        self.limit_y2 = OBSTACLE_MAX_Y
        self.min_x = 0
        self.max_x = 500
        self.space = space
        self.bodies =[]
        self.shapes = []
        self.image = pygame.image.load(image) if image != None else None
    def show_image(self, window, pos):
        if self.image != None:
            window.blit(self.image, pos)
    def destroy(self):
        try:
            self.space.remove(self.shape)
            pass
        except:
            pass

class MovingSaw(Obstacle):
    ''' a rotating saw that moves left and right !!

    deafults:
        -radius = 20
        -speed = 4'''
    def __init__(self,  space, velocity = (0,10)):
        pos = 100,100
        Obstacle.__init__(self, pos, random.choice(SAW_IMAGES), space)
        self.radius = 25
        self.speed = 1
        self.x = random.randint(self.min_x, self.max_x)
        self.y = random.randint(self.limit_y1, self.limit_y2)

        self.velocity = velocity
        self.body = pymunk.Body( 100,  100, pymunk.Body.KINEMATIC)
        self.body.position = self.x,self.y
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = 4
        self.shape.velocity = velocity
        self.space.add(self.body, self.shape)
        self.shapes.append(self.shape)
        self.bodies.append(self.body)
        self.angle = 0
        self.original_image = self.image 
        self.image_rect = None
    def move(self):
        if self.x > OBSTACLE_MAX_X or self.x < OBSTACLE_MIN_X:
            self.speed = -self.speed
        self.x += self.speed
        self.body.position = self.x ,self.y
    def rotate(self):
        self.angle += 1
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.image_rect = self.image.get_rect(center = self.original_image.get_rect(center = self.body.position).center)
    def show(self,window):
        self.rotate()
        self.move()
        window.blit(self.image, self.image_rect)

 

class BeachBall(Obstacle):
    '''
    a simple moving beach ball on which the ball can bounce from
    '''
    def __init__(self,  space ,pos = (100,100), elasticity = 1, speed = 2):
        Obstacle.__init__(self, pos, obstacle_images['beachball'], space)
        self.radius = 40
        self.x = random.randrange(self.min_x, self.max_x, 100)
        self.y = random.randint(self.limit_y1, self.limit_y2)
        self.body = pymunk.Body( 100,  100, pymunk.Body.KINEMATIC)
        self.body.position =self.x,self.y
        self.shape = pymunk.Circle(self.body, self.radius) 
        self.shape.collision_type = 6
        self.shape.elasticity = elasticity
        self.speed = speed
        self.space.add(self.body, self.shape)
        self.shapes.append(self.shape)
        self.bodies.append(self.body)
    def move(self):
        if self.x > OBSTACLE_MAX_X- self.radius or self.x < OBSTACLE_MIN_X:
            self.speed = -self.speed
        self.x += self.speed
        self.body.position = self.x ,self.y

    def show(self,window):
        self.move()
        pos = self.body.position
        pos = pos[0] - (self.radius + 2), pos[1] - (2 + self.radius)
        window.blit(self.image, pos)


class Platform(Obstacle):
    '''
    a platform that moves left and right
        has no damage on the ball
        '''
    def __init__(self,  space ,pos = (100,100), elasticity = 1, speed = 2,image = obstacle_images['platform']):
        Obstacle.__init__(self, pos, image, space)
        self.width = 150
        self.height = 20
        self.x = random.randint(self.min_x, self.max_x)
        self.y = random.randint(self.limit_y1, self.limit_y2)

        self.body = pymunk.Body( 100,  100, pymunk.Body.KINEMATIC)
        self.body.position =self.x,self.y
        self.shape = pymunk.Poly.create_box(self.body,(self.width,self.height))
        self.shape.offset = 0,0
        self.shape.elasticity = elasticity
        self.speed = speed
        self.space.add(self.body, self.shape)
        self.shape.collision_type = 5
        self.shapes.append(self.shape)
        self.bodies.append(self.body)
        self.rect = pygame.Rect(self.x - self.width/2,self.y - self.height/2,self.width,self.height)
        self.image_pos = None
    def move(self):
        if self.x >= OBSTACLE_MAX_X :
            self.speed = -self.speed
        if self.x < OBSTACLE_MIN_X:
            self.speed = -self.speed
        self.x += self.speed
        self.body.position = self.x ,self.y
        self.rect.x = self.x - self.width/2
        self.rect.y = self.y - self.height/2
        self.image_pos = self.rect.x  , self.rect.y
    def show(self,window):
        self.move()
        self.show_image(window,self.image_pos)

class SpikedPlatform(Platform):
    def __init__(self,space):
        Platform.__init__(self,space,image = obstacle_images['spiked_platform'])
        self.shape.collision_type = 4
    def show_image(self,window):
        pos = self.image_pos
        im_pos = pos[0] -10,pos[1]-10
        window.blit(self.image, im_pos)

    def show(self, window):
        self.move()
        self.show_image(window )

 
class ObstacleManager:
    def __init__(self, space):
        self.obstacles = []
        self.space = space
    def clear(self):
        for obstacle in self.obstacles:
            try:
                obstacle.destroy()
                pass
            except:pass
        self.obstacles = []
    def new_obstacle(self,score):
        self.clear()
        pass
        obs = None
        '''
        0 > 20:
            # one obstacle platform or beachball

        50 > 80
            # two  obstacles - platform,beachball
        81 > 100
            # one saw
        100 > 200
            # one obstacle, one saw
        200 > infinity
            # two saws
        '''
        beginner_obstacles  = [Platform, BeachBall]
        begginer2_obstacles = [Platform, BeachBall]*10
        intermediate_obstacles = [MovingSaw,SpikedPlatform,Platform, BeachBall]
        advanced_obstacles = [MovingSaw,SpikedPlatform] * 30
        if score < 20:
            obs = random.choices(beginner_obstacles, k=random.choice([0,1]))
        elif score < 30:
            # just add a plattform or a beach ball
            obs = random.choices(beginner_obstacles, k=1)
        elif score < 50 :
            obs=  random.choices(begginer2_obstacles , k=2)

        elif score < 100:
            obs = random.choices(intermediate_obstacles, k=(random.randint(1,2)))
        elif score > 200:
            obs = random.choices(advanced_obstacles, k=2)
        if obs != None:
            self.add(obs )

    # add an obstacle to the list
    def add(self, obstacles):
        for obs in obstacles:
            self.obstacles.append(obs(self.space))

    # display the obstacles
    def show_obstacles(self, window):
        for obstacle in self.obstacles:
            obstacle.show(window)
