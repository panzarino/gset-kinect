import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from pygame import sprite
import math
import random
import time

width = 1200
height = 600

numBalls = 3

class NotABall(sprite.Sprite):
    def hit_by_ball(self, cur_ball):
        pass

class Paddle(pygame.sprite.DirtySprite, NotABall):
	def __init__(self, image, paddleCpt):
		self.image = image
		self.dirty = 2
		self.rect = Rect(85, 3, 30, 2)
		self.size = Rect(0, 0, 30, 2)
		self.paddleCpt = 100

class Block(NotABall):
	def __init__(self, x, y, w, h, color):
		self.size = Rect(0, 0, w, h)
		self.rect = Rect(x, y, w, h)
		self.color = color
		self.image = pygame.SurfaceType((w, h))
		pygame.draw.rect(self.image, color, self.size)

class Ball(sprite.Sprite):
    def __init__(self, game, color = 'white', size = 2, 
                 direction = math.atan2(1, .5), ballCptX = 100, ballCptY = 5, balldx = random.choice([2, -2]), balldy = random.choice([1, 2])):
        super(Ball, self).__init__()
        self.size = size
        self.color = color
        self.image = pygame.SurfaceType((size, size))
        self.set_color(color)
        self.speed = speed
        self.ballCptX = ballCptX
        self.ballCptY = ballCptY
        self.balldx = balldx
        self.balldy = balldy
        self.old_pos = None        
        self.rect = pygame.Rect(ballCptX, ballCptY, size, size)
        self.speed = math.sqrt(balldx**2 + balldy**2)

    def set_color(self, new_color):
        self.color = new_color
        pygame.draw.circle(self.image, THECOLORS[new_color], (self.size/2, self.size/2), self.size/2)

block1 = Block(80, 60, 20, 10, THECOLORS["blue"])
block2 = Block(60, 60, 20, 10, THECOLORS["green"])
block3 = Block(60, 60, 20, 10, THECOLORS["yellow"])
block4 = Block(100, 60, 20, 10, THECOLORS["orange"])
block5 = Block(120, 60, 20, 10, THECOLORS["red"])
block6 = Block(120, 60, 20, 10, THECOLORS["purple"])
block7 = Block(60, 70, 20, 10, THECOLORS["pink"])
block8 = Block(120, 80, 20, 10, THECOLORS["black"])
block9 = Block(80, 80, 20, 10, THECOLORS["tan"])
block10 = Block(140, 80, 20, 10, THECOLORS["white"])

screen = pygame.display.set_mode((width, height), 0, 32)
screen.convert()
screen.fill(THECOLORS["black"])

background = pygame.Surface((width, height), 0, 32)
background.fill(THECOLORS["black"])
background.convert()

image1 = pygame.SurfaceType((15, 40))
pygame.draw.rect(image1, THECOLORS["red"], pygame.Rect(0, 0, 30, 2))

while (numBalls > 0):
	if (paddleCpt == ballCptX):
		pass

	elif (paddleCpt < ballCptX and paddleCpt < 185):
		paddle.move(1,0)
		paddleCpt += 1

	elif (paddleCpt > ballCptX and paddleCpt > 15):
		paddle.move(-1,0)
		paddleCpt -= 1

	ball.move(balldx, balldy)
	ballCptX += balldx
	ballCptY += balldy

	if (ballCptX-radius <= 0 or ballCptX+radius >= 200):
		balldx *= -1

	if (ballCptY+radius >= 99):
		balldy *= -1

	if (ballCptY <= -2):
		numBalls -= 1
		lives.setText("Lives: %i" % numBalls)
		time.sleep(2)
		ball.move(paddleCpt-ballCptX, 5-ballCptY)
		ballCptX = paddleCpt
		ballCptY = 5
		balldy = random.choice([1, 2])

	elif (ballCptY <= 5 and ballCptX >= paddleCpt-15 and ballCptX <= paddleCpt+15):	# collision
		angle = atan2(balldx, balldy)
		if (ballCptX == paddleCpt):
			balldx = 0
			balldy *= 1

		if (ballCptX < paddleCpt):
			angle = 90 - 14/3 * (paddleCpt - ballCptX)
			balldy = math.sin(angle) * speed
			balldx = math.cos(angle) * speed

		if (ballCptX > paddleCpt):
			angle = 90 + 14/3 * (ballCptX - paddleCpt)
			balldy = math.sin(angle) * speed
			balldx = math.cos(angle) * speed

if (numBalls == 0):
	t.setText("You lost!")
else:
	t.setText("You won!")

#math.atan2
win.getMouse()
win.close()