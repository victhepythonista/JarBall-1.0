import pygame
import random
from tools import write_on_screen


class Animation:
    ''' displays the message on to a screen for a limited period before 'dying' '''
    def  __init__(self, message, position,time_limit = 100, font_size = 20, color = (45,45,45), sound_name = ''):
        self.font_size = font_size
        self.color = color
        self.position = position
        self.timer = 0
        self.time_limit = time_limit
        self.message = message
        self.dead = False
        self.sound_name = sound_name
    def show(self, window):
        self.timer += 1
        if self.timer >= self.time_limit:
            self.dead = True
        write_on_screen(self.message, self.position, window, self.color, self.font_size)
class InfoAnimation(Animation):
    '''
    for displaying basic sentence animations
    '''
    def  __init__(self, message, position,time_limit = 100, font_size = 20, color = (145,145,0)):
        Animation.__init__(self, message, position, time_limit,font_size, color)
        self.x = position[0]
        self.y = position[1]
        self.font_limits = [font_size , font_size + 100]
        self.font_countdown = 10

    def show(self, window):
        self.position = self.x,self.y
        self.timer += 1
        if self.timer >= 50:
            self.dead = True
        write_on_screen(self.message, self.position, window, self.color, self.font_size)
class PointAnimation:
    '''
    points will have an effect of floating up and dissapearing'''
    def  __init__(self, message, position,time_limit = 100, font_size = 20, color = (0,145,0)):
        Animation.__init__(self, message, position, time_limit,font_size, color)
        pos_x = int(position[0])
        self.x = random.randint(pos_x - 50, pos_x + 50)
        self.y = position[1]
        self.speed = 1
    def show(self, window):
        self.y -= self.speed
        self.timer += 1
        if self.timer >= self.time_limit:
            self.dead = True
        write_on_screen(self.message, (self.x,self.y), window, self.color, self.font_size)
class Animator:
    '''
    handles several animations at a time
    '''
    def __init__(self):
        self.animations = []

    def get_point_message_y(self):
        if self.animations != []:
            y = self.animations[-1].y + 100
            return y
        else:
            return random.randint(100,400)

    def  point(self,pos,point_value ,message ,font_size = 15,color = (65,145,45) ,point_color = (0,200,0)):
       # point_info = InfoAnimation(message, (random.randint(100,300),self.get_point_message_y()), font_size = font_size, color = color)
        pos = random.randint(int(pos[0]),int(pos[0])+ 50), random.randint(int(pos[1]),int(pos[1])+ 50)
        point = PointAnimation(str(point_value),pos,font_size = 30,color = point_color)
        self.animations.append(point )
       # self.animations.append(point_info )
    def show(self,window):
        for animation in self.animations:
            animation.show(window)
            if animation.dead:
                self.animations.pop(self.animations.index(animation))
    def clear(self):
        del(self.animations)
        self.animations = []