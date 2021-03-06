import pygame
from pygame.draw import *

class Circle(object):
	def __init__(self, screen, color, pos, rad, outline=0):
		self.screen = screen;
		self.color = color;
		self.pos = pos;
		self.rad = rad;
		self.outline = outline;
		self.x = 0
		self.y = 0
	# put into position
	def draw(self):
		self.rect = circle(self.screen, self.color, self.pos, self.rad, self.outline)
class Ball(Circle):
	def change(self):
		newx = int(self.pos[0])+self.x
		newy = int(self.pos[1])+self.y
		self.pos = (newx, newy)
		self.draw()
class Paddle(object):
	# create paddle
	def __init__(self, screen, color, x, y, length, width, outline=0):
		self.screen = screen
		self.color = color
		self.rectlist = [x, y, length, width]
		self.outline = outline;
		self.newy = y
		self.diff = 0
	# put into position
	def draw(self):
		self.rect = rect(self.screen, self.color, self.rectlist, self.outline)
	# update coordinates
	def change(self):
		if (abs(self.newy-self.rectlist[1])>4):
			self.rectlist = [self.rectlist[0], self.rectlist[1]+self.diff, self.rectlist[2], self.rectlist[3]]
		self.draw()
	def move(self, newy):
		self.newy = newy
		current = self.rectlist[1]
		diff = self.newy - current
		self.diff = diff/4
class Line(object):
	# create line
	def __init__(self, screen, color, start, end, width=1):
		self.screen = screen
		self.color = color
		self.start = start
		self.end = end
		self.width = width
	# put into position
	def draw(self):
		self.rect = line(self.screen, self.color, self.start, self.end, self.width)
	# update coordinates
	def change(self, x1=0, y1=0, x2=0, y2=0):
		newx1 = int(self.start[0])+x1
		newy1 = int(self.start[1])+y1
		self.start = (newx1, newy1)
		newx2 = int(self.end[0])+x2
		newy2 = int(self.end[1])+y2
		self.end = (newx2, newy2)
		self.draw()
class Text(object):
	# create Text
	def __init__(self, screen, font, text, color, pos, antialias=0):
		self.screen = screen
		self.font = font
		self.content = text
		self.color = color
		self.pos = pos
		self.antialias = antialias
	def draw(self):
		self.text = self.font.render(self.content, self.antialias, self.color)
		self.screen.blit(self.text, self.pos)
	def change(self, text=""):
		self.content = text
		self.draw()
def center_text(font, string, y, z):
	x = w = 0
	dim = font.size(string)
	width = w + (y - w - dim[0]) / 2
	height = x + (z - x - dim[1]) / 2
	return (width, height)
