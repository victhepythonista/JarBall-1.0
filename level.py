import random
from random import randint,randrange


level_bgs = [
 (0,120,215,1),
 (255,228,81,1),
(173,255,47,1),
(103,238,233,1),
(161,165,231,1),
(98,238,195,1),
(156,152,237,1),
(195,237,152),
(152,209,137),
(141,212,240),
 ]
'''
 a level dict contains a list of different possible values that represent different levels
  eg :
    {(pendulum_pivot_pos),(ball_pos),(basket pos) ,background_color '''

ball_positions = [(40,50), (390,100)]
levels = {
0 : [ [
        (randint(200,300),0),
        (random.choice(ball_positions)),
        (random.randint(65,300), random.randint(500,550))
    ] for i in range(100)],

 }
class Level:
    @staticmethod
    def random_level_color():
        #return random.choice(level_bgs)
        return (230,230,230)
    @staticmethod
    def random_point_position():
        return (random.randint(100,300), random.randint(100,200))
    @staticmethod
    def new_level(space, score ):
        level_index = 0
        info =  random.choice(levels[level_index])
        info.append((20,20,20))
        return info
