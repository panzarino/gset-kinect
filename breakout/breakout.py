import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from pygame import sprite
from pygame.draw import *
import math
import random
import time
from pykinect import nui
import ctypes
import thread

KINECTEVENT = pygame.USEREVENT

video_display = False

kinect = nui.Runtime()
kinect.skeleton_engine.enabled = True

screen_lock = thread.allocate()

def get_screen_size():
	user32 = ctypes.windll.user32
	return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

class Paddle(object):
	def __init__(self, screen, color, x, y, length, width, outline=0):
		self.screen = screen
		self.color = color
		self.rectlist = [x, y, length, width]
		self.outline = outline;
		self.newx = x
		self.diff = 0
		self.center = x + length / 2

	def draw(self):
		self.rect = rect(self.screen, self.color, self.rectlist, self.outline)

	def change(self):
		if (abs(self.newx-self.rectlist[0])>4):
			self.rectlist = [self.rectlist[0] + self.diff, self.rectlist[1], self.rectlist[2], self.rectlist[3]]
		self.draw()

	def move(self, newx):
		self.newx = newx
		current = self.rectlist[0]
		diff = self.newx - current
		self.diff = diff/4

class Block(object):
	def __init__(self, screen, color, x, y, length, width, exists, outline=0):
		self.screen = screen
		self.color = color
		self.rectlist = [x, y, length, width]
		self.outline = outline
		self.newx = x
		self.diff = 0
		self.exists = exists

	def draw(self):
		if (self.exists):
			self.rect = rect(self.screen, self.color, self.rectlist, self.outline)

	def change(self):
		if (abs(self.newx-self.rectlist[0])>4):
			self.rectlist = [self.rectlist[0] + self.diff, self.rectlist[1], self.rectlist[2], self.rectlist[3]]
		self.draw()

class Circle(object):
	def __init__(self, screen, color, pos, radius, outline=0):
		self.screen = screen
		self.color = color
		self.pos = pos
		self.radius = radius
		self.outline = outline
		self.balldx = 2
		self.balldy = -1
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

clock = pygame.time.Clock() 

