from controller import Controller

from core.game import Game
from core.color import *
import pygame
from time import sleep

def run():

	game = Game("Pong")
	game.start()

	# create and start the controller
	controller = Controller(game)
	controller.start()

	# keep looping the game
	while True:

		# tell the controller to get the next frame
		controller.go()

		# add a little render delay
		# 60 fps
		game.delay(.016)

if __name__ == "__main__":
	run()
