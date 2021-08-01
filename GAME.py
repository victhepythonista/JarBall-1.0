import pygame
import pymunk
import random
import sys
import time

#custom modules
from app import GameApp
from objects import EnclosedBox,GumBall,Pendulum,Jar, JarImage,ObstacleManager
from tools import write_on_screen
from level import Level
from score import ScoreManager
from animation import Animator
from ui import UIbutton
from sounds import GameSounds


# game constants
SCREENSIZE = 500,700
ROPE_COLOR = (230,230,230)
PAUSED = pygame.image.load('./data/images/paused.png')
HELP_INFO = pygame.image.load('./data/images/help.png')
SWISH_POINT_COLOR = 181,250,5,1
SWISH_INFO_COLOR = 100,250,56,1
OBSTACLE_BOUNCE_COLOR = 132,133,200,1
RICOCHET_POINT_COLOR = 5,177,216,1
RICOCHET_INFO_COLOR = 100,234,230,1
HIT_RIM_POINT_COLOR = 5,216,58,1
HIT_RIM_INFO_COLOR = 253,141,0,1
IN_JAR_POINT_COLOR = 5,254,253
class Game(GameApp):
    def __init__(self):
        GameApp.__init__(self, ' test 1', size = SCREENSIZE, background_color = (0,120,215,1), debug =False)
        GameSounds.background_music()
        self.level_bg = Level.random_level_color()
        self.score = 0
        self.score_cache = 0
        self.rope_anchor = None
        self.showing_help = False
        self.help_back_button = UIbutton((200,600), self.back_to_paused_screen, 'back')
        self.paused_buttons =  [
                        UIbutton((100,200), self.resume, '   resume'),
                        UIbutton((100,300), self.main_menu, '  main menu'),
                        UIbutton((100,400), self.help_info,'    help'),
                         UIbutton((100,500), sys.exit,'    quit')
        ]
        self.animator = Animator()
        self.container = EnclosedBox(self.space, 0,0,500,700, friction = .3)
        self.pendulum = None
        self.jar = None
        self.removables = [ ]
        self.rope_cut = False
        self.next_level_count = 0
        self.new_game_count = 0
        self.gumball  = None
        self.hit_rim = False
        self.jar_image = JarImage()
        self.obstacles = [ ]
        self.obstacle_manager = ObstacleManager(self.space)
        self.game_over = False
        self.paused = False
        self.pause_screen_count = 0
        self.TEST_SCORE = 0
        self.RESULTS = 0
        self.in_jar = False
        self.is_highscore = False
        self.new_level()
        self.collision_handlers()
    @property
    def get_ball_pos(self):
        return self.pendulum.pendulum.body.position
    # handle collisions eg ricochets, misses ..etc
    def collision_handlers(self):
        '''
        1 - ball
        2 - walls
        3 - jar rims
        4 - spikes and saws 
        5 - hit the platform

        '''
        ricochet = self.space.add_collision_handler(1,2).begin = self.ricochet
        hit_the_rim = self.space.add_collision_handler(1,3).begin = self.hit_the_rim
        hit_platform = self.space.add_collision_handler(1,5).begin = self.hit_platform_obstacle
        hit_harmful_oject = self.space.add_collision_handler(1,4).begin = self.hit_harmful_oject
        hit_ball = self.space.add_collision_handler(1,6).begin = self.hit_beachball
        bounce_in_jar = self.space.add_collision_handler(1,7).begin = self.bounce_in_jar
        

    def ricochet(self,  *args ):
        if self.pendulum != None and self.rope_cut:
            self.animator.point(self.pendulum.pendulum.body.position, '+2','RICOCHET !',point_color = RICOCHET_POINT_COLOR, color = RICOCHET_INFO_COLOR)
            self.trick_point(2)
            GameSounds.play('bounce_off_wood')
        return True
    def hit_the_rim(self, *args):
        self.animator.point(self.pendulum.pendulum.body.position, '+1', 'rim bounce !!',point_color = HIT_RIM_POINT_COLOR,color = HIT_RIM_INFO_COLOR)
        self.trick_point(1)
        self.hit_rim = True
        GameSounds.play('bounce_off_rim')

        return True
    def hit_beachball(self, *args):
        self.animator.point(self.pendulum.get_ball_pos,'+6','',point_color = OBSTACLE_BOUNCE_COLOR)
        self.trick_point(6)
        GameSounds.play('hit_ball_obstacle')
        return True
    def hit_platform_obstacle(self, *args):
        if self.in_jar == False:
            self.animator.point(self.pendulum.get_ball_pos,'+6','',point_color = OBSTACLE_BOUNCE_COLOR)
            self.trick_point(6)
            GameSounds.play('hit_woody_obstacle')
        return True
    def hit_harmful_oject(self, *args):
        if self.game_over == False and self.in_jar == False:
            self.GAME_OVER()
        return True
    def bounce_in_jar(self, *args):
        GameSounds.play('bounce_off_rim')
        return True
    def main_menu(self):
        self.running = False
    def help_info(self):
        self.showing_help = True
    def back_to_paused_screen(self):
        self.showing_help = False
    # display animations
    def show_animations(self):
        self.animator.show(self.screen)

    # show current obstacles
    def show_obstacles(self):
        self.obstacle_manager.show_obstacles(self.screen)
    # draw rope
    def draw_rope(self):
        if self.rope_cut == False:
            pygame.draw.line(self.screen,ROPE_COLOR, self.rope_anchor,self.pendulum.body.position,2 )

    # destroy the jar and ball
    def destroy_removables(self):
        for item in self.removables:
                item.destroy()

    def trick_point(self, point):
        if self.game_over == False :
            self.score_cache += point
    # start a new hame
    def new_game(self):
        self.score = 0
        self.new_game_count = 0
        self.score_cache = 0
        self.new_level()

    # make a new level
    def new_level(self):
        self.in_jar = False
        self.score += self.score_cache
        self.score_cache = 0
        self.obstacle_manager.new_obstacle(self.score)
        # clear current animations
        self.animator.clear()
        self.hit_rim = False
        self.next_level_count = 0
        self.destroy_removables()
        new_level_items = Level.new_level(self.space,self.score)
        pivot_pos = new_level_items[0]
        ball_pos = new_level_items[1]
        jar_pos = new_level_items[2]
        self.rope_anchor = pivot_pos
        self.pendulum = Pendulum(self.space,pivot_pos, ball_pos )
        self.jar = Jar(self.space, jar_pos[0],jar_pos[1],100,150)
        self.removables = [self.pendulum ,self.jar]
        self.rope_cut = False
        self.level_bg = new_level_items[3]
        self.gumball = GumBall(self.pendulum.body)
        # add obstacles if score is more than 20
    def resume(self):
        self.paused =  False
        GameSounds.background_music()
    def GAME_OVER(self):
        if self.game_over == False:
            self.RESULTS = self.score
            self.game_over = True
            self.is_highscore = ScoreManager.is_highscore(self.RESULTS)
            self.new_game()

    def ball_is_in_jar(self):
        ball_pos = self.pendulum.get_ball_pos
        if self.jar.x < ball_pos[0] < self.jar.limit_x and ball_pos[1] < self.jar.limit_y and ball_pos[1] > self.jar.y:
            return True
        return False
    # checks if ball in basket
    def ball_in_jar(self):
        ball_pos = self.pendulum.body.position

        if ball_pos[1] > self.jar.y + 100 and ((ball_pos[0] > self.jar.limit_x)  or (ball_pos[0] < self.jar.x)) :
            self.GAME_OVER()
        # if ball is stationary
        if self.pendulum.body.velocity == (0,0):
            self.GAME_OVER()
        if self.ball_is_in_jar():
            self.in_jar = True
            if self.next_level_count == 0:
                GameSounds.play('in_jar')
                self.score += 5
                self.animator.point(self.get_ball_pos,'+5','in the jar !' , point_color = IN_JAR_POINT_COLOR)
                if self.hit_rim == False:
                    self.animator.point(self.get_ball_pos,'+3','its a SWISH' ,point_color = SWISH_POINT_COLOR, color = SWISH_INFO_COLOR )
                    self.trick_point(3)
            self.next_level_count += 1
            if self.next_level_count > 200 :
                if self.ball_is_in_jar():
                    self.new_level()
                else:
                    self.GAME_OVER()
        elif ball_pos[1] > self.jar.y:
            if self.new_game_count > 200:
                self.GAME_OVER()
            self.new_game_count += 1

    # get key inputs
    def handle_keys(self):
        '''
        esc - pause
        space- cut cord/rope
        '''
        for ev in self.events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    if self.showing_help == True:
                        self.showing_help = False
                    elif self.game_over == False and self.paused == False:
                        self.paused =True
                        GameSounds.UI_background_music()
                if ev.key == pygame.K_r:
                    self.paused = False
                if ev.key == pygame.K_SPACE:
                    if self.rope_cut == False and self.game_over == False and self.paused == False :
                        GameSounds.play('snip')
                        self.pendulum.cut()
                        self.rope_cut = True
                       
                    if self.game_over :
                        self.game_over = False
                
    def game_over_display(self):
        self.screen.fill((20,20,20))
        if self.is_highscore:
            write_on_screen('NEW HIGHSCORE!' , (40,200), self.screen,(100, 100,200),50)
            write_on_screen('   %s' %self.RESULTS , (50,300), self.screen,(40, 100,160),50)
        else:
            write_on_screen('GAME OVER' , (100,200), self.screen,(200, 0,0),50)
            write_on_screen(str(self.RESULTS) , (150,300), self.screen,(200, 0,0),60)
        write_on_screen('space to restart' , (100,600), self.screen,(200, 200,250),30)
    # paused game
    def pause_display(self):
        self.screen.fill((20,20,20))
        self.pause_screen_count += 1
        if self.showing_help:
            self.screen.blit(HELP_INFO, (0,0))
            self.help_back_button.show(self.screen,pygame.mouse.get_pos(), self.events)
        else:
            write_on_screen('highscore : %s'%ScoreManager.get_highscore(), (10,30), self.screen,(70,70,143),25)
            for b in self.paused_buttons:
                b.show(self.screen,pygame.mouse.get_pos(), self.events)

        self.handle_keys()

    def general_display(self):
        if self.showing_help == False:
            write_on_screen('score : %s'%self.score, (10,0), self.screen,(0,200,0),25)
        self.handle_keys()
    def app_display(self):
        self.handle_keys()
        self.ball_in_jar()
        self.show_obstacles()
        if self.gumball != None:
            angle = self.pendulum.pendulum.body.angle
            
            self.draw_rope()
            self.gumball.show(self.screen,angle)
           
            jar_pos = self.jar.pos[0], self.jar.pos[1] - 5
            self.jar_image.show(self.screen  ,jar_pos)
        self.show_animations()


if __name__ == '__main__':
    Game().run()
