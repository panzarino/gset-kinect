from pygame.color import THECOLORS
from pygame.locals import *
from pygame import sprite
import math
import random
import time

width = 1200
height = 600

win = GraphWin("Breakout", width, height)
win.setCoords(0, 0, 200, 100)

paddle = Polygon(Point(115, 1), Point(85, 1), Point(85, 3), Point(115, 3))
paddle.setFill("blue")
paddle.setOutline("red")
paddle.setWidth(2)
paddle.draw(win)

t = Text(Point(100, 50), "Welcome to Breakout!")
t.setSize(16)
t.draw(win)

ball = Circle(Point(100, 5), 2)		# ball starts on paddle
ball.draw(win)						# use leg? to start (kick leg)
ballCptX = 100
ballCptY = 5
radius = 2
balldx = random.choice([2, -2])
balldy = random.choice([1, 2])

paddleCpt = 100

numBalls = 3
lives = Text(Point(190, 90), "Lives: %i" % numBalls)
lives.setSize(16)
lives.draw(win)

block1 = Polygon(Point(100, 50), Point(100, 60), Point(80, 60), Point(80, 50))
block2 = Polygon(Point(80, 50), Point(80, 60), Point(60, 60), Point(60, 50))
block3 = Polygon(Point(80, 70), Point(60, 70), Point(60, 60), Point(80, 60))
block4 = Polygon(Point(120, 50), Point(120, 60), Point(100, 60), Point(100, 50))
block5 = Polygon(Point(140, 50), Point(140, 60), Point(120, 60), Point(120, 50))
block6 = Polygon(Point(140, 70), Point(140, 60), Point(120, 60), Point(120, 70))
block7 = Polygon(Point(80, 80), Point(80, 70), Point(60, 70), Point(60, 80))
block8 = Polygon(Point(100, 70), Point(120, 70), Point(120, 80), Point(100, 80))
block9 = Polygon(Point(100, 70), Point(80, 70), Point(80, 80), Point(100, 80))
block10 = Polygon(Point(120, 70), Point(140, 70), Point(140, 80), Point(120, 80))

block1.setFill("blue")
block2.setFill("green")
block3.setFill("yellow")
block4.setFill("orange")
block5.setFill("red")
block6.setFill("purple")
block7.setFill("pink")
block8.setFill("black")
block9.setFill("tan")
block10.setFill("light blue")

block1.draw(win)
block2.draw(win)
block3.draw(win)
block4.draw(win)
block5.draw(win)
block6.draw(win)
block7.draw(win)
block8.draw(win)
block9.draw(win)
block10.draw(win)

screen = pygame.display.set_mode((width, height), 0, 32)
screen.convert()
screen.fill(THECOLORS["black"])

background = pygame.Surface((width, height), 0, 32)
background.fill(THECOLORS["black"])
background.convert()

self.group.clear(screen, background)
with self.game.screen_lock:
	self.group.draw(screen)

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
		if (ballCptX == paddleCpt):
			balldx = 0
			balldy *=-1

		if (ballCptX < paddleCpt):
			angle = 90 - 14/3 * (paddleCpt - ballCptX)
			balldx = math.tan(angle)
			balldy = 1

		if (ballCptX > paddleCpt):
			angle = 90 + 14/3 * (ballCptX - paddleCpt)
			balldx = math.tan(angle)
			balldy = 1

if (numBalls == 0):
	t.setText("You lost!")
else:
	t.setText("You won!")

#math.atan2
win.getMouse()
win.close()