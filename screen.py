import pygame, sys, os, numpy

class Screen:
    '''

    a basic screen

    '''
    def __init__(self, size, fps = 50, title = 'basic screen', noframe = False):
        pygame.init()
        self.running = True
        self.name = ""
        self.size = size
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.events = pygame.event.get()
        pygame.display.set_caption(title)
        self.window = pygame.display.set_mode(self.size, pygame.NOFRAME  ) if noframe else pygame.display.set_mode(self.size  )


    def screen_backend(self):
        self.clock.tick(self.fps)
        pygame.display.set_caption(self.name)



    def exit(self):
        # exit the screen
        self.running = False

    def quit_event(self  ):
            # anticipate a quit event

        for ev in self.events:
            if ev.type == pygame.QUIT:
                pygame.quit()
                self.running = False
                sys.exit()
    def dipslay_widgets(self):
        pass
    def show(self):
        while self.running:
            self.display_widgets()
            self.events = pygame.event.get()
            self.screen_backend()

            self.quit_event()
            pygame.display.update()
            continue
