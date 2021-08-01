
'''
introduction screen
'''

import pygame
import random
import sys

from ui import UIbutton
from app import App
from objects import GumBall,Pendulum,EnclosedBox
from tools import write_on_screen
from sounds import GameSounds
SCREENSIZE = 500,700
bg_color = 15,15,15
LOGO = pygame.image.load('./data/images/logo.png')
help_info = pygame.image.load('./data/images/help.png')

class Intro(App):
    def __init__(self):
        App.__init__(self, ' test 1', size = SCREENSIZE, background_color = bg_color)
        GameSounds.UI_background_music()
        self.intro_screen_buttons = [
            UIbutton((200,250), self.start, 'start'),
            UIbutton((200,350), self.show_help, 'help'),
            UIbutton((200,450), self.exit, 'exit'),


        ]
        self.game_started = False
        self.start_timer = 0
        self.starting_pendulum =Pendulum(self.space, (250,180), (400,190),elasticity = .6,friction = .2)
        self.start_gumball_color = GumBall.get_random_color()
        self.container = None
        self.showing_help = False
    def draw_rope(self):
     if self.game_started == False:
        pygame.draw.line(self.screen,(240,240,240), self.starting_pendulum.joint_position,self.starting_pendulum.body.position,2 )

    def show_logo(self):
        self.screen.blit(LOGO, (0,0))
    def show_ball(self):
        pygame.draw.circle(self.screen, (240,240,240), self.starting_pendulum.body.position, 31,0)
    def show_help(self):
        self.showing_help = True
    def handle_keys(self):
        for ev in self.events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.showing_help = False
                    


    # display buttons , titles and other widgets
    def display_widgets(self):
        if self.showing_help:
            self.screen.fill(bg_color)
            self.screen.blit(help_info, (0,0))
        else:
            for button in self.intro_screen_buttons:
                button.show(self.screen, pygame.mouse.get_pos(), self.events)
            self.show_ball()
            self.show_logo()
    # starting the game
    def start(self):
        self.container = EnclosedBox(self.space, 0,0,500,700, elasticity = .8,friction= .3)
        self.starting_pendulum.cut()
        self.game_started = True
        print('starting')

    # exiting game
    def exit(self):
        sys.exit()
    def app_display(self):
        self.draw_rope()
        self.display_widgets()
        self.handle_keys()
        if self.game_started:
            self.start_timer += 1
            if self.start_timer >= 200:
                self.running = False
                pygame.mixer.music.stop()


if __name__ == '__main__':
    Intro().run()
