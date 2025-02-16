import pygame as pg
import sys
from Rocket import *

class App:
    def __init__(self, WIDTH = 800, HEIGHT = 450, FPS = 100,  FPSlock = True):
        self.res = self.width, self.height = (WIDTH, HEIGHT)
        self.screen = pg.display.set_mode(self.res)
        self.clock = pg.time.Clock()
        self.target_fps = FPS
        self.time = 0
        self.FPSlock = FPSlock
        self.dt = 0
        self.dragging_rocket = False
        self.relative_force_app_point = VectorZero()
        self.line_end = VectorZero()

        self.rocket = Rocket(mass=0.8, mI=0.05, pos=vec2(400, 225), cg=vec2(0, 10))

    def update(self):
        self.rocket.update(self.dt)
        #print(self.dt)

    def draw(self):
        self.screen.fill("white")

        self.rocket.draw(pg, self.screen)
        if self.dragging_rocket:
            pg.draw.line(self.screen, "purple", (self.relative_force_app_point + self.rocket.pos).get(), self.line_end.get(), 2)

        pg.display.flip()

    def run(self):
        while True:
            self.get_time()
            self.check_events()

            self.update()
            self.draw()

            if self.FPSlock:
                self.dt = self.clock.tick(self.target_fps) * .001
            else:
                self.dt = self.clock.tick() * .001
            pg.display.set_caption(f'FPS: {round(self.clock.get_fps(), 2)}')


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = vec2(event.pos)
                rocket_rect = pg.Rect(
                    self.rocket.pos.x - self.rocket.width / 2,
                    self.rocket.pos.y - self.rocket.height / 2,
                    self.rocket.width,
                    self.rocket.height
                )
                if rocket_rect.collidepoint(mouse_pos.get()):
                    self.dragging_rocket = True
                    self.relative_force_app_point = mouse_pos - self.rocket.pos
                    self.line_end = mouse_pos
                else:
                    self.rocket.setTarget(mouse_pos)

            elif event.type == pg.MOUSEMOTION:
                if self.dragging_rocket:
                    self.line_end = vec2(event.pos)

            elif event.type == pg.MOUSEBUTTONUP:
                if self.dragging_rocket:
                    force = 0.1*(self.relative_force_app_point + self.rocket.pos - self.line_end)
                    self.rocket.applyForce(force, self.relative_force_app_point + self.rocket.pos)
                    self.dragging_rocket = False

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

if __name__ == '__main__':
    app = App()
    app.run()