class Game(object):
	def __init__(self):
		self.screensize = get_screen_size()
		self.screen = pygame.display.set_mode(self.screensize, pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		
		self.width = 1200
		self.height = 600

		self.numBalls = 3

		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
		self.screen.convert()
		self.screen.fill(THECOLORS["black"])

		self.background = pygame.Surface((self.width, self.height), 0, 32)
		self.background.fill(THECOLORS["black"])
		self.background.convert()

		block2 = Block(self.screen, THECOLORS["green"], 360, 60, 120, 60, True)
		block7 = Block(self.screen, THECOLORS["pink"], 360, 120, 120, 60, True)
		block3 = Block(self.screen, THECOLORS["yellow"], 360, 180, 120, 60, True)
		block1 = Block(self.screen, THECOLORS["blue"], 480, 60, 120, 60, True)
		block9 = Block(self.screen, THECOLORS["tan"], 480, 180, 120, 60, True)
		block4 = Block(self.screen, THECOLORS["orange"], 600, 60, 120, 60, True)
		block8 = Block(self.screen, THECOLORS["grey"], 600, 180, 120, 60, True)
		block5 = Block(self.screen, THECOLORS["red"], 720, 60, 120, 60, True)
		block6 = Block(self.screen, THECOLORS["purple"], 720, 120, 120, 60, True)
		block10 = Block(self.screen, THECOLORS["white"], 720, 180, 120, 60, True)

		self.pieces_group = (block1, block2, block3, block4, block5, block6, block7, block8, block9, block10)

		self.image1 = pygame.SurfaceType((15, 40))
		pygame.draw.rect(self.image1, THECOLORS["red"], pygame.Rect(0, 0, 90, 6))

		self.ball = Ball(self.screen, THECOLORS["white"], (650, 560), 12)
		self.paddle = Paddle(self.screen, THECOLORS["red"], 550, 580, 200, 10)

		self.isCollided = False

	def quit(self):
		pygame.quit()
		sys.exit()

	def go(self):
		# move paddles to kinect locations
		events = pygame.event.get()
		for e in events:
			if e.type == KINECTEVENT:
				for skeleton in e.skeletons:
					head = skeleton.SkeletonPositions[JointId.Head]
					if (not head.y==0):
						xval = interp(head.x, [-.025,.30], [0,1])
						xpos = (1-xval) * self.game.screensize[1]
						self.paddle.move(xpos)
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					self.game.quit()

	def doUpdate(self):
		pygame.display.set_caption('Python Kinect Game %d fps' % clock.get_fps())
		self.screen.fill(THECOLORS["black"])
		self.go()
		self.ball.change()
		self.paddle.change()
		for m in self.pieces_group:
			m.change()

		pygame.display.update()

	def play(self):
		while (self.numBalls > 0):

			if (self.ball.pos[0] - self.ball.radius <= 0 or self.ball.pos[0] + self.ball.radius >= 1200):
				if (self.isCollided == False):
					self.ball.balldx *= -1
					self.isCollided = True
			else:
				self.isCollided = False

			if (self.ball.pos[1] + self.ball.radius <= 20):
				if (self.isCollided == False):
					self.ball.balldy *= -1
					self.isCollided = True
			else:
				self.isCollided = False

			if (self.ball.pos[1] >= 610):
				self.numBalls -= 1
				self.ball.setPos(self.paddle.center, 540)
				self.ball.balldy = random.choice([-1, -2])

			if (self.ball.pos[1] + self.ball.radius >= 580 and self.ball.pos[0] >= self.paddle.center - 100 and self.ball.pos[0] <= self.paddle.center + 100):
				self.angle = math.atan2(self.ball.balldx, self.ball.balldy)
				if (self.isCollided == False):
					self.isCollided = True
					if (self.ball.pos[0] == self.paddle.center):
						self.ball.balldx = 0.1
						self.ball.balldy *= -1

					if (self.ball.pos[0] < self.paddle.center):
						self.angle = 90 - 14/3 * (self.paddle.center - self.ball.pos[0])
						self.ball.balldy = -math.sin(self.angle) * self.ball.speed
						self.ball.balldx = math.cos(self.angle) * self.ball.speed

					if (self.ball.pos[0] > self.paddle.center):
						self.angle = 90 + 14/3 * (self.ball.pos[0] - self.paddle.center)
						self.ball.balldy = -math.sin(self.angle) * self.ball.speed
						self.ball.balldx = math.cos(self.angle) * self.ball.speed
			else:
				self.isCollided = False

			check = False

			if (self.isCollided == False):
				for m in self.pieces_group:
					if (self.ball.pos[0] + self.ball.radius >= m.rectlist[0] and self.ball.pos[0] - self.ball.radius <= m.rectlist[0] + m.rectlist[2]):
						if (m.rectlist[1] <= self.ball.pos[1] <= m.rectlist[1] + m.rectlist[3] and (m.rectlist[0] < self.ball.pos[0] <= m.rectlist[0] + 5 or m.rectlist[0] + m.rectlist[2] - 5 <= self.ball.pos[0] < m.rectlist[0] + m.rectlist[2]) and m.exists):		# block 1 left/right side
							self.ball.balldx = -self.ball.balldx
							check = True
							self.isCollided = True

						if (m.rectlist[0] <= self.ball.pos[0] <= m.rectlist[0] + m.rectlist[2] and (m.rectlist[1] < self.ball.pos[1] <= m.rectlist[1] + 5 or m.rectlist[1] + m.rectlist[3] - 5 <= self.ball.pos[1] < m.rectlist[1] + m.rectlist[3]) and m.exists):	# block 1 top/bottom side 
							self.ball.balldy = -self.ball.balldy
							self.isCollided = True
							check = True

					else:
						self.isCollided = False
					
					if (check):
						m.exists = False
						check = False

			self.totalx = self.ball.pos[0] + self.ball.balldx
			self.totaly = self.ball.pos[1] + self.ball.balldy
			self.ball.setPos(int(self.totalx), int(self.totaly))

			self.doUpdate()

			pygame.display.flip()
			clock.tick(40)

if __name__ == '__main__':
	# Initialize PyGame
	pygame.init()
	pygame.font.init()

	game = Game()
	game.play()