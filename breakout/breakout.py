import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from pygame import sprite
import math
import random
import time

class NotABall(sprite.Sprite):
	def hit_by_ball(self, cur_ball):
		pass

class Paddle(pygame.sprite.DirtySprite, NotABall):
	def __init__(self, image):

		self.image = image
		self.dirty = 2
		self.rect = Rect(85, 3, 30, 2)
		self.size = Rect(0, 0, 30, 2)
		self.paddleCpt = 100

	def getPaddleCpt(self):
		return self.paddleCpt

class Block(NotABall):
	def __init__(self, x, y, w, h, color):
		super(Block, self).__init__()
		self.size = Rect(0, 0, w, h)
		self.rect = Rect(x, y, w, h)
		self.color = color
		self.image = pygame.SurfaceType((w, h))
		pygame.draw.rect(self.image, color, self.size)

class Ball(sprite.Sprite):
	def __init__(self, color = 'white', size = 2, direction = math.atan2(1, .5), ballCptX = 100, ballCptY = 5, balldx = random.choice([2, -2]), balldy = random.choice([1, 2])):
		super(Ball, self).__init__()
		self.size = size
		self.color = color
		self.image = pygame.SurfaceType((size, size))
		self.set_color(color)
		self.ballCptX = ballCptX
		self.ballCptY = ballCptY
		self.balldx = balldx
		self.balldy = balldy
		self.old_pos = None
		self.rect = pygame.Rect(ballCptX, ballCptY, size, size)
		self.speed = math.sqrt(balldx**2 + balldy**2)
		self.radius = size / 2

	def update(self, *args):
		self.prev_rect = self.rect
		self.rect = pygame.Rect(self.ballCptX, self.ballCptY, self.size, self.size)
		return super(Ball, self).update(*args)

	def set_color(self, new_color):
		self.color = new_color
		pygame.draw.circle(self.image, THECOLORS[new_color], (self.size/2, self.size/2), self.size/2)

	def getBallCptX(self):
		return self.ballCptX

	def getBallCptY(self):
		return self.ballCptY

	def getBalldx(self):
		return self.balldx

	def getBalldy(self):
		return self.balldy

	def setBallCptX(self, x):
		self.ballCptX = x

	def setBallCptY(self, y):
		self.ballCptY = y

	def setBalldx(self, x):
		self.balldx = x

	def setBalldy(self, y):
		self.balldy = y

	def getRadius(self):
		return self.radius

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
		self.ball_group = sprite.Group()

		self.image1 = pygame.SurfaceType((15, 40))
		pygame.draw.rect(self.image1, THECOLORS["red"], pygame.Rect(0, 0, 90, 6))

		self.ball = Ball()
		self.paddle = Paddle(self.image1)

		self.ballCptX = self.ball.getBallCptX()
		self.ballCptY = self.ball.getBallCptY()
		self.balldx = self.ball.getBalldx()
		self.balldy = self.ball.getBalldy()
		self.paddleCpt = self.paddle.getPaddleCpt()
		self.radius = self.ball.getRadius()

		self.ball.add(self.ball_group)

	def draw(self):
		self.pieces_group.clear(self.screen, self.background)
		self.pieces_group.draw(self.screen)

		self.ball_group.clear(self.screen, self.background)
		self.ball_group.draw(self.screen)

	def doUpdate(self):
		pygame.display.set_caption('Python Kinect Game %d fps' % clock.get_fps())
		self.ball.update()
		self.draw()

	def play(self):
		while (self.numBalls > 0):
			if (self.paddleCpt == self.ballCptX):
				pass

			elif (self.paddleCpt < self.ballCptX and self.paddleCpt < 185):
				self.paddle.move(1,0)
				self.paddleCpt += 1

			elif (self.paddleCpt > self.ballCptX and self.paddleCpt > 15):
				paddle.move(-1,0)
				paddleCpt -= 1

			self.totalx = self.ballCptX + self.balldx
			self.totaly = self.ballCptY + self.balldy
			self.ball.setBallCptX(self.totalx)
			self.ball.setBallCptY(self.totaly)


			if (self.ballCptX - self.radius <= 0 or self.ballCptX + self.radius >= 200):
				self.balldx *= -1

			if (self.ballCptY + self.radius >= 99):
				self.balldy *= -1

			if (self.ballCptY <= -2):
				self.numBalls -= 1
				self.lives.setText("Lives: %i" % self.numBalls)
				time.sleep(2)
				self.ball.move(self.paddleCpt - self.ballCptX, 5 - self.ballCptY)
				self.ballCptX = self.paddleCpt
				self.ballCptY = 5
				self.balldy = random.choice([1, 2])

			elif (self.ballCptY <= 5 and self.ballCptX >= self.paddleCpt - 15 and self.ballCptX <= self.paddleCpt+15):
				self.angle = math.atan2(self.balldx, self.balldy)
				if (self.ballCptX == self.paddleCpt):
					self.balldx = 0
					self.balldy *= 1

				if (self.ballCptX < self.paddleCpt):
					self.angle = 90 - 14/3 * (self.paddleCpt - self.ballCptX)
					self.balldy = math.sin(self.angle) * self.speed
					self.balldx = math.cos(self.angle) * self.speed

				if (self.ballCptX > self.paddleCpt):
					self.angle = 90 + 14/3 * (ballCptX - paddleCpt)
					self.balldy = math.sin(self.angle) * self.speed
					self.balldx = math.cos(self.angle) * self.speed

			self.ball.setBalldx(self.balldx)
			self.ball.setBalldy(self.balldy)
			self.ball.setBallCptX(self.ballCptX)
			self.ball.setBallCptY(self.ballCptY)

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