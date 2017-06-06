
#
import pygame
import settings as opt

import logging
info = logging.info
debug = logging.debug
error = logging.error
warning = logging.warning
collide = pygame.sprite.spritecollide

from vec import Vec2d as Vector

class Entrance(pygame.sprite.Sprite):
    oid = 0
    def __init__(self, world, pos, dim, color):
        self._layer = opt.ENTRANCE_LAYER
        self.groups = world.all_sprites, world.entrance
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.oid = Entrance.oid
        Entrance.oid += 1
        self.world = world
        self.image = pygame.Surface(dim)
        self.image.fill(color)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.pos = Vector(pos)
        self._active = False
        self.car = None
        self.reserved = False
        self.access_log = dict()
        self.activate

    @property
    def active(self):
        return self._active

    def __cmp__(self, other):
        return cmp(self.oid, other.oid)

    def update(self):
        self.rect.center = self.pos
        cc = collide(self, self.world.cars, False)
        if self.active:
            if not cc:
                self.deactivate()
                self.car = None
        else:
            if cc:
                for c in cc:
                    self.activate()
                    self.car = c
                    debug("Car %d arrived at entrance %d at %s",
                           c.oid, self.oid, opt.str_now())

    def activate(self):
        self._active = True
        self.image = pygame.Surface((4, 6))
        self.image.fill(opt.RED)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.pos = Vector((90, 128))


    def deactivate(self):
        self._active = False
        self.image = pygame.Surface((4, 30))
        self.image.fill(opt.RED)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.pos = Vector((90,140))
