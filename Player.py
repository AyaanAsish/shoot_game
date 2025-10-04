"""
Ayaan Asish
Player class file to make objects in space invaders game
2025-06-13
ICD2O
"""

# imports
import random


# Player CLASS
class Player:
    # constructor
    def __init__(self, x, y, dx, dy, img, dim, hasM, isM):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.img = img
        self.dim = dim
        self.hasM = hasM
        if isM:
            self.state = "rd"

    # movement
    def moveTickX(self):
        self.x += self.dx

    def moveTickY(self):
        self.y += self.dy

    def moveTick(self):
        self.moveTickX()
        self.moveTickY()

    # random position set
    def setRand(self):
        self.x = random.randint(0, 750)
        self.y = random.randint(0, 100)

    # check if object still inbounds
    def checkBoundaryX(self, w):
        if self.x < 0:
            return 0
        elif self.x > w - self.dim:
            return w - self.dim
        else:
            return -1

    def checkBoundaryY(self, h):
        if self.y < 0:
            return 0
        elif self.y > h - self.dim:
            return h - self.dim
        else:
            return -1

    def checkBoundary(self, w, h):
        if self.checkBoundaryX(w) == -1 and self.checkBoundaryY(h) == -1:
            return -1
        else:
            return [self.x, self.y]

    # figure out distance between 2 objects
    def distance(self, o):
        return (((self.x + self.dim / 2) - (o.x + o.dim / 2)) ** 2 + (
                (self.y + self.dim / 2) - (o.y + o.dim / 2)) ** 2) ** 0.5

    # collision methods, 1 with higher radius
    @staticmethod
    def collisionR(o1, o2):
        if o1.distance(o2) < 35:
            return True
        else:
            return False

    @staticmethod
    def collisionS(o1, o2):
        if o1.distance(o2) < 75:
            return True
        else:
            return False
