from color import *

import pygame
from pygame.locals import *

import ctypes
import sys
import time

class Game(object):
	# initialize object
	def __init__(self, name, background = BLACK, show_cursor = False):
		self.name = name
		self.background = background;
		self.show_cursor = show_cursor
	# start pygame in fullscreen
	def start(self):
		pygame.init()
		pygame.display.set_caption(self.name)
		self.screensize = get_screen_size()
		self.screen = pygame.display.set_mode(self.screensize, pygame.FULLSCREEN)
		pygame.mouse.set_visible(self.show_cursor)
		self.screen.fill(self.background)
	# quit game
	def quit(self):
		pygame.quit()
		sys.exit()
	# render screen
	def render(self, clear=True):
		pygame.display.update()
		if clear:
			self.screen.fill(self.background)
	# time delay
	def delay(self, sec):
		return time.sleep(sec)

def get_screen_size():
	user32 = ctypes.windll.user32
	return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)