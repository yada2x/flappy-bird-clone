import pygame
import random

class PhysicsObject:
    def __init__(self, game, obj_type, pos, size):
        self.game = game
        self.obj_type = obj_type
        self.pos = list(pos)
        self.size = size
        
        self.action = ''
        self.anim_offset = (0, 0)
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.obj_type + "/" + self.action].copy()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) # x, y, w, h
    
    def render(self, surf: pygame.Surface):
        surf.blit(self.animation.img(), (self.pos[0] + self.anim_offset[0], self.pos[1] + self.anim_offset[1]))
        # surf.blit(self.game.assets[self.obj_type], (self.pos[0], self.pos[1]))

class Pipe(PhysicsObject):
    def __init__(self, game, obj_type, pos, size, gap):
        super().__init__(game, obj_type, pos, size)
        
        self.top_pipe = pygame.transform.flip(self.game.assets[obj_type], False, True)
        self.bot_pipe = self.game.assets[obj_type]
        self.gap = gap
    
    def rect(self):
        return [pygame.Rect(self.pos[0], self.pos[1] - self.size[1] - self.gap // 2, self.size[0], self.size[1]), pygame.Rect(self.pos[0], self.pos[1] + self.gap // 2, self.size[0], self.size[1])]

    def points_rect(self):
        return pygame.Rect(self.pos[0] + self.size[0]//2 , self.pos[1] - self.gap // 2, 1, self.gap)

    def update(self, speed):
        self.pos[0] -= speed

    def render(self, surf: pygame.Surface):
        surf.blit(self.top_pipe, (self.pos[0], self.pos[1] - self.size[1] - self.gap // 2))
        surf.blit(self.bot_pipe, (self.pos[0], self.pos[1] + self.gap // 2))

class PipeSpawner:
    def __init__(self, game, obj_type, spawn_point, size, speed, gap):
        self.pipes: list[Pipe] = []
        self.game = game
        self.obj_type = obj_type
        self.spawn_point = spawn_point
        self.size = size
        self.speed = speed
        self.gap = gap

    def update(self, speed):
        to_remove = []
        pipe: Pipe
        for pipe in self.pipes:
            pipe.update(speed)
            if pipe.pos[0] <= -pipe.size[0]:
                to_remove.append(pipe)
        
        for pipe in to_remove:
            self.pipes.remove(pipe)
    
    def get_rects(self):
        rects = []
        for pipe in self.pipes:
            top, bot = pipe.rect()
            rects.append(top)
            rects.append(bot)
        return rects

    def get_point_rects(self):
        rects = []
        for pipe in self.pipes:
            rects.append(pipe.points_rect())
        return rects

    def render(self, surf: pygame.Surface):
        for pipe in self.pipes:
            pipe.render(surf)
    
    def add_pipe(self):
        y_pos = random.randrange(40 + 30, 360 - 30)
        pipe = Pipe(self.game, self.obj_type, (self.spawn_point, y_pos), self.size, self.gap)
        self.pipes.append(pipe)
    
    def clear(self):
        self.pipes = []

class Bird(PhysicsObject):
    def __init__(self, game, obj_type, pos, size):
        super().__init__(game, obj_type, pos, size)
        self.velocity = 0
        self.top_bound = self.game.display.get_height() - self.size[1] - 112
        self.bot_bound = -self.size[1] * 1.25
        self.alive = True
        self.floored = False

        self.set_action('flapping')

    def update(self):
        if self.pos[1] + self.velocity < self.top_bound and self.pos[1] > self.bot_bound:
            self.pos[1] += self.velocity
            self.velocity = min(12, self.velocity + 0.5)
        else:
            if self.pos[1] + self.velocity < self.top_bound:
                self.pos[1] = min(self.top_bound, self.pos[1] + self.velocity)
                self.velocity = min(12, self.velocity + 1)
            else:
                self.pos[1] = self.top_bound
                self.floored = True
            self.alive = False
        
        self.animation.update()

        return self.alive

    def collisions(self, rects: list[pygame.Rect], point_rects: list[pygame.Rect]):
        bird = self.rect()
        for rect in rects:
            if rect.colliderect(bird):
                self.alive = False
                self.game.sfx['hit'].play()

        for rect in point_rects:
            if rect.colliderect(bird) and self.alive:
                return True
        return False


    def rect(self):
        # 3 pixel leverage
        return pygame.Rect(self.pos[0] + 5, self.pos[1] + 5, self.size[0] - 5, self.size[1] - 5) # x, y, w, h

    def jump(self):
        if self.alive:
            self.velocity = -7