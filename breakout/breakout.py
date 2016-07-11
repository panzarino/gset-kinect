from graphics import *
import math
import random
import time

win = GraphWin("Breakout", 1200, 600)
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

block1 = Polygon(Point(100, 40), Point(100, 60), Point(90, 60), Point(90, 40))
block2 = Polygon(Point(), Point(), Point(), Point())
block3 = Polygon(Point(), Point(), Point(), Point())
block4 = Polygon(Point(), Point(), Point(), Point())
block5 = Polygon(Point(), Point(), Point(), Point())
block6 = Polygon(Point(), Point(), Point(), Point())
block7 = Polygon(Point(), Point(), Point(), Point())
block8 = Polygon(Point(), Point(), Point(), Point())
block9 = Polygon(Point(), Point(), Point(), Point())
block10 = Polygon(Point(), Point(), Point(), Point())

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
		balldy *= -1

#math.atan2
win.getMouse()
win.close()