import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from pygame import sprite
from pygame.draw import *
import math
import random
import time

class Paddle(object):
	def __init__(self, screen, color, x, y, length, width, outline=0):
		self.screen = screen
		self.color = color
		self.rectlist = [x, y, length, width]
		self.outline = outline;
		self.newy = y
		self.diff = 0
		self.center = x + length / 2

	def draw(self):
		self.rect = rect(self.screen, self.color, self.rectlist, self.outline)

	def change(self):
		if (abs(self.newy-self.rectlist[1])>4):
			self.rectlist = [self.rectlist[0], self.rectlist[1]+self.diff, self.rectlist[2], self.rectlist[3]]
		self.draw()

	def move(self, newx):
		self.newy = newx
		current = self.rectlist[0]
		diff = self.newx - current
		self.diff = diff/4

class Block(NotABall):
	def __init__(self, x, y, w, h, color):
		super(Block, self).__init__()
		self.size = Rect(0, 0, w, h)
		self.rect = Rect(x, y, w, h)
		self.color = color
		self.image = pygame.SurfaceType((w, h))
		pygame.draw.rect(self.image, color, self.size)

class Circle(object):
	def __init__(self, screen, color, pos, radius, outline=0):
		self.screen = screen;
		self.color = color;
		self.pos = pos;
		self.radius = radius;
		self.outline = outline;
		self.balldx = 2;
		self.balldy = 1;
		self.speed = math.sqrt(self.balldx**2 + self.balldy**2)

	def draw(self):
		self.setPos(int(self.pos[0]), int(self.pos[1]))
		self.rect = circle(self.screen, self.color, self.pos, self.radius, self.outline)

	def setPos(self, xpos, ypos):
		self.pos = (xpos, ypos)

class Ball(Circle):
	def change(self):
		newx = int(self.pos[0])+self.balldx
		newy = int(self.pos[1])+self.balldy
		self.pos = (newx, newy)
		self.draw()

block1 = Block(120, 60, 60, 30, THECOLORS["blue"])
block2 = Block(60, 60, 60, 30, THECOLORS["green"])
block3 = Block(60, 120, 60, 30, THECOLORS["yellow"])
block4 = Block(180, 60, 60, 30, THECOLORS["orange"])
block5 = Block(240, 60, 60, 30, THECOLORS["red"])
block6 = Block(240, 90, 60, 30, THECOLORS["purple"])
block7 = Block(60, 90, 60, 30, THECOLORS["pink"])
block8 = Block(180, 120, 60, 30, THECOLORS["grey"])
block9 = Block(120, 120, 60, 30, THECOLORS["tan"])
block10 = Block(240, 120, 60, 30, THECOLORS["white"])

clock = pygame.time.Clock() 

class Game(object):
	def __init__(self):
		self.width = 1200
		self.height = 600

		self.numBalls = 3

		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
		self.screen.convert()
		self.screen.fill(THECOLORS["black"])

		self.background = pygame.Surface((self.width, self.height), 0, 32)
		self.background.fill(THECOLORS["black"])
		self.background.convert()

		self.pieces_group = sprite.Group(block1, block2, block3, block4, block5, block6, block7, block8, block9, block10)

		self.image1 = pygame.SurfaceType((15, 40))
		pygame.draw.rect(self.image1, THECOLORS["red"], pygame.Rect(0, 0, 90, 6))

		self.ball = Ball(self.screen, THECOLORS["white"], (100, 10), 12)
		self.paddle = Paddle(self.screen, THECOLORS["red"], 100, 0, 30, 5)

	def draw(self):
		self.screen.fill(THECOLORS["black"])
		self.pieces_group.clear(self.screen, self.background)
		self.pieces_group.draw(self.screen)

	def doUpdate(self):
		pygame.display.set_caption('Python Kinect Game %d fps' % clock.get_fps())
		self.draw()
		self.ball.change()
		self.paddle.change()

		pygame.display.update()

	def play(self):
		while (self.numBalls > 0):

			if (self.ball.pos[0] - self.ball.radius <= 0 or self.ball.pos[0] + self.ball.radius >= 200):
				self.ball.balldx *= -1

			if (self.ball.pos[1] + self.ball.radius >= 99):
				self.ball.balldy *= -1

			if (self.ball.pos[1] <= -2):
				self.numBalls -= 1
				self.ball.setPos(self.paddle.center, 10)
				self.ball.balldy = random.choice([1, 2])

			elif (self.ball.pos[1] <= 5 and self.ball.pos[0] >= self.paddle.center - 15 and self.ball.pos[0] <= self.paddle.center+15):
				self.angle = math.atan2(self.ball.balldx, self.ball.balldy)
				if (self.ball.pos[0] == self.paddle.center):
					self.ball.balldx = 0
					self.ball.balldy *= -1

				if (self.ball.pos[0] < self.paddle.center):
					self.angle = 90 - 14/3 * (self.paddle.center - self.ball.pos[0])
					self.ball.balldy = math.sin(self.angle) * self.ball.speed
					self.ball.balldx = math.cos(self.angle) * self.ball.speed

				if (self.ball.pos[0] > self.paddle.center):
					self.angle = 90 + 14/3 * (self.ball.pos[0] - self.paddle.center)
					self.ball.balldy = math.sin(self.angle) * self.ball.speed
					self.ball.balldx = math.cos(self.angle) * self.ball.speed

			self.totalx = self.ball.pos[0] + self.ball.balldx
			self.totaly = self.ball.pos[1] + self.ball.balldy
			self.ball.setPos(int(self.totalx), int(self.totaly))
			self.ball.balldx = self.ball.balldx
			self.ball.balldy = self.ball.balldy

			self.paddle.move(self.paddle.rectlist[0] + 3)

			self.doUpdate()

			pygame.display.flip()
			clock.tick(40)

		if (self.numBalls == 0):
			t.setText("You lost!")
		else:
			t.setText("You won!")

if __name__ == '__main__':
	# Initialize PyGame
	pygame.init()
	pygame.font.init()

	game = Game()
	game.play()