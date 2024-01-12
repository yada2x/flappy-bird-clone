import pygame

class PhysicsObject:
    def __init__(self, game, obj_type, pos, size):
        self.game = game
        self.obj_type = obj_type
        self.pos = list(pos)
        self.size = size

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) # x, y, w, h
    
    def render(self, surf: pygame.Surface):
        surf.blit(self.game.assets[self.obj_type], (self.pos[0], self.pos[1]))


class Pipe(PhysicsObject):
    def __init__(self, game, obj_type, pos, size):
        super().__init__(game, obj_type, pos, size)
        
        self.top_pipe = self.game.assets[obj_type]
        self.bot_pipe = self.game.assets[obj_type]
        self.speed = 15


class Bird(PhysicsObject):
    def __init__(self, game, obj_type, pos, size):
        super().__init__(game, obj_type, pos, size)
        self.velocity = 0
        self.top_bound = self.game.display.get_height() + size[1]
        self.bot_bound = -self.size[1] * 1.25
        self.alive = True
    
    def update(self):
        if self.pos[1] < self.top_bound and self.pos[1] > self.bot_bound:
            self.pos[1] += self.velocity
            self.velocity = min(12, self.velocity + 0.5)
        else:
            self.pos[1] = min(self.top_bound, self.pos[1] + self.velocity)
            self.velocity = min(12, self.velocity + 1)
            self.alive = False
        return self.alive

    def jump(self):
        if self.alive:
            self.velocity = -8