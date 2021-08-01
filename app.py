
import pygame, pymunk, sys
from pymunk import pygame_util
class App:

    def __init__(self, name = "App",step = .03,fps = 60, size= (500,500),gravity = (0,200), background_color = pygame.Color("grey"), debug = True, noframe = True):
        self.name =name
        self.fps = fps
        self.step = step
        self.debug = True
        self.background_color = background_color
        self.running = True
        self.SIZE  = size
        self.clock = pygame.time.Clock()
        if noframe:
            self.screen = (pygame.display.set_mode(self.SIZE, pygame.NOFRAME))
        else:
            self.screen = pygame.display.set_mode(self.SIZE )

        pygame.display.set_caption(self.name)
        self.events = None
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.drawoptions = pygame_util.DrawOptions(self.screen)
    def quit_event(self):
        self.events = pygame.event.get()
        events = self.events
                # anticipate a quit event
        for ev in events:
            if ev.type == pygame.QUIT:
                print('exiting Application')
                pygame.quit()
                self.running = False
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q:
                    sys.exit()
    def app_display(self):
        pass

    def run(self):
        while self.running:
            self.quit_event()
            self.screen.fill(self.background_color)
            #self.clock.tick(self.fps)
            self.space.step(self.step)

            if self.debug:
                self.drawoptions = pygame_util.DrawOptions(self.screen)
            self.space.debug_draw(self.drawoptions)
            self.app_display()
            pygame.display.update()
            continue
class GameApp:
        def __init__(self, name = "App",step = .02,fps = 100, size= (500,500),gravity = (0,200), background_color = pygame.Color("grey"), debug = True, noframe = True):
            self.name =name
            self.fps = fps
            self.step = step
            self.debug = debug
            self.background_color = background_color
            self.running = True
            self.SIZE  = size
            self.paused = False
            self.clock = pygame.time.Clock()
            self.level_bg = 20,20,20
            self.game_over = False
            if noframe:
                self.screen = (pygame.display.set_mode(self.SIZE, pygame.NOFRAME))
            else:
                self.screen = pygame.display.set_mode(self.SIZE )

            pygame.display.set_caption(self.name)
            self.events = None
            self.space = pymunk.Space()
            self.gravity = gravity
            self.space.gravity = gravity
            self.drawoptions = pygame_util.DrawOptions(self.screen)
        def get_events(self):
            self.events = pygame.event.get()
            events = self.events
                    # anticipate a quit event
            for ev in events:
                if ev.type == pygame.QUIT:
                    print('exiting Application')
                    pygame.quit()
                    self.running = False
                    sys.exit()

        def app_display(self):
            pass
        def pause_display(self):
            pass
        def game_over_display(self):
            pass
        def general_display(self):
            # stuff thatcan be shoen even ehen game is
            # paused
            pass
        def run(self):
            while self.running:

                self.get_events()
                if self.paused:
                    self.pause_display()
                elif self.game_over:
                    self.game_over_display()
                else:
                    if self.game_over == False:
                        self.space.step(self.step)
                        self.screen.fill(self.level_bg)
                        if self.debug:
                            self.drawoptions = pygame_util.DrawOptions(self.screen)
                            self.space.debug_draw(self.drawoptions)

                    self.app_display()
                self.general_display()
                pygame.display.update()
                continue
